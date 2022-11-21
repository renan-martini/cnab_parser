from django.urls import path
from parser import views


urlpatterns = [
    path("parser/", views.CreateCNAB.as_view()),
    path("transactions/<str:store_name>/", views.ListOperations.as_view()),
]
