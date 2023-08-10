from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('signup',views.register,name="signup"),
    path('contact',views.contact,name="contact"),
    path('myproducts',views.products,name="myproducts"),
    path('per_product/<int:pk>',views.per_product,name="per_product"),
    path('addproduct',views.addtoinvent,name="addproduct"),
    path('delete/<int:pk>',views.delete_item,name="delete_item"),
    path('update_item/<int:pk>',views.update_itemsa,name="update_item"),
    path('order_product/<int:pk>',views.orders,name="order_product"),
    path('ordermessage/<int:pk>',views.ordermessage,name="ordermessage"),
    path('dashboard',views.details,name="dashboard"),

]
