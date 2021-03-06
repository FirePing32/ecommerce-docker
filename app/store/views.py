from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from store.forms import UserForm, UserDetailForm, VendorForm, VendorDetailForm, ItemForm
from django.urls import reverse
from .models import Item, Cart, UserDetail, Reviews, UserOrders, VendorDetail, WishList
from django.contrib.auth.models import User
import csv
import logging

logger = logging.getLogger(__name__)

def index(request):
    try:
        account_status = request.user.vendordetail.is_vendor
        logger.info('CHECKING VENDOR STATUS')
    except:
        account_status = False

    if request.user.is_authenticated:
        try:
            if User.objects.filter(username=request.user.username)[0].userdetail:
                logger.info(f'USER_DETAILS ALREADY EXIST: USERNAME={request.user.username}')
                pass
        except:
            UserDetail.objects.create(user=request.user, address="", balance=0)
            logger.info(f'USER_DETAILS MODEL CREATED FOR USERNAME: {request.user.username}')

    if request.user.is_authenticated and account_status:
        return redirect('vendorDashboard')
    else:
        store_items = Item.objects.all()
        return render(request, 'store/index.html', {'store_items':store_items})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.info(f'USER LOGIN: USERNAME={username}')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                logger.info(f'USER "{username}" SUCCESSFULLY LOGGED IN')
                return HttpResponseRedirect(reverse('index'))
            else:
                logger.error(f'INVALID CREDENTIALS FOR USERNAME: {username}')
                return HttpResponse("Account not found !")
        else:
            logger.error(f'INVALID CREDENTIALS FOR USERNAME: {username}')
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'store/login.html')

@login_required
def user_logout(request):
    logger.info(f'USER LOGOUT SUCCESSFUL FOR USERNAME: {request.user.username}')
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
            logger.info(f'NEW USER SIGNUP SUCCESSFUL: {user_form.cleaned_data} {user_detail_form.cleaned_data}')
        else:
            logger.error(f'{user_form.errors} {user_detail_form.errors}')
    else:
        user_form = UserForm()
        user_detail_form = UserDetailForm()
    return render(request,'store/signup.html',
                          {'user_form':user_form,
                           'user_detail_form':user_detail_form,
                           'registered':registered})

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
            logger.info(f'NEW VENDOR SIGNUP SUCCESSFUL: {vendor_form.cleaned_data} {vendor_detail_form.cleaned_data}')
        else:
            logger.error('{vendor_form.errors} {vendor_detail_form.errors}')
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
            itemform = ItemForm(request.POST, request.FILES)
            if itemform.is_valid():
                item = itemform.save(commit=False)
                item.vendorName = request.user.vendordetail
                item.itemimg = request.FILES['itemimg']
                item.save()
                itemcreated = True
                logger.info(f'VENDOR ITEM CREATED: {itemform.cleaned_data}')
            else:
                logger.error(itemform.errors)
        elif 'deleteitem' in request.POST:
            store_items = Item.objects.filter(itemname=request.POST.get('dropdown'))
            logger.info(f'VENDOR ITEM DELETED: {store_items[0]}')
            store_items.delete()
            itemdeleted = True

    itemform = ItemForm()
    storefront = Item.objects.all()

    vendorObj = User.objects.get(email=request.user.email)
    items = Item.objects.filter(vendorName=vendorObj.vendordetail)

    return render(request, 'store/vendor/dashboard.html',
                            {'item_form':itemform,
                            'itemcreated':itemcreated,
                            'itemdeleted':itemdeleted,
                            'storefront':storefront,
                            'itemsList':items})

@login_required
def export_csv(request):
    vendorObj = User.objects.filter(username=request.user)
    items = Item.objects.filter(vendorName=vendorObj[0].vendordetail)
    vendorItems = items.values_list('itemname', 'itemdesc', 'itemprice', 'orders')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Item Description', 'Item Price', 'Orders'])

    for item in vendorItems:
        writer.writerow(item)

    logger.info(f'VENDOR ITEM CSV FILE CREATED: {vendorItems}')
    return response

@login_required
def itemView(request, uuid):
    added_to_cart = False
    added_to_wishlist = False
    already_in_wishlist = False
    review_submitted = False
    exists = False
    if request.method == 'POST':
        if 'addToCart' in request.POST:
            itemObj = Item.objects.filter(itemno=uuid)
            userObj = request.user
            itemInCart = Cart.objects.filter(user_id=request.user.id, item_id=itemObj[0].id)
            if itemInCart.exists():
                for item in itemInCart:
                    item.quantity += 1
                    item.save()
                    added_to_cart = True
                    logger.info(f'ITEM QUANTITY UPDATED FOR: {itemInCart}')
            else:
                Cart.objects.create(user_id=userObj.id, item_id=itemObj[0].id, quantity=1)
                added_to_cart = True
                logger.info(f'ITEM ADDED TO CART: {itemObj[0]}')

        elif 'addToWishlist' in request.POST:
            item = Item.objects.get(itemno=uuid)
            iteminlist = WishList.objects.filter(user_id=request.user.id, item_id=item.id).exists()

            if iteminlist:
                already_in_wishlist = True
                logger.info(f'ITEM ALREADY IN WISHLIST: {item}')
            else:
                WishList.objects.create(user_id=request.user.id, item_id=item.id)
                added_to_wishlist = True
                logger.info(f'ITEM ADDED TO WISHLIST: {item}')

        elif 'review' in request.POST:
            review = request.POST.get('review')
            item_obj = Item.objects.get(itemno=uuid)
            exists = Reviews.objects.filter(user_id=request.user.id, item_id=item_obj.id).exists()
            if exists:
                review_submitted = False
                logger.info('REVIEW ALREADY EXISTS')
            else:
                Reviews.objects.create(user=request.user, item=item_obj, review=review)
                review_submitted = True
                logger.info('REVIEW SUBMITTED')

    itemobj = Item.objects.filter(itemno=uuid)
    reviews = Reviews.objects.filter(item=itemobj[0])
    return render(request, 'store/item.html',
                            {'itemobj':itemobj,
                            'added_to_cart':added_to_cart,
                            'added_to_wishlist':added_to_wishlist,
                            'already_in_wishlist':already_in_wishlist,
                            'reviewStatus':review_submitted,
                            'reviews':reviews,
                            'exists':exists})

def vendorProfile(request, vendor):
    vendorObj = User.objects.filter(username=vendor)
    items = Item.objects.filter(vendorName=vendorObj[0].vendordetail)
    return render(request, 'store/vendor/profile.html',
                            {'vendorObj':vendorObj,
                            'vendorItems':items})

@login_required
def cart(request):

    checkout = False
    cartItems = Cart.objects.filter(user=request.user)
    total = 0
    for item in cartItems:
        total += (item.item.itemprice * item.quantity)
    balance = request.user.userdetail.balance

    if request.method == 'POST':
        userObj = UserDetail.objects.get(user=request.user)
        userObj.balance -= total
        userObj.save()
        logger.info(f'CHECKOUT: AMOUNT DEDUCTED {total}')
        vendorEmails = []

        cartitems = Cart.objects.filter(user=request.user)
        for item in cartitems:
            vendorEmails.append(item.item.vendorName.vendor.email)
            itemOrder = Item.objects.get(itemno=item.item.itemno)
            itemOrder.orders += 1
            itemOrder.save()
            UserOrders.objects.create(user=request.user, item=item.item)

        Cart.objects.filter(user=request.user).delete()
        logger.info(f'CHECKOUT: ITEMS DROPPED FROM CART FOR USER: {request.user.username}')
        send_mail('Items Sold', f'Items were sold recently', 'nagarpalikaishere@gmail.com', vendorEmails, fail_silently=False)
        logger.info(f'CHECKOUT: MAILS SENT TO VENDORS: {vendorEmails}')
        checkout = True
        logger.info('CHECKOUT: SUCCESSFUL')

    return render(request, 'store/cart.html',
                            {'cartItems':cartItems,
                            'total':total,
                            'balance':balance,
                            'checkout':checkout})

@login_required
def userDashboard(request):
    balance_updated = False
    address_updated = False
    InvalidAddress = False
    InvalidAmount = False
    if request.method == 'POST':
        if 'amount' in request.POST:
            amount = request.POST.get('amount')
            if amount == '':
                InvalidAmount = True
                logger.warning('NO AMOUNT SPECIFIED')
            else:
                userObj = UserDetail.objects.get(user=request.user)
                userObj.balance += int(amount)
                userObj.save()
                balance_updated = True
                logger.info(f'BALANCE UPDATED: AMOUNT DEPOSITED {amount}')
        elif 'address' in request.POST:
            address = request.POST.get('address')
            if address == '':
                InvalidAddress = True
                logger.warning('NO ADDRESS SPECIFIED')
            else:
                userDetailObj = UserDetail.objects.get(user=request.user)
                userDetailObj.address = address
                userDetailObj.save()
                address_updated = True
                logger.info('ADDRESS UPDATED')

    balance = request.user.userdetail.balance
    address = request.user.userdetail.address
    return render(request, 'store/dashboard.html',
                            {'balance':balance,
                            'address':address,
                            'balance_updated':balance_updated,
                            'addressUpdated':address_updated,
                            'invalidaddr':InvalidAddress,
                            'invalidamnt':InvalidAmount})

@login_required
def wishlist(request):

    item_deleted = False

    if request.method == 'POST':
        itemid = list(request.POST)[1]
        item = Item.objects.get(itemno=itemid)
        WishList.objects.filter(item=item).delete()
        item_deleted = True
        logger.info(f'ITEM WITH ITEMNO: {itemid} DELETED FROM WISHLIST')

    items = WishList.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html',
                            {'items':items,
                            'item_deleted':item_deleted})

@login_required
def userorders(request):

    userOrders = UserOrders.objects.filter(user=request.user)
    return render(request, 'store/userorders.html',
                            {'orders':userOrders})
