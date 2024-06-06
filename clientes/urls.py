from django.urls import path
from. import views
# urls trabalham com request e response

urlpatterns = [
    path('', views.clientes, name= "clientes"),
    path('atualiza_cliente/', views.att_cliente, name="atualiza_cliente"),
    path('update_ar/<int:id>', views.update_ar, name="update_ar"),
    path('excluir_ar/<int:id>', views.excluir_ar, name="excluir_ar"),
    path('update_cliente/<int:id>', views.update_cliente, name="update_cliente")
]