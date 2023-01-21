from django.shortcuts import render,get_object_or_404,redirect,HttpResponse 
from .models import *
from django.db.models import Q
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .forms import *

# Create your views here.

def home(request):
    banner = Banner.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    e_products = Product.objects.filter(category__name = 'Electronics')

    context ={
        'banner':banner,
        'categories':categories,
        'brands':brands,
        'products':products,
        'e_products':e_products
    }

    return render(request, 'store_app/index.html', context)

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    related_products = Product.objects.filter(Q(category=product.category) | Q(brand=product.brand)).exclude(pk=pk)

    context = {
        'product':product,
        'related_products':related_products
    }
    return render(request, 'store_app/product-details.html', context)

def product_search(request):
    query = request.GET['q']
    lookup = Q(name__icontains =query) | Q(category__name__icontains = query) | Q(brand__name__icontains = query)
    products = Product.objects.filter(lookup)
    context = {
        'products':products,
        
    }
    return render(request, 'store_app/product-search.html', context)

from django.core.paginator import Paginator

def category_filtering(request,pk):
    cate = Category.objects.get(pk=pk)
    products = Product.objects.filter(Q(category=cate.id) | Q(category__parent_category=cate.id) | Q(category__parent_category__parent_category=cate.id))
    
    paginator = Paginator(products, 1) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj':page_obj
            }
    return render(request, 'store_app/category-product.html', context)


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check the order item is in the order
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, 'This Cart Product quantity updated')
            return redirect('product-detail', pk=pk)
        
        else:
            order.cart_product.add(cart_item)
            messages.info(request, 'This Product was add to cart')
            return redirect('product-detail', pk=pk)
    else:
        ordered_date = timezone.now()
        order =Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.cart_product.add(cart_item)
        messages.info(request, "this item quantity was updated")
        return redirect("product-detail", pk=pk)
    return redirect("product-detail", pk=pk)


@login_required
def cart_increment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check the order item is in the order
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, 'This Cart Product quantity updated')
            return redirect('cart-summary')
    else:
        return redirect('cart-summary')
    return redirect('cart-summary')

@login_required
def cart_decrement(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check the order item is in the order
        if order.cart_product.filter(product__pk=product.pk).exists():
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.info(request, 'This Cart Product quantity updated')
                return redirect('cart-summary')
            else:
                cart_item.delete()
                messages.info(request, 'This Product delete from cart ')
                return redirect('cart-summary')
    else:
        return redirect('cart-summary')
    return redirect('cart-summary')



@login_required
def remove_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check the order item is in the order
        if order.cart_product.filter(product__pk=product.pk).exists():
            cart_item = CartProduct.objects.filter(user=request.user, ordered=False)[0]
            cart_item.delete()
            messages.info(request, 'This item was remove from cart')
            return redirect('cart-summary')
        
        else:
            messages.info (request, 'This Product was not your cart')
            return redirect('cart-summary')
    else:
        messages.info (request, 'This Product was not your cart')
        return redirect('cart-summary')
    return redirect('cart-summary')

@login_required
def cart_summary(request):
    try:
        order =Order.objects.get(user=request.user, ordered=False)
        context={
            'order':order
        }
        return render(request, 'store_app/cart-summary.html',context)
    except ObjectDoesNotExist:
        messages.info(request, 'yor cart is empty')
        return redirect('/')

def order_summary(request):
    order =Order.objects.filter(user=request.user, ordered=True)
    context={
            'order':order
        }         
    return render(request, 'store_app/order-summary.html',context)

from django.http import HttpResponseRedirect

def add_to_wishlist(request,pk):
    product = get_object_or_404(Product, pk=pk)
    wish_product, created = WishList.objects.get_or_create(product=product,pk=product.pk, user=request.user)
    messages.success(request, 'Succesfully add')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def OrderDetails(request,pk):
    order = Order.objects.get(pk=pk)
    order_items = CartProduct.objects.filter(order=order)
    context={
            'order':order,
            'order_items':order_items,
        }
    return render(request, 'store_app/order_details.html',context)


@login_required
def review(request,pk):
    try:
        cartitems = CartProduct.objects.get(pk=pk,user=request.user, ordered=True)
        # user_review = ProductReview.objects.filter(user=request.user,product=cartitems.item)
        form = ProductReviewForm(request.POST, request.FILES)
        if request.method == 'POST':
            form = ProductReviewForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = request.user
                form.instance.product = cartitems.product
                form.rating = request.POST.get('rating')
                form.image = request.POST.get('image')
                form.save()
                messages.success(request, "Successful Save")
                return redirect('/')
            else:
                messages.error(request, 'Please correct the error below.')         
        context={
                'cartitems':cartitems,
                'form':form,
                # 'user_review':user_review
            }
        return render(request, 'store_app/review.html',context) 
    except ObjectDoesNotExist:
        return redirect('/')








def aboutus(request):
    about = AboutABC.objects.last()
    return render(request, 'store_app/about.html', {'about':about})


