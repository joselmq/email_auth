from django.urls import path

from company import views as com_views

urlpatterns = [
    # Company
    path("", com_views.ListCompanyView.as_view(), name="company_list"),
    path("create", com_views.CreateCompanyView.as_view(), name="company_create"),
    path("update/<int:pk>/", com_views.UpdateCompanyView.as_view(), name="update_company"),
    path("delete/<int:pk>/", com_views.DeleteCompanyView.as_view(), name="delete_company"),

    # Invoice
    path("invoice", com_views.ListInvoiceView.as_view(), name="invoice_list"),
]
