from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from .models import Company, FinancialUpload, Notification, BaseReport, ReportRequest, CustomReport, KPISnapshot
from .serializers import RegisterClientSerializer, RegisterAnalystSerializer,MyTokenObtainPairSerializer
from .services import process_financial_upload

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
                "status_onboarded": company.is_onboarded,
                "analist_nume": company.analyst.username if company.analyst else "Neatribuit",
                "owner_username": company.owner.username,
                "data_inregistrare": company.created_at.strftime("%d/%m/%Y")
            })
        return Response(data)

class FinancialUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        file_obj = request.FILES.get('file')
        company_id = request.data.get('company_id')

        if not file_obj or not company_id:
            return Response({"error": "Lipsesc fișierul sau ID-ul firmei"}, status=400)

        try:
            company = Company.objects.for_user(user).get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Firma nu a fost găsită sau nu ai acces"}, status=403)

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

        return Response({
            "message": "Fișierul a fost încărcat cu succes!",
            "upload_id": upload.id,
            "file_path": upload.file.name,
            "status": upload.status
        }, status=201)

class ReviewUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, upload_id):
        user = request.user
        decision = request.data.get('decision')
        reason = request.data.get('reason', '')

        if user.role != 'analyst' and not user.is_staff:
            return Response({"error": "Acces interzis"}, status=403)

        try:
            upload = FinancialUpload.objects.get(id=upload_id)
            client = upload.company.owner

            if decision == 'approve':
                success, message = process_financial_upload(upload)

                if success:
                    upload.status = 'approved'
                    upload.processed_by = user
                    upload.processed_at = timezone.now()
                    upload.save()

                    Notification.objects.create(
                        sender=user,
                        recipient=client,
                        title="Import Aprobat!",
                        message=f"Datele pentru firma {upload.company.name} au fost validate. Dashboard-ul tău este acum activ.",
                        action_url="/dashboard"
                    )

                    return Response({"message": "Fișier aprobat și date salvate!"})
                else:
                    return Response({"error": f"Procesarea a eșuat la validare: {message}"}, status=400)

            elif decision == 'reject':
                upload.status = 'rejected'
                upload.rejection_reason = reason
                upload.processed_by = user
                upload.processed_at = timezone.now()
                upload.save()

                Notification.objects.create(
                    sender=user,
                    recipient=client,
                    title="Import Respins",
                    message=f"Importul pentru {upload.company.name} a fost respins. Motiv: {reason}",
                    action_url="/upload"
                )

                return Response({"message": "Import respins cu succes."})

        except FinancialUpload.DoesNotExist:
            return Response({"error": "Upload negăsit"}, status=404)

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

    def get(self, request, company_id):
        try:
            company = Company.objects.for_user(request.user).get(id=company_id)
            statements = company.statements.all().select_related('kpi_snapshot').order_by('-reporting_date')

            data = []
            for s in statements:
                kpi = getattr(s, 'kpi_snapshot', None)
                data.append({
                    "id": s.id,
                    "date": s.reporting_date.strftime("%Y-%m-%d"),
                    "profit": float(s.net_profit),
                    "venituri": float(s.sales_revenue),
                    "probabilitate_faliment": kpi.bankruptcy_probability if kpi else None,
                    "eticheta": kpi.prediction_label if kpi else None,
                    "importanta_indicatori": kpi.feature_importance_data if kpi else {},
                    "kpis": {
                        "lichiditate": kpi.x4 if kpi else None,
                        "profitabilitate": kpi.x1 if kpi else None,
                        "leverage": kpi.x2 if kpi else None,
                    }
                })

            return Response({
                "company_name": company.name,
                "is_onboarded": company.is_onboarded,
                "summary": company.financial_summary,
                "history": data
            })
        except Company.DoesNotExist:
            return Response({"error": "Acces interzis"}, status=403)


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