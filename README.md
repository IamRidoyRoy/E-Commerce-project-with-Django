
# Hi, I'm Ridoy! 👋


# E-Commerce Solutions with Django 

This is a full-featured E-Commerce website with cart, pagination, payment gateway, search, rating, review functionality, and so on.


## Installation

  Get Django Ready....

```bash
1. python -m venv venv
2. source venv/Scripts/activate
3. pip install django==3.1
4. pip freeze
5. django-admin startproject pyshop .     
6  python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver
Done!

```
    
## Documentation

[Documentation](https://linktodocumentation)

### My Personal Notes:
```
# NB: Screenshort is not available here!

Inside the project:
*Create a templates folder in main directory 
*Create a static folder in django startproject folder
*Import all html files in Template folder

Static settings: 
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'pyshop/static',
]

1. python manage.py collectstatic

Create New Apps:
1. python manage.py startapp appname
2. python manage.py makemigrations
3. python manage.py migrate

Create admin panel user and pass(super user):
1. python manage.py createsupperuser ( work in CMD)
2. winpty python manage.py createsuperuser (in GIT BASH)


```

```
Create a custom user model:
1.	python manage.py startapp accounts
2.	add ‘accounts’  in settings
3.	INSTALLED_APPS = [
4.	    'django.contrib.admin',
5.	    'django.contrib.auth',
6.	    'django.contrib.contenttypes',
7.	    'django.contrib.sessions',
8.	    'django.contrib.messages',
9.	    'django.contrib.staticfiles',
10.	    'category',
11.	    'accounts',
12.	    
13.	] 


Accounts/models.py  modifications :
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.expressions import F

# Create your models here.

class MyAcccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):
        if not email:
            raise ValueError("Email is invalid")
        if not username:
            raise ValueError('User must have a user name')
        
        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self, first_name, last_name, email, username, password ):
        user = self.create_user(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name

        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user



class Account(AbstractBaseUser):
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    username    = models.CharField(max_length=50, unique= True)
    email = models.EmailField(max_length=100, unique=True)
    phone_num   = models.CharField(max_length=50)

    # Required 
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login  = models.DateTimeField(auto_now_add= True)
    is_admin    = models.BooleanField(default= False)
    is_staff    = models.BooleanField(default= False)
    is_active    = models.BooleanField(default= False)
    is_superadmin    = models.BooleanField(default= False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    object = MyAcccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

accounts/apps.py:
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

accounts/admin.py:
from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

category/models:
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique= True)
    slug = models.CharField(max_length=100, unique= True)
    description = models.TextField(max_length= 225, blank= True)
    cat_image = models.ImageField(upload_to = 'photos/categories', blank = True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name




After modify and code delete sqlite, and last two file from Category& accounts/migrations 

2. python manage.py runserver
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py runserver
6. winpty python manage.py createsuperuser  (inn GIT BAS) 
7. winpty python manage.py changepassword  email id  (if new super user did not work!)










Configuring Django Media File:
It will show the image properly!
 
 

Pyshop/settings.py: 
	# media file configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR /'media'

Pyshop/urls.py : 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name= 'home')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )


 
Done! Now the media file is working properly. 

Automatic slug creation:
	 

Category/models.py:
Add – 
    slug = SlugField(max_length=100, unique= True)

1.	Python manage.py makemigrations
2.	Python manage.py migrate

Category/admin.py:
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

admin.site.register(caregory, CategoryAdmin)

 
Look, now atomically create slug.

Create Store App & Product Model:
1.	Python manage.py startapp mystore
Pyshop/settings: 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'mystore'
    
] 
mystore/models.py:   
from category.models import category
# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique= True)
    slug            = models.SlugField(max_length=200, unique= True)
    description     = models.TextField(max_length=500, blank= True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to = 'photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default= True)
    category        = models.ForeignKey(category, on_delete=models.CASCADE )
    create_date     = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.product_name


mystore/admin.py:
To make automatic slug & list of display - 
from django.contrib import admin
from django.db import models

from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    

admin.site.register(Product, ProductAdmin)


Add Products:
 

Display Products in Homepage:
pyshop/views.py:
from django.shortcuts import render
from mystore.models import Product

def home(request):
    products = Product.objects.all().filter(is_available = True)

    context = {
        'products': products,
    }
    return render(request, 'home.html', context)




home.html:
<div class="row">

    {% for product in products %}

    <div class="col-md-3">
        <div class="card card-product-grid">
            <a href="./product-detail.html" class="img-wrap"> <img src="{{product.images.url}}"> </a>
            <figcaption class="info-wrap">
                <a href="./product-detail.html" class="title">{{product.product_name}}</a>
                <div class="price mt-1">${{ product.price }}</div> <!-- price-wrap.// -->
            </figcaption>
        </div>
    </div> <!-- col.// -->
    {% endfor %}
    
</div> <!-- row.// -->

Here I am modifying the html code with loop and product details 
 
Make Store Page:
*Create a template /mystore/mystore.html
Add – pyshop/urls.py:
from django.urls import path, include

path('mystore/', include('mystore.urls')),

mystore/views.py:
from django.shortcuts import render, get_object_or_404, render, get_list_or_404
from .models import Product
from category.models import Category

# Create your views here.

def mystore(request, category_slug = None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=categories, is_available= True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count' : product_count,
    }

    return render(request, 'mystore/mystore.html', context)


mystore/urls.py:
from django.urls import path
from . import views

urlpatterns = [
    path('', views.mystore, name= 'mystore'),
    path('<slug:category_slug>/', views.mystore, name= 'products_by_category'),
]


Template/mystore/mystore.html:
{% extends 'base.html' %}

{% load static %}
{% block content %}
<!— Content --!>

{% endblock %

And then modify all code:
{% extends 'base.html' %}

{% load static %}
{% block content %}

<!-- ========================= SECTION PAGETOP ========================= -->
    <section class="section-pagetop bg">
    <div class="container">
        <h2 class="title-page">Our Store</h2>
        
    </div> <!-- container //  -->
    </section>
    <!-- ========================= SECTION INTRO END// ========================= -->


<!-- ========================= SECTION CONTENT ========================= -->
<section class="section-content padding-y">
    <div class="container">
    
    <div class="row">
        <aside class="col-md-3">
            
    <div class="card">
        <article class="filter-group">
            <header class="card-header">
                <a href="#" data-toggle="collapse" data-target="#collapse_1" aria-expanded="true" class="">
                    <i class="icon-control fa fa-chevron-down"></i>
                    <h6 class="title">Categories</h6>
                </a>
            </header>
            <div class="filter-content collapse show" id="collapse_1" >
                <div class="card-body">
                    
                    <ul class="list-menu">
                    <li><a href="#">People  </a></li>
                    <li><a href="#">Watches </a></li>
                    <li><a href="#">Cinema  </a></li>
                    <li><a href="#">Clothes  </a></li>
                    <li><a href="#">Home items </a></li>
                    <li><a href="#">Animals</a></li>
                    <li><a href="#">People </a></li>
                    </ul>
    
                </div> <!-- card-body.// -->
            </div>
        </article> <!-- filter-group  .// -->
        <article class="filter-group">
            <header class="card-header">
                <a href="#" data-toggle="collapse" data-target="#collapse_4" aria-expanded="true" class="">
                    <i class="icon-control fa fa-chevron-down"></i>
                    <h6 class="title">Sizes </h6>
                </a>
            </header>
            <div class="filter-content collapse show" id="collapse_4" >
                <div class="card-body">
                  <label class="checkbox-btn">
                    <input type="checkbox">
                    <span class="btn btn-light"> XS </span>
                  </label>
    
                  <label class="checkbox-btn">
                    <input type="checkbox">
                    <span class="btn btn-light"> SM </span>
                  </label>
    
                  <label class="checkbox-btn">
                    <input type="checkbox">
                    <span class="btn btn-light"> LG </span>
                  </label>
    
                  <label class="checkbox-btn">
                    <input type="checkbox">
                    <span class="btn btn-light"> XXL </span>
                  </label>
            </div><!-- card-body.// -->
            </div>
        </article> <!-- filter-group .// -->
        
        <article class="filter-group">
            <header class="card-header">
                <a href="#" data-toggle="collapse" data-target="#collapse_3" aria-expanded="true" class="">
                    <i class="icon-control fa fa-chevron-down"></i>
                    <h6 class="title">Price range </h6>
                </a>
            </header>
            <div class="filter-content collapse show" id="collapse_3" >
                <div class="card-body">
                    
                    <div class="form-row">
                    <div class="form-group col-md-6">
                      <label>Min</label>
                      <!-- <input class="form-control" placeholder="$0" type="number"> -->
                          <select class="mr-2 form-control">
                            <option value="0">$0</option>
                            <option value="50">$50</option>
                            <option value="100">$100</option>
                            <option value="150">$150</option>
                            <option value="200">$200</option>
                            <option value="500">$500</option>
                            <option value="1000">$1000</option>
                        </select>
                    </div>
                    <div class="form-group text-right col-md-6">
                      <label>Max</label>
                          <select class="mr-2 form-control">
                            <option value="50">$50</option>
                            <option value="100">$100</option>
                            <option value="150">$150</option>
                            <option value="200">$200</option>
                            <option value="500">$500</option>
                            <option value="1000">$1000</option>
                            <option value="2000">$2000+</option>
                        </select>
                    </div>
                    </div> <!-- form-row.// -->
                    <button class="btn btn-block btn-primary">Apply</button>
                </div><!-- card-body.// -->
            </div>
        </article> <!-- filter-group .// -->
        
    </div> <!-- card.// -->
    
        </aside> <!-- col.// -->
        <main class="col-md-9">
    
    <header class="border-bottom mb-4 pb-3">
            <div class="form-inline">
                <span class="mr-md-auto"><b>{{product_count}}</b> Items found </span>
                
            </div>
    </header><!-- sect-heading -->
    
<div class="row">
    {% for product in products %}
        <div class="col-md-4">
            <figure class="card card-product-grid">
                <div class="img-wrap"> 
                    
                    <img src="{{product.images.url}}">
                    
                </div> <!-- img-wrap.// -->
                <figcaption class="info-wrap">
                    <div class="fix-height">
                        <a href="./product-detail.html" class="title">{{ product.product_name }}</a>
                        <div class="price-wrap mt-2">
                            <span class="price">${{ product.price }}</span>
                            <!-- <del class="price-old">$1980</del> -->
                        </div> <!-- price-wrap.// -->
                    </div>
                    <a href="#" class="btn btn-block btn-primary">Add to cart </a>
                </figcaption>
            </figure>
        </div> <!-- col.// -->
    {% endfor %}
    
</div> <!-- row end.// -->
    
    
    <nav class="mt-4" aria-label="Page navigation sample">
      <ul class="pagination">
        <li class="page-item disabled"><a class="page-link" href="#">Previous</a></li>
        <li class="page-item active"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item"><a class="page-link" href="#">Next</a></li>
      </ul>
    </nav>
    
        </main> <!-- col.// -->
    
    </div>
    
    </div> <!-- container .//  -->
    </section>
    <!-- ========================= SECTION CONTENT END// ========================= -->
    

{% endblock %}

Now I am able to do like…
 







When search for only shirt:
 

Now product is display by category!

Make Context Processors for Displaying Categories on Navbar:
At first I create a file – 
category/context_processor.py
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links) 

pyshop/settings.py: add in context processor-
'category.context_processor.menu_links',
Category/models.py:  add
  def get_url(self):
        return reverse('products_by_category', args=[self.slug] )

 

Now navbar category works properly.
Side Category in store page:
Templates/mystore/mystore.html :
<li><a href="{% url 'mystore' %}">All Products</a></li>

                    {% for category in links %}
                    <li><a href="{{ category.get_url }}">{{ category.category_name }}</a></li>
                    {% endfor %}


Implement Product Detail Url and Design:
Mystore/urls.py: add
    path('<slug:category_slug>/<slug:product_slug>', views.product_detail, name= 'product_detail'),


mystore/views.py: add
def product_detail(request, category_slug, product_slug):
    return render(request, 'mystore/product_detail.html')

And after modifying – product_detail.html  page:
 




Single product view details:
Mystore/views.py:
def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
    }

    return render(request, 'mystore/product_detail.html', context)

 
And after modifying – product_detail.html  page.

Get url for every single product:
Mystore/models.py: add-
def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

pyshop/home.html:  replace (/product_detail.html)
{{ product.get_url }}

 

Show out of stock:
Template/mystore/product_detail.html: Add
{% if single_product.stock == 0 %}
        <h2>Sorry! Out of stock<h2></h2>
        {% else %}

            <a href="./product-detail.html" class="btn  btn-primary"> <span class="text">Add to cart</span> <i class="fas fa-shopping-cart"></i>  </a>

    {% endif %}

 

Push all code to Github:
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/IamRidoyRoy/new-shop.git
git push -u origin main










Create Cart app & Functionality:

1.	Python manage.py startapp carts
Pyshop/settings.py: add - carts
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'mystore',
    'carts'
    
] 

Pyshop/urls.py: add path
    path('cart/', include('carts.urls')),

carts/urls.py: create it .
from django.urls import path
from .import views

urlpatterns =[

    path('', views.cart, name= 'cart')

]

carts/views.py:
def cart(request):
    return render(request, 'mystore/cart.html')


templates/mystore/cart.html:
{% extends 'base.html' %}

{% load static %}

{% block content %}

{% endblock %}
And work on content part.

Now we are going to create a model for cart:
Carts/models.py:
from django.db import models
from django.db.models.fields.related import ForeignKey

from mystore.models import Product

# Create your models here.

class Cart(models.Model):
    cart_id     = models.CharField(max_length=300, blank=True)
    date_added  = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product     = models.ForeignKey(Product, on_delete = models.CASCADE)
    cart        = models.ForeignKey(Cart, on_delete = models.CASCADE )
    quantity    = models.IntegerField()
    is_active   = models.BooleanField(default = True)

    def __str__(self):
        return self.product




carts/admin.py:
from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)

1.	Python manage.py makemigrations
2.	Python manage.py migrate 
3.	Python manage.py runserver
 
So, now we have carts functionality in admin panel. 

 


Add to Cart Functionality without Logging-in and with Session Key:
Carts/views.py:
from django.shortcuts import redirect, render
from carts.models import CartItem, Cart

from mystore.models import Product

# Create your views here.

def cart(request):
    return render(request, 'mystore/cart.html')

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id) # By using it we get the product.
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request) ) # get cart using cart id in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product = product, cart= cart)
        cart_item.quantity += 1 #cart quantuty will incremet by one
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    return redirect('cart')




carts/urls.py:
    path('ad_cart/<int:product_id>/', views.add_cart, name = 'add_cart'),


product_detail.html:
            <a href="{% url 'add_cart' single_product.id %}" class="btn  btn-primary"> <span class="text">Add to cart</span> <i class="fas fa-shopping-cart"></i>  </a>


 
Now , if we  click add to cart button, it go checkout page but not added item!

Cart View for Getting Cart Items, Total & Quantity:
Carts/views.py: add-
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import CartItem, Cart

from mystore.models import Product

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id) # By using it we get the product.
    try:
        cart = Cart.objects.get(cart_id= _cart_id(request) ) # get cart using cart id in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product = product, cart= cart)
        cart_item.quantity += 1 #cart quantuty will incremet by one
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')

def remove_cart(request, product_id ):
    cart    = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id ):
    cart    = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None, tax=0, grand_total=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price* cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2*total)/100
        grand_total = total + tax
    except :
        pass

    context ={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total,
    }  
    
    return render(request, 'mystore/cart.html', context)

carts/models.py: add-
def sub_total(self):
        return self.product.price *self.quantity


Template/mystore/cart.py:
{% extends 'base.html' %}

{% load static %}

{% block content %}

<section class="section-content padding-y bg">
    <div class="container">
    
    <!-- ============================ COMPONENT 1 ================================= -->
    {% if not cart_items %}
        <h2 class="text-center" >Your shopping cart is empty!</h2>
        <br>
        <div class="text-center">
            <a href="{% url 'mystore' %}" class="btn btn-primary">Continue Shopping</a>

        </div>

    {% else %}
    <div class="row">
        <aside class="col-lg-9">
    <div class="card">
    <table class="table table-borderless table-shopping-cart">
    <thead class="text-muted">
    <tr class="small text-uppercase">
      <th scope="col">Product</th>
      <th scope="col" width="120">Quantity</th>
      <th scope="col" width="120">Price</th>
      <th scope="col" class="text-right" width="200"> </th>
    </tr>
    </thead>
    <tbody>

{% for cart_item in cart_items %}   

    <tr>
        <td>
            <figure class="itemside align-items-center">
                <div class="aside"><img src="{{ cart_item.product.images.url }}" class="img-sm"></div>
                <figcaption class="info">
                    <a href="#" class="title text-dark">{{ cart_item.product.product_name }}t</a>
                    <p class="text-muted small">Matrix: 25 Mpx <br> Brand: Canon</p>
                </figcaption>
            </figure>
        </td>
        <td> 
        
            <!-- col.// -->
                        <div class="col"> 
                            <div class="input-group input-spinner">
                                <div class="input-group-prepend">
                                <a href="{% url 'remove_cart' cart_item.product.id %}" class="btn btn-light" type="button" id="button-plus"> <i class="fa fa-minus"></i> </a>
                                </div>
                                <input type="text" class="form-control"  value="{{ cart_item.quantity }}">
                                <div class="input-group-append">
                                <a href="{% url 'add_cart' cart_item.product.id %}" class="btn btn-light" type="button" id="button-minus"> <i class="fa fa-plus"></i> </a>
                                </div>
                            </div> <!-- input-group.// -->
                        </div> <!-- col.// -->
        </td>
        <td> 
            <div class="price-wrap"> 
                <var class="price">${{ cart_item.sub_total }}</var> 
                <small class="text-muted"> ${{ cart_item.product.price }} each </small> 
            </div> <!-- price-wrap .// -->
        </td>
        <td class="text-right"> 
        <a href="{% url 'remove_cart_item' cart_item.product.id %}" class="btn btn-danger"> Remove</a>
        </td>
    </tr>
    
{% endfor %}
    </tbody>
    </table>
    </div> <!-- card.// -->
    
        </aside> <!-- col.// -->
        <aside class="col-lg-3">
    
            <div class="card">
            <div class="card-body">
                <dl class="dlist-align">
                  <dt>Total price:</dt>
                  <dd class="text-right">${{ total }}</dd>
                </dl>
                <dl class="dlist-align">
                  <dt>Tax:</dt>
                  <dd class="text-right"> ${{ tax }}</dd>
                </dl>
                <dl class="dlist-align">
                  <dt>Grand Total:</dt>
                  <dd class="text-right text-dark b"><strong>${{ grand_total }}</strong></dd>
                </dl>
                <hr>
                <p class="text-center mb-3">
                    <img src="{% static './images/misc/payments.png' %}" height="26">
                </p>
                <a href="./place-order.html" class="btn btn-primary btn-block"> Checkout </a>
                <a href="./store.html" class="btn btn-light btn-block">Continue Shopping</a>
            </div> <!-- card-body.// -->
            </div> <!-- card.// -->
    
    </aside> <!-- col.// -->
    
    
    </div> <!-- row.// -->

    {% endif %}
    <!-- ============================ COMPONENT 1 END .// ================================= -->
    
    </div> <!-- container .//  -->
    </section>
    <!-- ========================= SECTION CONTENT END// ========================= -->

{% endblock %}
Modify  the functionality in cart.htmk file.


Now we able to see cart are working properly.  

	

Fix Add to Cart Links:
Mystore/mystore.html: add- herf
                    <a href="{% url 'add_cart' product.id %}" class="btn btn-block btn-primary">Add to cart </a>
  
Now, we can add to cart and add product to our checkout page. But if I click on any product it will not show details. And add link for “continue shopping”.
Cart.html: add a link :
href="{{ cart_item.product.get_url }}"
href="{% url 'mystore' %}

 
Now, if I click on any product it will go this page. And continue shopping will go to cart page.






Check If the Product Added to the Cart:
Mystore/views.py: add 
from carts.views import _cart_id

in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product=single_product).exists()

add to dictionary:  in_cart
context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
    }

Product_detail.html:
{% if single_product.stock == 0 %}
        <h2>Sorry! Out of stock. <small>Check it latter</small></h2> 
        {% else %}
          {% if in_cart %}
            <!-- added to cart  -->
            <a href="#" class="btn  btn-success"> <span class="text">Added to Cart</span> <i class="fas fa-check"></i>  </a>
            <a href="{% url 'cart' %}" class="btn  btn-outline-primary"> <span class="text">View Cart</span> <i class="fas fa-eye"></i>  </a>

            {% else %}
              <a href="{% url 'add_cart' single_product.id %}" class="btn  btn-primary"> <span class="text">Add to Cart</span> <i class="fas fa-shopping-cart"></i>  </a>
          {% endif %}
    {% endif %}

 

Now we will see added product & View Cart - - if it was added before.

Counter Context Processor for Cart Icon in Navbar:
Create a new file in ‘carts’ – context_processor.py
from .models import Cart, CartItem
from .views import _cart_id, cart

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return{}
    else:
        try:
            cart = Cart.objects.filter(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count = cart_count)

settings.py : add in template
                'carts.context_processor.counter',

Navbar.html:
href="{% url 'cart' %}

{{ cart_count }}

 
Now it is showing that two product in cart dynamically. 


Changes add to cart -> view details in store page:
Mystore.html:
                                <a href="{{ product.get_url }}" class="btn btn-block btn-primary">View Details</a>

Now if we go in store page and click on view details, It will show details of the product and we can add to cart if the product is available.

Add Paginator :
This is a process that we can go next page.
Mystore/views.py: add-
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

paginate = Paginator(products, 6)
page = request.GET.get('page')
paged_product = paginate.get_page(page)

context = {
        'products': paged_product,
        'product_count' : product_count,
    }

Now we can see only 6 product in store page. But if we click on category it will shows an error!
 
To skip error:
if category_slug != None:
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category=categories, is_available= True)
        paginate = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginate.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginate = Paginator(products, 6)
        page = request.GET.get('page')
        paged_product = paginate.get_page(page)
        product_count = products.count()

I copy and paste the same 3 line code in if block now we will not get any error.


Mystore.html:
Now I am going to fix next & previous button in store page-
{% if products.has_other_pages %}
                    <ul class="pagination">
                        {% if products.has_previous %}
                            <li class="page-item-active "><a class="page-link"
                                href="?page={{ products.previous_page_number }}">Previous</a></li>
                        {% else %}
                            <li class="page-item disabled"><a class="page-link" href="#">Previous</a></li>
                        {% endif %}

                        {% for i in products.paginator.page_range %}
                            {% if products.number == i %}
                                <li class="page-item"><a class="page-link" href="#">{{i}}</a></li>
                            {% else %}
                                <li class="page-item"><a class="page-link" href="?page={{i}}">{{i}}</a></li>
                            {% endif %}
                        {% endfor %}

                        {% if products.has_next %}
                            <li class="page-item "><a class="page-link" href="?page={{ products.next_page_number }}">Next</a></li>
                        {% else %}
                            <li class="page-item disabled"><a class="page-link" href="#">Next</a></li>
                        {% endif %}
                                
                    </ul>
                    {% endif %}
Now if have two page the next button will show active else show disabled & work properly.
Fix Error:
Mystore/views.py: add in else block
.order_by('id')

tax = 0
        grand_total = 0


Search Functionality:
Mystore/urls.py: add path
    path('search/', views.search, name="search"),


add category/  to make it meaningful :
path('category/<slug:category_slug>/', views.mystore, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>',
         views.product_detail, name='product_detail'),

mystore/views.py:  define a function for search
def search(request):
    return render(request, 'mystore/mystore.html')

 


navbar.html: 
add url & method 
            <form action="{% url 'search' %}" class="search" method="GET" >

Add name = “keyword”
                    <input type="text" class="form-control" style="width:60%;" placeholder="Search" name="keyword">


Mystore/views.py:
Now we set search for description-
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('create_date').filter(description__icontains=keyword)
    context = { 
        'products' : products, 
    }    
    return render(request, 'mystore/mystore.html', context)

•	 Here we find keyword in get request it will store the value in keyword.
•	Then search by description of all product
 
Here I just search for a shirt and get it as it match with its descriptions.

Mystore/views.py:
Add search option for title but we can’t directly add or sign so that we have to add Q .
from django.db.models import Q 

            products = Product.objects.order_by('create_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))





Now showing three shirts and the query is working fine but item found is not showing properly.
 


Mystore/views.py:
If we want to product count – add count() and pass it context dictionary .
product_count = products.count()

    context = { 
        'products' : products, 
        'product_count': product_count,
    }    

Now it will show – 3 items found. 
 


Now one problem – when we search any product it should show Search result not our store!

Mystore.html:
{% if 'search' in request.path %}
        <h2 class="title-page">Search result</h2>
    {% else %}
        <h2 class="title-page">Our Store</h2>  
    {% endif %} 





Now it will shows search result- when search something 
 


If no result found it should show no result found:
Mystore.html:
Just if condition added-
{% if products %}
                <div class="row">
                    {% for product in products %}
                    <div class="col-md-4">
                        <figure class="card card-product-grid">
                            <div class="img-wrap">

                                <a href="{{ product.get_url }}"><img src="{{product.images.url}}"></a>

                            </div> <!-- img-wrap.// -->
                            <figcaption class="info-wrap">
                                <div class="fix-height">
                                    <a href="{{ product.get_url }}" class="title">{{ product.product_name }}</a>
                                    <div class="price-wrap mt-2">
                                        <span class="price">${{ product.price }}</span>
                                        <!-- <del class="price-old">$1980</del> -->
                                    </div> <!-- price-wrap.// -->
                                </div>
                                <a href="{{ product.get_url }}" class="btn btn-block btn-primary">View Details</a>
                            </figcaption>
                        </figure>
                    </div> <!-- col.// -->
                    {% endfor %}

                </div> <!-- row end.// -->
                {% else %}
                    <div>
                        <h1>No result found! Please try again.</h1>
                    </div>
                {% endif %}








```

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://katherinempeterson.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/)

