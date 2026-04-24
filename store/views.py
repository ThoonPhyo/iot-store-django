from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Product, BestSellers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem
from django.db.models import Sum

def index(request):
    # ၁။ Data များ ဆွဲထုတ်ခြင်း
    new_arrivals = Product.objects.filter(label='new')
    best_sellers = BestSellers.objects.all()
    category_name = request.GET.get('category')
    
    if category_name:
        products = Product.objects.filter(product_type=category_name)
    else:
        products = Product.objects.all() 

    # ၂။ Cart Logic
    cart_total = 0
    total_quantity = 0
    user_cart = [] # အစမှာ အလွတ်ပေးထားမယ်

    if request.user.is_authenticated:
        user_cart = CartItem.objects.filter(user=request.user)
        if user_cart.exists(): # Cart ထဲမှာ ပစ္စည်းရှိရင်
            total_quantity = user_cart.aggregate(total=Sum('quantity'))['total'] or 0
            cart_total = sum(item.quantity * item.product.price for item in user_cart)

    # ၃။ Context - ဒီနေရာမှာ 'cart_items' ကို ထည့်ပေးရ
    context = {
        'products': products,
        'selected_category': category_name,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'cart_total': cart_total,
        'total_quantity': total_quantity,
        'cart_items': user_cart,  # <--- ဒီစာကြောင်းက အဓိက အသက်ပါပဲ!
    }
    
    return render(request, 'store/index.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # အကောင့်ဆောက်ပြီးတာနဲ့ တစ်ခါတည်း Login ပေးဝင်မယ်
            return redirect('index') # home page ကို ပြန်ပို့မယ်
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def add_to_cart(request, product_id):
    # User က Login မဝင်ရသေးရင် Warning ပေးပြီး Login page ကို ပို့မယ်
    if not request.user.is_authenticated:
        messages.warning(request, "ခြင်းထဲထည့်ရန် အရင်ဆုံး Login ဝင်ပေးပါ။")
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    
    # User ရဲ့ Cart ထဲမှာ ဒီပစ္စည်းရှိပြီးသားလား စစ်မယ်
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        # ရှိပြီးသားဆိုရင် Quantity ကို ၁ တိုးမယ်
        cart_item.quantity += 1
        cart_item.save()
    
    # ပစ္စည်းထည့်ပြီးရင် မူလစာမျက်နှာ (သို့) ပစ္စည်းစာရင်းဆီ ပြန်ပို့မယ်
    return redirect('index')


# Quantity တိုးရန်
def add_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

# Quantity လျှော့ရန်
def reduce_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete() # ၁ ခုပဲ ရှိတော့ရင် ထပ်လျှော့ရင် ဖျက်လိုက်မယ်
    return redirect(request.META.get('HTTP_REFERER', 'index'))

# ပစ္စည်းကို ခြင်းထဲမှ လုံးဝဖျက်ရန်
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def checkout(request):
    if request.user.is_authenticated:
        # ၁။ လက်ရှိ User ရဲ့ CartItem အားလုံးကို ဆွဲထုတ်မယ်
        cart_items = CartItem.objects.filter(user=request.user)
        
        # ၂။ စုစုပေါင်းအရေအတွက်ကို တွက်မယ်
        total_quantity = sum(item.quantity for item in cart_items)

        # ၄။ Subtotal ကို တွက်မယ် (quantity * price) of each item in the cart
        subtotal = [item.subtotal() for item in cart_items]


        # ၃။ စုစုပေါင်းဈေးနှုန်းကို တွက်မယ် (quantity * price)
        cart_total = sum(item.total_price() for item in cart_items)
    else:
        subtotal = []
        cart_items = []
        total_quantity = 0
        cart_total = 0

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'cart_total': cart_total,
        'subtotal': subtotal,
    }
    
    return render(request, 'store/checkout.html', context)

def home(request):
    return render(request, 'store/index.html')

