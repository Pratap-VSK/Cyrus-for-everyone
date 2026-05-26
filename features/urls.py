from django.urls import path
from . import views

urlpatterns = [
    # Navigation Routes (Frontend Pages)
    path('', views.home_page, name='home'),
    path('calculator/', views.calculator_page, name='calculator'),
    path('height/', views.height_page, name='height'),
    path('distance/', views.distance_page, name='distance'),
    path('area/', views.area_page, name='area'),
    path('weight/', views.weight_page, name='weight'),
    path('gst/', views.gst_page, name='gst'),
    path('student/', views.student_page, name='student'),

    # API Endpoint Routes (Backend Calculations)
    path('calculate/', views.process_calculation, name='calculate'),
    path('calculate-height/', views.calculate_height, name='calculate_height'),
    path('calculate-distance/', views.calculate_distance, name='calculate_distance'),
    path('calculate-area/', views.calculate_area, name='calculate_area'),
    path('calculate-weight/', views.calculate_weight, name='calculate_weight'),
    path('calculate-gst/', views.calculate_gst, name='calculate_gst'),
    path('calculate-physics/', views.calculate_physics, name='calculate_physics'),
]