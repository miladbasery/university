from django.urls import path
from . import views

urlpatterns = [
    # اسم این مسیر را dashboard می‌گذاریم تا redirect('dashboard') کار کند
    path('dashboard/', views.dashboard_view, name='dashboard'),
]