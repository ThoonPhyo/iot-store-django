from django import forms
from .models import Product
from django.contrib.auth.models import User

# ၁။ Product အသစ်ထည့်ဖို့ ဒါမှမဟုတ် ပြင်ဖို့အတွက် Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image',]
        # ဒါက HTML မှာ ပေါ်မယ့် input field တွေကို သတ်မှတ်တာပါ

# # ၂။ User အသစ်တွေ Register လုပ်ဖို့ Form (Teacher လိုချင်တဲ့ Authentication အတွက်)
# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']