from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('book/', views.book, name='book'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.signout, name='signout'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('tips/', views.tips, name='tips'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('submit-testimonial/', views.submit_testimonial, name='submit_testimonial'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]