from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from . import *


class IndexPage(TemplateView):
    template_name = 'index.html'
