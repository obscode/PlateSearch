from django.urls import path

from . import views

urlpatterns = [
    path("", views.plate_search, name="search"),
    path("<int:plateid>/", views.plate_view, name="plateview")
]
