
"""Kiski URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('portfolio_overview/', views.firstpage, name="firstpage"),
    path('net_exposure/', views.secondpage, name="secondpage"),
    path('factor_contribution/', views.thirdpage, name="thirdpage"),
    path('gross_exposure_pnl/', views.fourthpage, name="fourthpage"),
    path('value_at_risk/', views.fifthpage, name="fifthpage"),
    path('excess_volume_return_distribution/', views.sixthpage, name="sixthpage"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path('voicebot/', views.voicebot, name="voicebot")
]