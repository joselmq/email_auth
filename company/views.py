from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Company
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class CompanyList(ListView):
    model = Company


class CompanyInfo(DetailView):
    model = Company


class CompanyCreate(SuccessMessageMixin, CreateView):
    model = Company
    form = Company
    fields = "__all__"
    success_message = 'Empresa creada con éxito!'

    def get_success_url(self):
        return reverse('company')


class CompanyUpdate(SuccessMessageMixin, UpdateView):
    model = Company
    form = Company
    fields = '__all__'
    success_message = 'Empresa actualizada con éxito!'

    def get_success_url(self):
        return reverse('company')


class CompanyDelete(SuccessMessageMixin, DeleteView):
    model = Company
    form = Company
    fields = '__all__'

    def get_success_url(self):
        success_message = 'Empresa eliminada con éxito!'
        messages.success(self.request, success_message)
        return reverse('company')
