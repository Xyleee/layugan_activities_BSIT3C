from django.contrib import admin
from django.urls import path, include
from portfolio.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', include('portfolio.urls', namespace="portfolio")),
    path('', index, name='home'),
]