from django.db import models

# Create your models here.

class Registration(models.Model):
    fname=models.CharField(max_length=30)
    lname=models.CharField(max_length=10)
    email=models.EmailField(max_length=50)
    contact=models.BigIntegerField()
    password=models.CharField(max_length=20)
    address=models.CharField(max_length=100)



class Hotels(models.Model):
    name=models.CharField(max_length=20)
    dateopen=models.DateField()
    address=models.CharField(max_length=100)
    image=models.ImageField()
    lic=models.BigIntegerField()
    contact=models.BigIntegerField()
    email=models.EmailField(max_length=50,null=True)
    rating=models.IntegerField(null=True)
    realrat=models.CharField(max_length=20,null=True)


class Request(models.Model):
    request=models.CharField(max_length=20)
    user=models.ForeignKey(Registration,on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotels,on_delete=models.CASCADE,null=True)


class Review(models.Model):
    hotelname=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    uname=models.ForeignKey(Registration, on_delete=models.CASCADE)
    review=models.CharField(max_length=200)
    dateofreview=models.DateField(auto_now_add=True)
    

# class Rating(models.Model):
#     hotelname=models.ForeignKey(Hotels, on_delete=models.CASCADE)
#     rating1=models.IntegerField()

class Dish(models.Model):
    dishname=models.CharField(max_length=20)
    hotelname=models.ForeignKey(Hotels, on_delete=models.CASCADE)
    price=models.IntegerField(null=True)
    image=models.ImageField(null=True)
    
