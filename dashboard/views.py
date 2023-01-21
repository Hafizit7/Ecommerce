from django.shortcuts import render
from store_app.models import Banner
from .dacorator import *
# Create your views here.
@daseboard_required
def dashboard(request):
    return render(request, 'dashboard/index.html', {})

@daseboard_required
def banner_list(request):
    banner_list = Banner.objects.all()
    return render(request, 'dashboard/banner/banner-list.html', {'banner_list':banner_list})
    