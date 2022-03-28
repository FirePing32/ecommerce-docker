from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from store.forms import UserForm, UserDetailForm, VendorForm, VendorDetailForm, ItemForm
from django.urls import reverse
from .models import Item, Cart, UserDetail
from django.contrib.auth.models import User

def index(request):
    try:
        account_status = request.user.vendordetail.is_vendor
    except:
        account_status = False

    if request.user.is_authenticated and account_status:
        return redirect('vendorDashboard')
    else:
        store_items = Item.objects.all()
        return render(request, 'store/index.html', {'store_items':store_items})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not found !")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'store/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_detail_form = UserDetailForm(request.POST)
        if user_form.is_valid() and user_detail_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = user_detail_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, user_detail_form.errors)
    else:
        user_form = UserForm()
        user_detail_form = UserDetailForm()
    return render(request,'store/signup.html',
                          {'user_form':user_form,
                           'user_detail_form':user_detail_form,
                           'registered':registered})

def vendorlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        vendor = authenticate(username=username, password=password)
        if vendor:
            if vendor.is_active:
                login(request,vendor)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not found !")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'store/vendor/login.html')

def vendorsignup(request):
    registered = False
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST)
        vendor_detail_form = VendorDetailForm(request.POST)
        if vendor_form.is_valid() and vendor_detail_form.is_valid():
            vendor = vendor_form.save()
            vendor.set_password(vendor.password)
            vendor.save()
            profile = vendor_detail_form.save(commit=False)
            profile.vendor = vendor
            profile.save()
            registered = True
        else:
            print(vendor_form.errors, vendor_detail_form.errors)
    else:
        vendor_form = VendorForm()
        vendor_detail_form = VendorDetailForm()
    return render(request,'store/vendor/signup.html',
                          {'vendor_form':vendor_form,
                           'vendor_detail_form':vendor_detail_form,
                           'registered':registered})

@login_required
def vendorDashboard(request):
    itemcreated = False
    itemdeleted = False
    if request.method == 'POST':
        if 'additem' in request.POST:
            itemform = ItemForm(request.POST)
            if itemform.is_valid():
                item = itemform.save(commit=False)
                item.vendorName = request.user.vendordetail
                item.save()
                itemcreated = True
            else:
                print(itemform.errors)
        elif 'deleteitem' in request.POST:
            store_items = Item.objects.filter(itemname=request.POST.get('dropdown'))
            store_items.delete()
            itemdeleted = True

    itemform = ItemForm()
    storefront = Item.objects.all()
    return render(request, 'store/vendor/dashboard.html',
                            {'item_form':itemform,
                            'itemcreated':itemcreated,
                            'itemdeleted':itemdeleted,
                            'storefront':storefront})

@login_required
def itemView(request, uuid):
    added_to_cart = False
    if request.method == 'POST':
        itemObj = Item.objects.filter(itemno=uuid)
        userObj = request.user
        itemInCart = Cart.objects.filter(user=request.user, item=itemObj[0])
        if itemInCart:
            for item in itemInCart:
                item.quantity = item.quantity + 1
                item.save()
                added_to_cart = True
        else:
            Cart.objects.create(user=userObj, item=itemObj[0], quantity=1)
            added_to_cart = True

    itemobj = Item.objects.filter(itemno=uuid)
    return render(request, 'store/item.html',
                            {'itemobj':itemobj,
                            'added_to_cart':added_to_cart})

def vendorProfile(request, vendor):
    vendorObj = User.objects.filter(username=vendor)
    return render(request, 'store/vendor/profile.html',
                            {'vendorObj':vendorObj})

@login_required
def cart(request):

    checkout = False
    cartItems = Cart.objects.all()
    total = 0
    for item in cartItems:
        total += (item.item.itemprice * item.quantity)
    balance = request.user.userdetail.balance

    if request.method == 'POST':
        userObj = UserDetail.objects.get(user=request.user)
        userObj.balance -= total
        userObj.save()
        Cart.objects.all().delete()
        checkout = True

    return render(request, 'store/cart.html',
                            {'cartItems':cartItems,
                            'total':total,
                            'balance':balance,
                            'checkout':checkout})

@login_required
def userDashboard(request):
    balance_updated = False
    if request.method == 'POST':
        amount = request.POST.get('amount')
        userObj = UserDetail.objects.get(user=request.user)
        userObj.balance += int(amount)
        userObj.save()
        balance_updated = True

    balance = request.user.userdetail.balance
    return render(request, 'store/dashboard.html',
                            {'balance':balance,
                            'balance_updated':balance_updated})