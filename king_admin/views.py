from django.shortcuts import render

from . import app_config
from .base_admin import registered_sites

# Create your views here.
def app_index(request):
    print(registered_sites)
    return render(request, 'king_admin/app_index.html')
