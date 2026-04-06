from django.urls import path
from .views import CompanyListView, FinancialUploadView, ReviewUploadView, NotificationListView, \
    MarkNotificationReadView, DashboardDataView, ClientUploadHistoryView, BaseReportListView, CreateReportRequestView, \
    FulfillReportRequestView

urlpatterns = [
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:company_id>/dashboard/', DashboardDataView.as_view(), name='dashboard-data'),

    path('uploads/', FinancialUploadView.as_view(), name='upload-create'),
    path('companies/<int:company_id>/uploads/', ClientUploadHistoryView.as_view(), name='upload-history'),
    path('uploads/<int:upload_id>/review/', ReviewUploadView.as_view(), name='upload-review'),

    path('companies/<int:company_id>/reports/standard/', BaseReportListView.as_view(), name='report-standard-list'),
    path('companies/<int:company_id>/reports/request/', CreateReportRequestView.as_view(),
         name='report-request-create'),
    path('reports/requests/<int:request_id>/fulfill/', FulfillReportRequestView.as_view(), name='report-fulfill'),

    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]