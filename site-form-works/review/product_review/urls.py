"""product_review URL Configuration

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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app.views import ProductsList, ProductView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('', ProductsList.as_view(), name='main_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from app.views import product_list_view, product_view
#
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('product/<int:pk>/', product_view, name='product_detail'),
#     path('', product_list_view, name='main_page'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
