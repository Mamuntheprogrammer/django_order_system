from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Products(models.Model):
    CATEGORY = (('Indoor', 'Indoor'), ('Out door', 'Out door'))
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name


class Order(models.Model):
    def __str__(self):
        return self.product.name


    STATUS = (('Pending', 'Pending'), ('Out for Delivery',
                                       'Out for Delivery'), ('Delivered', 'Delivered'))

    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    note=models.CharField(max_length=1000,null=True)