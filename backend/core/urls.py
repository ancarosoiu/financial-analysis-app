from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CompanyListView,
    DownloadFinancialUploadView,
    FinancialUploadView,
    ReviewUploadView,
    NotificationListView,
    MarkNotificationReadView,
    DashboardDataView,
    ClientUploadHistoryView,
    BaseReportListView,
    DownloadBaseReportView,
    CreateReportRequestView,
    ClientReportRequestListView,
    AnalystReportRequestListView,
    FulfillReportRequestView,
    DownloadCustomReportView,
    MyTokenObtainPairView,
    RegisterClientView,
    RegisterAnalystView,
    AnalystDashboardStatsView,
    AnalystPendingUploadsView,
    AnalystUploadsView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/client/', RegisterClientView.as_view(), name='register-client'),
    # path('register/analyst/', RegisterAnalystView.as_view(), name='register-analyst'),

    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:company_id>/dashboard/', DashboardDataView.as_view(), name='dashboard-data'),

    path('analyst/dashboard-stats/', AnalystDashboardStatsView.as_view(), name='analyst-dashboard-stats'),
    path('analyst/uploads/pending/', AnalystPendingUploadsView.as_view(), name='analyst-pending-uploads'),
    path('analyst/uploads/', AnalystUploadsView.as_view(), name='analyst-uploads'),

    path('uploads/', FinancialUploadView.as_view(), name='upload-create'),
    path('companies/<int:company_id>/uploads/', ClientUploadHistoryView.as_view(), name='upload-history'),
    path('uploads/<int:upload_id>/review/', ReviewUploadView.as_view(), name='upload-review'),
    path("uploads/<int:upload_id>/download/",DownloadFinancialUploadView.as_view(),name="download-financial-upload"),

    path('companies/<int:company_id>/reports/standard/', BaseReportListView.as_view(), name='report-standard-list'),
    path('reports/standard/<int:report_id>/download/', DownloadBaseReportView.as_view(),name='report-standard-download'),
    path('companies/<int:company_id>/reports/request/', CreateReportRequestView.as_view(),name='report-request-create'),
    path('companies/<int:company_id>/reports/requests/', ClientReportRequestListView.as_view(),name='client-report-requests'),
    path('analyst/reports/requests/', AnalystReportRequestListView.as_view(), name='analyst-report-requests'),
    path('reports/requests/<int:request_id>/fulfill/', FulfillReportRequestView.as_view(), name='report-fulfill'),
    path('reports/custom/<int:report_id>/download/', DownloadCustomReportView.as_view(), name='report-custom-download'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]