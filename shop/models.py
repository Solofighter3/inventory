from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Contact(models.Model):
    email=models.CharField(max_length=100)
    desc=models.TextField()
    def __str__(self):
        return self.email

class YourItem(models.Model):
    name=models.CharField(max_length=50,null=False,blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cost_per_item=models.DecimalField(max_digits=20,decimal_places=2,null=False,blank=False)
    ammount_in_stock=models.IntegerField(null=False,blank=False)
    ammount_sold=models.IntegerField(null=False,blank=False)
    sales_of_item=models.DecimalField(max_digits=20,decimal_places=2,null=False,blank=False)
    stock_date=models.DateField(auto_now_add=True)#Whenever the product is added this field will get updated
    #This updates whenever the product/object is first created
    last_sales_date=models.DateField(auto_now=True)
    #This updates whenever the product/object is saved or changed.
    def __str__(self):
        return self.name

class Orders(models.Model):
    ordername=models.CharField(max_length=100)
    order_location=models.CharField(max_length=100)
    orderer_phoneno=models.IntegerField(null=False,blank=False)
    Orderer_Username=models.ForeignKey(User,on_delete=models.CASCADE)
    product_ordered=models.ForeignKey(YourItem,on_delete=models.CASCADE)
    ordered_date=models.DateField(auto_now_add=True)#Whenever the product is added this field will get updated
    #This updates whenever the product/object is first created
    last_order_date=models.DateField(auto_now=True)
    #This updates whenever the product/object is saved or changed.
    def __str__(self):
        return self.ordername






