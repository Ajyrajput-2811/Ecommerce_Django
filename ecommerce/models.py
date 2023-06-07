from django.db import models
import uuid 
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    name = models.CharField( max_length=50)
    email = models.EmailField( max_length=254)

    def __str__(self)->str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)    
    price = models.IntegerField()
    digital = models.BooleanField(default=False,null = True,blank=False)
    images = models.ImageField()

    def __str__(self)->str:
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url           

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE,blank = True , null = True)
    cart_id = models.UUIDField(default = uuid.uuid4 ,unique = True,editable = False)     
    complete = models.BooleanField(default = False,null=True,blank=False)

    def __str__(self)->str:
        return str(self.id) 

    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total

    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total   

    @property
    def shipping(self):
        shipping = False
        cartitems = self.cartitem_set.all()
        for i in cartitems:
            if i.product.digital == False:
                shipping = True
        return shipping     


class Cartitem(models.Model):
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)    
    quantity = models.IntegerField(default = 0)

    def __str__(self)->str: 
        return self.product.name

    @property
    def get_total(self)->str:
        total = self.product.price * self.quantity
        return total   

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete = models.CASCADE)
    address = models.CharField( max_length=50)
    city = models.CharField( max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField( max_length=50)
    def __str__(self)->str:
        return self.address

    

