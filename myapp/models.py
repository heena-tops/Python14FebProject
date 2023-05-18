from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	pswd=models.CharField(max_length=100)
	contact=models.IntegerField()
	address=models.TextField()
	usertype=models.CharField(default="user",max_length=100)

	def __str__(self):
		return self.fname+" "+self.lname

class Category(models.Model):

	name=models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Product(models.Model):

	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	category=models.ForeignKey(Category,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=100)
	product_price=models.IntegerField()
	product_qty=models.IntegerField()
	product_desc=models.TextField()
	product_image=models.ImageField(upload_to='media/images')

	def __str__(self):
		return self.product_name+" - "+self.seller.fname

class Wishlist(models.Model):

	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.product.product_name

class Cart(models.Model):

	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	payment=models.BooleanField(default=False)
	product_price=models.IntegerField()
	product_qty=models.IntegerField(default=1)
	total=models.IntegerField()
	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
	def __str__(self):
		return self.product.product_name

class Transaction(models.Model):

	user=models.ForeignKey(User,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)