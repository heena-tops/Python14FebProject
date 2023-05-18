from django.shortcuts import render,redirect
from .models import User,Category,Product,Wishlist,Cart,Transaction
from django.conf import settings
from django.core.mail import send_mail
import random
import razorpay
from django.http import JsonResponse

# Create your views here.

def form_validation(request):
	email=request.GET.get('email')
	print(">>>>>>>>>>>>>>>>AJAX DATA : ",email)
	data={'is_taken':User.objects.filter(email__iexact=email).exists()}

	return JsonResponse(data)

def index(request):
	product=Product.objects.all()
	return render(request,'index.html',{'product':product})

def product(request):
	product=Product.objects.all()
	return render(request,'products.html',{'product':product})

def seller_index(request):
	return render(request,'seller_index.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg1="Email Already Exist !!!"
			return render(request,'signup.html',{'msg1':msg1})
		except:
			User.objects.create(
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				pswd=request.POST['pswd'],
				contact=request.POST['contact'],
				address=request.POST['address'],
				usertype=request.POST['usertype'],
				)
			msg="Registration Successfull"
		return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],pswd=request.POST['pswd'])
			wishlist=Wishlist.objects.filter(user=user)
			cart=Cart.objects.filter(user=user)
			if user.usertype=="seller":
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'seller_index.html')

			else:
				request.session['wishlist_count']=len(wishlist)
				request.session['cart_count']=len(cart)
				request.session['email']=user.email
				request.session['fname']=user.fname
				print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>COUNT OF WISHLIST : ",request.session['wishlist_count'])
				return render(request,'index.html')
		except:
			msg="Username or Password Does not Matched!!!"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try :
		del request.session['email']
		del request.session['fname']
		del request.session['wishlist_count']
		del request.session['cart_count']
		return render(request,'login.html')
	except:
		msg="Something went Wrong, Try Again !!!"
		return render(request,'login.html',{'msg':msg})

def change_pswd(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.session['email'])
			if user.pswd==request.POST['pswd']:
				if request.POST['n_pswd']==request.POST['cn_pswd']:
					user.pswd=request.POST['n_pswd']
					user.save()
					return redirect('logout')
				else:
					msg="New Password & Confirm Password Does not Matched !!!"
					return render(request,'change_pswd.html',{'msg':msg})
			else:	
				msg="Old Password Does not Matched !!!"
				return render(request,'change_pswd.html',{'msg':msg})
		except:
			msg = "Soemthing went Wrong !!!"
			return render(request,'change_pswd.html',{'msg':msg})
	else:
		return render(request,'change_pswd.html')

def forgot_pswd(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			subject = 'OTP for forgot Password'
			otp=random.randint(1000,9999)
			message = f'Hi {user.fname}, Your OTP : '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email,]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'verify_otp.html',{'email':user.email,'otp':otp})
		except:
			msg="No Such User Exist !!!"
			return render(request,'forgot_pswd.html',{'msg':msg})
	else:
		return render(request,'forgot_pswd.html')

def verify_otp(request):
	if request.method=="POST":
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		print(">>>>>>>>OTP : ",otp)
		print(">>>>>>>>UOTP : ",uotp)
		print(">>>>>>>>Email : ",email)
		if uotp==otp:
			return render(request,'create_pswd.html',{'email':email})
		else:
			msg="OTP Does not Matched !!!"
			return render(request,'verify_otp.html',{'msg':msg})
	else:
		return render(request,'verify_otp.html')

def create_pswd(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if request.POST['n_pswd']==request.POST['cn_pswd']:
				user.pswd=request.POST['n_pswd']
				user.save()
				return redirect('login')
			else:
				msg="New Password & Confirm Password Does not Matched !!"
				return render(request,'create_pswd.html',{'msg':msg})
		except:
			msg="User Not Exist !!!"
			return render(request,'create_pswd.html',{'msg':msg})
	else:
		return render(request,'create_pswd.html')

def seller_change_pswd(request):
	if request.method=="POST":
		try:
			seller=User.objects.get(email=request.session['email'])
			if seller.pswd==request.POST['pswd']:
				if request.POST['n_pswd']==request.POST['cn_pswd']:
					seller.pswd=request.POST['n_pswd']
					seller.save()
					return redirect('logout')
				else:
					msg="New Password & Confirm Password Does not Matched !!!"
					return render(request,'seller_change_pswd.html',{'msg':msg})
			else:	
				msg="Old Password Does not Matched !!!"
				return render(request,'seller_change_pswd.html',{'msg':msg})
		except:
			msg = "Soemthing went Wrong !!!"
			return render(request,'seller_change_pswd.html',{'msg':msg})
	else:
		return render(request,'seller_change_pswd.html')

def seller_add_product(request):
	category=Category.objects.all()
	seller=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		Product.objects.create(
				seller=seller,
				category=Category.objects.get(name=request.POST['category']),
				product_name=request.POST['product_name'],
				product_price=request.POST['product_price'],
				product_qty=request.POST['product_qty'],
				product_desc=request.POST['product_desc'],
				product_image=request.FILES['product_image']
			)
		msg="Product Added.........."
		return render(request,'seller_add_product.html',{'cat':category,'msg':msg})

	else:
		return render(request,'seller_add_product.html',{'cat':category})

def myproduct(request):
	seller=User.objects.get(email=request.session['email'])
	product=Product.objects.filter(seller=seller)

	return render(request,'myproduct.html',{'product':product})


def seller_product_edit(request,pk):
	category=Category.objects.all()
	seller=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)

	if request.method=="POST":
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_qty=request.POST['product_qty']
		product.product_desc=request.POST['product_desc']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		return render(request,'seller_product_edit.html',{'product':product,'cat':category})
	else:
		return render(request,'seller_product_edit.html',{'product':product,'cat':category})

def seller_product_delete(request,pk):
	seller=User.objects.get(email=request.session['email'])
	product=Product.objects.get(seller=seller,pk=pk)

	product.delete()

	return redirect('myproduct')

def product_details(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	try:
		wishlist=Wishlist.objects.get(user=user,product=product)
		if wishlist:
			wishlist_flag=True
	except:
		pass
	try:
		cart=Cart.objects.get(user=user,product=product)
		if cart:
			cart_flag=True
	except:
		pass
	return render(request,'product_details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def wishlist(request):
	try:
		user=User.objects.get(email=request.session['email'])
		wishlist=Wishlist.objects.filter(user=user)
		request.session['wishlist_count']=len(wishlist)
		
		return render(request,'wishlist.html',{'wishlist':wishlist})
	except:
		return render(request,'wishlist.html')

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	try:
		user=User.objects.get(email=request.session['email'])
		wishlist=Wishlist.objects.create(
			user=user,
			product=product
			)
		return redirect('wishlist')
	except:
		return render(request,'wishlist.html')

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment=False)
	for i in cart:
			net_price+=i.product_price
	request.session['cart_count']=len(cart)
	try:
		client = razorpay.Client(auth = (settings.KEY_ID,settings.KEY_SECRET))
		payments=client.order.create({'amount':net_price*100, 'currency':'INR','payment_capture':1})
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		print(payments)
		print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		cart.razorpay_order_id=payments['id']
		for i in cart:
			i.save()
		return render(request,'cart.html',{'cart':cart,'net_price':net_price,'payments':payments})
	except:
		return render(request,'cart.html',{'cart':cart,'net_price':net_price})

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	try:
		user=User.objects.get(email=request.session['email'])
		cart=Cart.objects.create(
			user=user,
			product=product,
			product_qty=1,
			product_price=product.product_price,
			total=0,
			)
		return redirect('cart')
	except:
		return render(request,'cart.html')

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')

def change_qty(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product)
	cart.product_qty=int(request.POST['qty'])
	cart.product_price=product.product_price*cart.product_qty
	cart.save()
	return redirect('cart')


def search(request):
	if request.method=="POST":
		search=request.POST['search_item']
		if request.POST['search_item'].__contains__(search):
			product=Product.objects.filter(product_name=search)
			return render(request,'products.html',{'product':product})
		else:
			msg="No such Product Found ..."
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MSG1",msg)
			return render(request,'products.html',{'msg':msg})
	else:
		return render(request,'index.html')

def success(request):
	order_id=request.GET.get('order_id')
	cart=Cart.objects.filter(razorpay_order_id=order_id)
	user=User.objects.get(email=request.session['email'])
	t = Transaction.objects.create(user=user)
	for i in cart:
		i.payment=True
		i.save()
	msg="Payment Successfull ...."
	cart.delete()
	return render(request,'callback.html',{'msg':msg})

def tarnsaction(request):
	user=User.objects.get(email=request.session['email'])
	t = Transaction.objects.filter(user=user)
	print(">>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	print(user.fname)
	print(">>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	return render(request,'Transaction_history.html',{'t':t,'user':user})

#.create() : will create new data objects 
#Syntax : model_name.objects.create()

#.get() : to retrive single object from data table with a codnition(select * from table_name where condition)
# Syntax : model_name.objects.get(codnition)

# .all() : to retrive QuerySet from database
# Syntax : model_name.objects.all()

# .filter() : to retrive all QuerySet with condition
# Syntax : model_name.objects.filter(condition)

#session : A time span between user login and logout