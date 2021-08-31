from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse


class HomePageView(TemplateView):
    template_name = "home.html"

