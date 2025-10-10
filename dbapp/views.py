from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return render(request, 'dbapp/dashboard.html')

def goods_table(request):
    return render(request, 'dbapp/goods_table.html')