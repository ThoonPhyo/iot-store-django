from django.db import models
from django.contrib.auth.models import User

# ၁။ Product Table (ပစ္စည်းအချက်အလက်တွေသိမ်းဖို့)
class Product(models.Model):
    name = models.CharField(max_length=255) # ပစ္စည်းနာမည်
    price = models.DecimalField(max_digits=10, decimal_places=0) # ဈေးနှုန်း (ဥပမာ- 1500.50)
    description = models.TextField() # အသေးစိတ်ဖော်ပြချက်
    image = models.ImageField(upload_to='product_images/') # ပုံသိမ်းမည့်နေရာ

    # Category ရွေးစရာများကို သတ်မှတ်ခြင်း
    CATEGORY_CHOICES = [
        ('modules', 'Modules'),
        ('sensors', 'Sensors'),
        ('microcontroller', 'Microcontroller'),
        ('components', 'Components'),
    ]

    # Badge အတွက် ရွေးချယ်စရာများ
    LABEL_CHOICES = [
        ('none', 'None'), # ဘာမှမပြချင်ရင်
        ('new', 'New Arrival'),
        ('off', '50% OFF'),
        ('limited', 'Limited'),
        ('out', 'Stock Out'),
    ]

    # ဒီနေရာမှာ အမျိုးအစားကို Dropdown အနေနဲ့ ထည့်လိုက်တာပါ
    product_type = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='modules'
    )

    # Label field ကို ထည့်ပါ
    label = models.CharField(
        max_length=10, 
        choices=LABEL_CHOICES, 
        default='none'
    )

    def __str__(self):
        return self.name # Admin panel မှာ ပစ္စည်းနာမည်အတိုင်း မြင်ရအောင်လုပ်တာ

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    shopping_time = models.DateTimeField(auto_now_add=True)

    # ဈေးနှုန်းစုစုပေါင်း တွက်ရန် ထည့်ပေးပါ
    def total_price(self):
        return self.quantity * self.product.price

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class BestSellers(models.Model):
    # ForeignKey နဲ့ Product table က ပစ္စည်းကို လှမ်းချိတ်မယ်
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Admin မှာ နာမည်ပေါ်ဖို့အတွက်
    def __str__(self):
        return self.product.name