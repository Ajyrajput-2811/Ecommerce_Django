from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer,complete = False)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total':0,'get_cart_items':0,"shipping":False}
        cartItems = cart['get_cart_items']

    context = {"products":Product.objects.all(),"cartItems":cartItems}
    return render(request,'store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer,complete = False)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0,'get_cart_items':0,"shipping":False}
        cartItems = cart['get_cart_items']

    context = {"items":items,"cart":cart,"cartItems":cartItems}        
    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer,complete = False)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        items = []
        cart = {'get_cart_total':0,'get_cart_items':0,"shipping":False}
        cartItems = cart['get_cart_items']

    context = {"items":items,"cart":cart,"cartItems":cartItems} 
    return render(request,'checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print("productId:",productId,"action:",action)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    cart, created = Cart.objects.get_or_create(customer = customer,complete = False)
    cartitem, created = Cartitem.objects.get_or_create(product=product, cart = cart)

    if action == 'add':
        cartitem.quantity = ( cartitem.quantity + 1)
    elif action == 'remove':
        cartitem.quantity = ( cartitem.quantity - 1)
    cartitem.save()

    if cartitem.quantity <=0:
        cartitem.delete()    

    return JsonResponse({"message":'item was added'},safe = False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer,complete = False)
        total = data['form']['total']
        cart.cart_id = transaction_id

        if total == cart.get_cart_total:
            cart.complete = True
            cart.save()

        if cart.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                cart = cart,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
               
                  )    

    
    else:
        print('user is not logged in!')
        
    
    return JsonResponse('payment completed!',safe=False)    
