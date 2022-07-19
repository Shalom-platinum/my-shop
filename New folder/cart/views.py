from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Category
from .cart import Cart
from .forms import CartAddProductsForm
from coupons.forms import CouponApplyForm

# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id= product_id)
    form = CartAddProductsForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
        quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@require_POST
def coupon_remove(request):
    request.session['coupon_id']= None
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    for item in cart:
        # i want to try to convert the money value to comma seperated thousands
        #item['price'] = "{:,}".format(item['price'])
        item['update_quantity_form'] = CartAddProductsForm(initial={'quantity': item['quantity'],'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart, 'categories': categories, 'coupon_apply_form':coupon_apply_form})