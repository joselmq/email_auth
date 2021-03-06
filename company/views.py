from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)

from .models import Company, Invoice
from .serializers import CompanySerializer, InvoiceSerializer


# Company Views
class ListCompanyView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CreateCompanyView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class UpdateCompanyView(UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DeleteCompanyView(DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# Invoice Views
class ListInvoiceView(ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class CreateInvoiceView(CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class UpdateInvoiceView(UpdateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class DeleteInvoiceView(DestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
