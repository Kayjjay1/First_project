from django.urls import path

from . import views

urlpatterns = [
    path('hospital/<str:hospital_id>/<str:status>/', views.DoctorManagementView.as_view()),
    path('hospital/<str:hospital_id>/<str:user_id>/', views.DoctorManagementView.as_view()),
    path('hospital/<str:hospital_id>/', views.DoctorAcceptDoctorInvitate.as_view()),
]