from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
from .models import *
from .filters import OrderFilter
from .forms import *

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was created for ' + user)
                return redirect('login')


        contex={'form':form}
        return render(request,'accounts/register.html',contex)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Incorrect credintials ')

        contex={}
        return render(request,'accounts/login.html',contex)

def logoutUser(request):
    logout(request)
    return redirect ('login')

@login_required(login_url='login')
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

@login_required(login_url='login')
def products(request):
    products = Products.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
def customers(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    order_count=orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs
    contex={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter,}
    return render(request, 'accounts/customers.html',contex)

@login_required(login_url='login')
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    form=OrderForm(initial={'customer':customer})
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    contex={'form':form,}
    return render(request,'accounts/order_form.html',contex)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request,'accounts/delete.html',context)