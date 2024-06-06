from django.urls import path
from. import views
# urls trabalham com request e response

urlpatterns = [
    path('novo_servico/', views.novo_servico, name="novo_servico"),
]