from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import *

from .forms import *


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    contex = {'orders': orders, 'customers': customers, 'total_customer': total_customer,
              'total_order': total_order, 'delivered': delivered,'pending':pending}
    return render(request, 'accounts/dashboard.html', contex)


def products(request):
    products = Products.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customers(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    order_count=orders.count()

    contex={'customer':customer,'orders':orders,'order_count':order_count}
    return render(request, 'accounts/customers.html',contex)

def createOrder(request):
    form=OrderForm()
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')


    contex={'form':form}

    return render(request,'accounts/order_form.html',contex)

def updateOrder(request,pk):
    
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method =='POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    


    contex={'form':form}
    return render(request,'accounts/order_form.html',contex)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request,'accounts/delete.html',context)