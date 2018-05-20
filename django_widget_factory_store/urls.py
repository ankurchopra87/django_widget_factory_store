"""django_widget_factory_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from rest_framework import routers
from store import views
from store.admin import admin_site
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


# Django Rest Framework router registration
router = routers.DefaultRouter()
router.register(r'skus', views.SKUViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'product_attributes', views.AttributeViewSet)
router.register(r'product_attribute_types', views.AttributeTypeViewSet)

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='index.html'), name="home"),
    path('admin/', admin_site.urls),
    path('api/', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
