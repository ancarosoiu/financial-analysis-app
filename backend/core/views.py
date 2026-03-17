from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Company, FinancialUpload, Notification
from .services import process_financial_upload

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