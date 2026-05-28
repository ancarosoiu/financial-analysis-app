from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CompanyListView,
    FinancialUploadView,
    ReviewUploadView,
    NotificationListView,
    MarkNotificationReadView,
    DashboardDataView,
    ClientUploadHistoryView,
    BaseReportListView,
    CreateReportRequestView,
    FulfillReportRequestView,
    MyTokenObtainPairView,
    RegisterClientView,
    RegisterAnalystView,
    AnalystDashboardStatsView,
    AnalystPendingUploadsView,
    AnalystUploadsView
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/client/', RegisterClientView.as_view(), name='register-client'),
    path('register/analyst/', RegisterAnalystView.as_view(), name='register-analyst'),

    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:company_id>/dashboard/', DashboardDataView.as_view(), name='dashboard-data'),

    path('analyst/dashboard-stats/', AnalystDashboardStatsView.as_view(), name='analyst-dashboard-stats'),
    path('analyst/uploads/pending/', AnalystPendingUploadsView.as_view(), name='analyst-pending-uploads'),
    path('analyst/uploads/', AnalystUploadsView.as_view(), name='analyst-uploads'),

    path('uploads/', FinancialUploadView.as_view(), name='upload-create'),
    path('companies/<int:company_id>/uploads/', ClientUploadHistoryView.as_view(), name='upload-history'),
    path('uploads/<int:upload_id>/review/', ReviewUploadView.as_view(), name='upload-review'),

    path('companies/<int:company_id>/reports/standard/', BaseReportListView.as_view(), name='report-standard-list'),
    path('companies/<int:company_id>/reports/request/', CreateReportRequestView.as_view(), name='report-request-create'),
    path('reports/requests/<int:request_id>/fulfill/', FulfillReportRequestView.as_view(), name='report-fulfill'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]