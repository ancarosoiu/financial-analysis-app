from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from .models import Company, FinancialUpload, Notification, BaseReport, ReportRequest, CustomReport, KPISnapshot, MLModelVersion
from .serializers import RegisterClientSerializer, RegisterAnalystSerializer,MyTokenObtainPairSerializer
from .services import process_financial_upload, auto_assign_analyst
from django.db.models import Case, When, IntegerField
from datetime import timedelta

class RegisterClientView(generics.CreateAPIView):
    serializer_class = RegisterClientSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Cont client creat cu succes.",
                "username": user.username,
                "role": "client",
            },
            status=status.HTTP_201_CREATED,
        )


class RegisterAnalystView(generics.CreateAPIView):
    serializer_class = RegisterAnalystSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Cont analist creat cu succes.",
                "username": user.username,
                "role": "analyst",
            },
            status=status.HTTP_201_CREATED,
        )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ClientUploadHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        try:
            company = Company.objects.for_user(request.user).get(id=company_id)
            uploads = company.uploads.all().order_by('-uploaded_at')
            data = [{
                "id": u.id,
                "data_incarcare": u.uploaded_at.strftime("%d/%m/%Y %H:%M"),
                "status": u.status,
                "nume_fisier": u.file.name.split('/')[-1],
                "motiv_respingere": u.rejection_reason
            } for u in uploads]
            return Response(data)
        except Company.DoesNotExist:
            return Response({"error": "Acces interzis"}, status=403)


class AnalystDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'analyst' and not request.user.is_staff:
            return Response({"error": "Acces interzis"}, status=403)

        my_companies = Company.objects.filter(analyst=request.user)
        pending_uploads = FinancialUpload.objects.filter(company__analyst=request.user, status='pending').count()
        pending_reports = ReportRequest.objects.filter(analyst=request.user, status='pending').count()

        high_risk_count = 0
        for comp in my_companies:
            last_snapshot = KPISnapshot.objects.filter(statement__company=comp).order_by(
                '-statement__reporting_date').first()
            if last_snapshot and last_snapshot.bankruptcy_probability > 50:
                high_risk_count += 1

        return Response({
            "total_firme": my_companies.count(),
            "importuri_noi": pending_uploads,
            "cereri_rapoarte_noi": pending_reports,
            "firme_risc_ridicat": high_risk_count
        })

class AnalystPendingUploadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'analyst' and not request.user.is_staff:
            return Response({"error": "Acces interzis"}, status=403)

        uploads = FinancialUpload.objects.filter(
            status='pending'
        ).select_related(
            'company',
            'company__owner',
            'company__analyst'
        ).order_by('-uploaded_at')

        if request.user.role == 'analyst' and not request.user.is_staff:
            uploads = uploads.filter(company__analyst=request.user)

        data = []

        for upload in uploads:
            data.append({
                "id": upload.id,
                "company_id": upload.company.id,
                "company_name": upload.company.name,
                "cui": upload.company.cui,
                "industry": upload.company.industry,
                "client_username": upload.company.owner.username,
                "file_name": upload.file.name.split('/')[-1],
                "uploaded_at": upload.uploaded_at.strftime("%d/%m/%Y %H:%M"),
                "status": upload.status,
            })

        return Response(data)

class AnalystUploadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'analyst' and not request.user.is_staff:
            return Response({"error": "Acces interzis"}, status=403)

        status_filter = request.query_params.get("status", "pending")

        uploads = FinancialUpload.objects.select_related(
            "company",
            "company__owner",
            "company__analyst",
            "processed_by",
        )

        if request.user.role == "analyst" and not request.user.is_staff:
            uploads = uploads.filter(company__analyst=request.user)

        if status_filter != "all":
            uploads = uploads.filter(status=status_filter)

        uploads = uploads.annotate(
            status_order=Case(
                When(status="pending", then=0),
                When(status="approved", then=1),
                When(status="rejected", then=2),
                default=3,
                output_field=IntegerField(),
            )
        ).order_by("status_order", "uploaded_at")

        data = []

        for upload in uploads:
            data.append({
                "id": upload.id,
                "company_id": upload.company.id,
                "company_name": upload.company.name,
                "cui": upload.company.cui,
                "industry": upload.company.industry,
                "client_username": upload.company.owner.username,
                "analyst_username": upload.company.analyst.username if upload.company.analyst else None,
                "file_name": upload.file.name.split("/")[-1],
                "uploaded_at": upload.uploaded_at.strftime("%d/%m/%Y %H:%M"),
                "status": upload.status,
                "processed_by": upload.processed_by.username if upload.processed_by else None,
                "processed_at": upload.processed_at.strftime("%d/%m/%Y %H:%M") if upload.processed_at else None,
                "rejection_reason": upload.rejection_reason,
            })

        return Response(data)

class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        companies = Company.objects.for_user(request.user)

        data = []
        for company in companies:
            data.append({
                "id": company.id,
                "nume": company.name,
                "cui": company.cui,
                "industrie": company.industry,
                "adresa": company.address,
                "email": company.email_contact,
                "telefon": company.phone_number,
                "status_onboarded": company.is_onboarded,
                "analist_nume": company.analyst.username if company.analyst else "Neatribuit",
                "owner_username": company.owner.username,
                "data_inregistrare": company.created_at.strftime("%d/%m/%Y")
            })

        return Response(data)

    def post(self, request):
        if request.user.role != "client":
            return Response(
                {"error": "Doar utilizatorii de tip client pot crea o companie."},
                status=403
            )

        existing_company = Company.objects.filter(owner=request.user).first()

        if existing_company:
            return Response(
                {
                    "message": "Clientul are deja o companie asociată.",
                    "company_id": existing_company.id,
                    "company_name": existing_company.name,
                    "is_onboarded": existing_company.is_onboarded,
                },
                status=200
            )

        name = request.data.get("name")
        cui = request.data.get("cui")
        industry = request.data.get("industry", "")
        address = request.data.get("address", "")
        phone_number = request.data.get("phone_number", "")
        email_contact = request.data.get("email_contact", "")

        if not name or not cui:
            return Response(
                {"error": "Denumirea companiei și CUI-ul sunt obligatorii."},
                status=400
            )

        if Company.objects.filter(cui=cui).exists():
            return Response(
                {"error": "Există deja o companie cu acest CUI."},
                status=400
            )

        company = Company.objects.create(
            name=name,
            cui=cui,
            industry=industry,
            address=address,
            phone_number=phone_number,
            email_contact=email_contact,
            owner=request.user,
            is_onboarded=False,
        )

        return Response(
            {
                "message": "Compania a fost creată cu succes.",
                "company_id": company.id,
                "company_name": company.name,
                "is_onboarded": company.is_onboarded,
            },
            status=201
        )

class FinancialUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        file_obj = request.FILES.get('file')
        company_id = request.data.get('company_id')

        if not file_obj or not company_id:
            return Response(
                {"error": "Lipsesc fișierul sau ID-ul firmei."},
                status=400
            )

        try:
            company = Company.objects.for_user(user).get(id=company_id)
        except Company.DoesNotExist:
            return Response(
                {"error": "Firma nu a fost găsită sau nu ai acces."},
                status=403
            )

        # 1. Nu permitem un import nou dacă există deja unul în așteptare.
        pending_exists = FinancialUpload.objects.filter(
            company=company,
            status="pending"
        ).exists()

        if pending_exists:
            return Response(
                {
                    "error": "Există deja un import în așteptare pentru această firmă. Așteaptă validarea lui înainte de a încărca alt fișier.",
                    "code": "pending_import_exists"
                },
                status=409
            )

        # 2. Dacă firma este deja onboarded, permitem import nou doar după 30 zile
        # de la ultimul import aprobat.
        if company.is_onboarded:
            last_approved_upload = FinancialUpload.objects.filter(
                company=company,
                status="approved",
                processed_at__isnull=False
            ).order_by("-processed_at").first()

            if last_approved_upload:
                today = timezone.localdate()
                next_allowed_date = last_approved_upload.processed_at.date() + timedelta(days=30)

                if today < next_allowed_date:
                    return Response(
                        {
                            "error": f"Poți încărca un import nou abia după data de {next_allowed_date.strftime('%d/%m/%Y')}.",
                            "code": "too_soon_after_last_approved_import",
                            "next_allowed_date": next_allowed_date.strftime("%Y-%m-%d")
                        },
                        status=409
                    )

        # 3. Asignare automată analist dacă firma nu are încă.
        if not company.analyst:
            auto_assign_analyst(company)
            company.refresh_from_db()

        upload = FinancialUpload.objects.create(
            company=company,
            file=file_obj,
            status='pending'
        )

        if company.analyst:
            Notification.objects.create(
                sender=user,
                recipient=company.analyst,
                title="Document nou în așteptare",
                message=f"Clientul {user.username} a încărcat un fișier nou pentru firma {company.name}. Te rugăm să îl validezi.",
                action_url=f"/analyst/review/{upload.id}"
            )

        return Response(
            {
                "message": "Fișierul a fost încărcat cu succes!",
                "upload_id": upload.id,
                "file_path": upload.file.name,
                "status": upload.status
            },
            status=201
        )

class ReviewUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, upload_id):
        user = request.user
        decision = request.data.get('decision')
        reason = request.data.get('reason', '')

        if user.role != 'analyst' and not user.is_staff:
            return Response(
                {"error": "Acces interzis. Doar analiștii pot procesa importuri."},
                status=403
            )

        if decision not in ['approve', 'reject']:
            return Response(
                {"error": "Decizie invalidă. Folosește 'approve' sau 'reject'."},
                status=400
            )

        try:
            upload = FinancialUpload.objects.select_related(
                'company',
                'company__owner',
                'company__analyst'
            ).get(id=upload_id)

            client = upload.company.owner

            if upload.status != 'pending':
                return Response(
                    {"error": "Acest import a fost deja procesat."},
                    status=400
                )

            if user.role == 'analyst' and upload.company.analyst != user:
                return Response(
                    {"error": "Nu ești analistul asignat acestei companii."},
                    status=403
                )

            if decision == 'approve':
                success, message = process_financial_upload(upload)

                if success:
                    upload.status = 'approved'
                    upload.processed_by = user
                    upload.processed_at = timezone.now()
                    upload.rejection_reason = None
                    upload.save()

                    Notification.objects.create(
                        sender=user,
                        recipient=client,
                        title="Import aprobat",
                        message=(
                            f"Datele pentru firma {upload.company.name} au fost validate. "
                            "Dashboard-ul tău este acum activ."
                        ),
                        action_url="/dashboard"
                    )

                    return Response(
                        {
                            "message": "Fișier aprobat și date salvate cu succes.",
                            "upload_id": upload.id,
                            "company_id": upload.company.id,
                            "company_is_onboarded": upload.company.is_onboarded,
                        },
                        status=200
                    )

                return Response(
                    {"error": f"Procesarea a eșuat la validare: {message}"},
                    status=400
                )

            if decision == 'reject':
                if not reason:
                    return Response(
                        {"error": "Motivul respingerii este obligatoriu."},
                        status=400
                    )

                upload.status = 'rejected'
                upload.rejection_reason = reason
                upload.processed_by = user
                upload.processed_at = timezone.now()
                upload.save()

                Notification.objects.create(
                    sender=user,
                    recipient=client,
                    title="Import respins",
                    message=(
                        f"Importul pentru firma {upload.company.name} a fost respins. "
                        f"Motiv: {reason}"
                    ),
                    action_url="/upload"
                )

                return Response(
                    {
                        "message": "Import respins cu succes.",
                        "upload_id": upload.id,
                    },
                    status=200
                )

        except FinancialUpload.DoesNotExist:
            return Response(
                {"error": "Upload-ul nu a fost găsit."},
                status=404
            )

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = request.user.received_notifications.all()[:10] # Ultimele 10
        data = [{
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at.strftime("%d/%m %H:%M")
        } for n in notifications]
        return Response(data)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)

            notification.is_read = True
            notification.save()

            return Response({
                "status": "success",
                "message": "Notificarea a fost marcată ca citită."
            }, status=200)

        except Notification.DoesNotExist:
            return Response({
                "error": "Notificarea nu a fost găsită sau nu aveți acces la ea."
            }, status=404)

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def _safe_float(self, value):
        """
        Transformă valorile Decimal / Float din baza de date în float
        pentru a putea fi trimise corect în răspunsul JSON.
        """
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def get(self, request, company_id):
        try:
            company = Company.objects.for_user(request.user).get(id=company_id)

            statements = (
                company.statements
                .select_related("kpi_snapshot")
                .order_by("reporting_date")
            )

            history = []

            for statement in statements:
                kpi = getattr(statement, "kpi_snapshot", None)

                history.append({
                    "id": statement.id,
                    "date": statement.reporting_date.strftime("%Y-%m-%d"),

                    # =========================
                    # DATE FINANCIARE PRINCIPALE
                    # =========================
                    "profit": self._safe_float(statement.net_profit),
                    "venituri": self._safe_float(statement.sales_revenue),
                    "ebit": self._safe_float(statement.ebit),
                    "cheltuieli_operationale": self._safe_float(statement.operating_expenses),

                    "active_totale": self._safe_float(statement.total_assets),
                    "active_curente": self._safe_float(statement.current_assets),
                    "cash": self._safe_float(statement.cash),
                    "stocuri": self._safe_float(statement.inventory),

                    "datorii_totale": self._safe_float(statement.total_liabilities),
                    "datorii_curente": self._safe_float(statement.short_term_liabilities),
                    "capitaluri_proprii": self._safe_float(statement.equity),
                    "profit_retinut": self._safe_float(statement.retained_earnings),

                    # =========================
                    # PREDICȚIE ML + SHAP LOCAL
                    # =========================
                    "probabilitate_faliment": (
                        self._safe_float(kpi.bankruptcy_probability)
                        if kpi else None
                    ),
                    "eticheta": (
                        kpi.prediction_label
                        if kpi else None
                    ),

                    # Aici se trimite explicația SHAP locală salvată
                    # pentru perioada financiară respectivă.
                    "importanta_indicatori": (
                        kpi.feature_importance_data
                        if kpi and kpi.feature_importance_data else {}
                    ),

                    # =========================
                    # KPI-URI PENTRU DASHBOARD
                    # =========================
                    "kpis": {
                        # KPI-urile principale afișate în carduri
                        "rentabilitate_active": (
                            self._safe_float(kpi.x1) if kpi else None
                        ),  # profit net / active totale

                        "grad_indatorare": (
                            self._safe_float(kpi.x2) if kpi else None
                        ),  # datorii totale / active totale

                        "capital_lucru_active": (
                            self._safe_float(kpi.x3) if kpi else None
                        ),  # capital de lucru / active totale

                        "lichiditate_curenta": (
                            self._safe_float(kpi.x4) if kpi else None
                        ),  # active curente / datorii curente

                        "profit_retinut_active": (
                            self._safe_float(kpi.x6) if kpi else None
                        ),  # profit reținut / active totale

                        "ebit_active": (
                            self._safe_float(kpi.x7) if kpi else None
                        ),  # EBIT / active totale

                        "capitaluri_datorii": (
                            self._safe_float(kpi.x8) if kpi else None
                        ),  # capitaluri proprii / datorii totale

                        "rotatie_active": (
                            self._safe_float(kpi.x9) if kpi else None
                        ),  # vânzări / active totale

                        "solvabilitate": (
                            self._safe_float(kpi.x10) if kpi else None
                        ),  # capitaluri proprii / active totale

                        "profit_vanzari": (
                            self._safe_float(kpi.x23) if kpi else None
                        ),  # profit net / vânzări

                        "log_active": (
                            self._safe_float(kpi.x29) if kpi else None
                        ),  # logaritmul activelor totale

                        "capital_lucru": (
                            self._safe_float(kpi.x55) if kpi else None
                        ),  # capital de lucru

                        # Chei compatibile cu eventualele componente vechi din frontend
                        "lichiditate": (
                            self._safe_float(kpi.x4) if kpi else None
                        ),
                        "profitabilitate": (
                            self._safe_float(kpi.x1) if kpi else None
                        ),
                        "leverage": (
                            self._safe_float(kpi.x2) if kpi else None
                        ),
                    }
                })

            latest_snapshot = history[-1] if history else None

            active_model = MLModelVersion.objects.filter(is_active=True).first()

            model_info = None

            if active_model:
                model_info = {
                    "name": active_model.name,
                    "version": active_model.version,
                    "accuracy": self._safe_float(active_model.accuracy),
                    "f1_score": self._safe_float(active_model.f1_score),
                }

            return Response({
                "company_name": company.name,
                "is_onboarded": company.is_onboarded,
                "summary": company.financial_summary,
                "history": history,
                "latest": latest_snapshot,
                "model": model_info,
            })

        except Company.DoesNotExist:
            return Response(
                {"error": "Acces interzis sau compania nu există."},
                status=403
            )

class BaseReportListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, company_id):
        try:
            company = Company.objects.for_user(request.user).get(id=company_id)

            reports = BaseReport.objects.filter(snapshot__statement__company=company)

            data = []
            for rep in reports:
                snapshot = rep.snapshot
                data.append({
                    "id": rep.id,
                    "data_generare": rep.generated_at.strftime("%d/%m/%Y"),
                    "data_bilant": snapshot.statement.reporting_date.strftime("%d/%m/%Y"),
                    "probabilitate_faliment": f"{snapshot.bankruptcy_probability}%",
                    "status_risc": snapshot.prediction_label,
                    "pdf_url": rep.pdf_file.url if rep.pdf_file else None
                })

            return Response(data)

        except Company.DoesNotExist:
            return Response({"error": "Acces interzis sau firma nu există"}, status=403)


class CreateReportRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, company_id):
        user = request.user
        client_message = request.data.get('message', '')

        if not client_message:
            return Response({"error": "Te rugăm să completezi cerințele tale pentru analist."}, status=400)

        try:
            company = Company.objects.for_user(user).get(id=company_id)

            report_request = ReportRequest.objects.create(
                company=company,
                analyst=company.analyst,
                client_message=client_message,
                status='pending'
            )

            if company.analyst:
                from .models import Notification
                Notification.objects.create(
                    sender=user,
                    recipient=company.analyst,
                    title="Solicitare Raport Nouă",
                    message=f"Firma {company.name} a solicitat o analiză personalizată.",
                    action_url=f"/analyst/requests/{report_request.id}"
                )

            return Response({
                "message": "Solicitarea a fost trimisă cu succes către analistul tău!",
                "request_id": report_request.id
            }, status=201)

        except Company.DoesNotExist:
            return Response({"error": "Firma nu a fost găsită"}, status=404)


class FulfillReportRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        user = request.user

        if user.role != 'analyst' and not user.is_staff:
            return Response({"error": "Doar analiștii pot completa rapoarte."}, status=403)

        try:
            report_request = ReportRequest.objects.get(id=request_id, analyst=user)

            if report_request.status == 'completed':
                return Response({"error": "Acest raport a fost deja finalizat."}, status=400)

            analyst_message = request.data.get('analyst_message')
            recommendations = request.data.get('recommendations')

            custom_report = CustomReport.objects.create(
                request=report_request,
                analyst_message=analyst_message,
                expert_recommendations=recommendations,
                extra_data_json=request.data.get('extra_data', {})
            )

            report_request.status = 'completed'
            report_request.save()

            return Response({
                "message": "Raportul personalizat a fost salvat și trimis clientului!",
                "report_id": custom_report.id
            })

        except ReportRequest.DoesNotExist:
            return Response({"error": "Cererea nu a fost găsită sau nu ești asignat pe ea."}, status=404)