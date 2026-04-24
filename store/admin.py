from django.contrib import admin
from .models import Product, CartItem, BestSellers

# ၁။ Product Admin: Name, Type, Price, Category တွေပြဖို့
class ProductAdmin(admin.ModelAdmin):
    # ဇယားမှာ ပြချင်တဲ့ column နာမည်တွေကို ဒီမှာ ထည့်
    list_display = ('name', 'product_type', 'price', 'label') 
    list_filter = ('product_type', 'label') # ဘေးမှာ filter နဲ့ ရွေးကြည့်လို့ရအောင်
    search_fields = ('name',) # ပစ္စည်းနာမည်နဲ့ ရှာလို့ရအောင်

# ၂။ BestSellers Admin: Product Name နဲ့ Product Type ပြဖို့
class BestSellersAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_type')

    # Product table က data တွေကို လှမ်းယူတဲ့ function များ
    def get_name(self, obj):
        return obj.product.name
    get_name.short_description = 'Product Name' # Column ခေါင်းစဉ် နာမည်ပေးခြင်း

    def get_type(self, obj):
        return obj.product.get_product_type_display() # Human-readable name ရဖို့
    get_type.short_description = 'Product Type'

# ၃။ CartItem Admin: User, Product, Qty, Time ပြဖို့
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'get_total_price', 'shopping_time')
    list_filter = ('user',)

    # ဈေးနှုန်းတွက်တဲ့ function
    def get_total_price(self, obj):
        return f"{obj.quantity * obj.product.price} Ks"
    get_total_price.short_description = 'Total Price'

# Model တွေကို Admin မှာ Register လုပ်ခြင်း
admin.site.register(Product, ProductAdmin)
admin.site.register(BestSellers, BestSellersAdmin)
admin.site.register(CartItem, CartItemAdmin)