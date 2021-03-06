"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from module.moduleapi import views

# http://127.0.0.1:8000/users
router = routers.DefaultRouter()
router.register(r'MyProjectStock', views.MyProjectStockViewSet)
router.register(r'MyProjectWeather', views.MyProjectWeatherViewSet)
router.register(r'Savestockprice', views.SavestockpriceViewSet)
router.register(r'Savestockratio', views.SavestockratioViewSet)
router.register(r'Saveweathertemp', views.SaveWeathertempViewSet)
router.register(r'Saveweathertempwithhumid', views.SaveWeathertempwithhumidViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('apt-auth', include('rest_framework.urls', namespace='rest_framework'))
]
