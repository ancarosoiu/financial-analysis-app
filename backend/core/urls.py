from django.urls import path
from .views import CompanyListView, FinancialUploadView, ReviewUploadView, NotificationListView, MarkNotificationReadView, DashboardDataView

urlpatterns = [
    path('firme/', CompanyListView.as_view(), name='lista-firme'),
    path('upload/', FinancialUploadView.as_view(), name='upload-financiar'),

    path('review-upload/<int:upload_id>/', ReviewUploadView.as_view(), name='review-upload'),

    path('notificari/', NotificationListView.as_view(), name='lista-notificari'),
    path('notificari/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notificare-citita'),

    path('dashboard/<int:company_id>/', DashboardDataView.as_view(), name='dashboard-data'),
]