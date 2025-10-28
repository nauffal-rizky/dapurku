from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import CustomUser, Product, ProductVariant

class RegisterForm(UserCreationForm):
  email = forms.EmailField(required=True)
  phone_number = forms.CharField(required=True)
  profile_image = forms.ImageField(required=True)
  description = forms.CharField(
    required=False,
    widget=forms.Textarea(attrs={"placeholder": "Tuliskan deskripsi singkat tentang Anda/UMKM..."})
  )
  is_umkm = forms.BooleanField(
    required=False,
    label="Register as UMKM",
    help_text="Check this if you're registering as a UMKM.",
    widget=forms.HiddenInput()
  )

  class Meta:
    model = CustomUser
    fields = [
      'username',
      'email',
      'phone_number',
      'password1',
      'password2',
      'profile_image',
      'description', 
      'is_umkm'
    ]

class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['name', 'description', 'price', 'image', 'category', 'is_available']
    widgets = {
      'description': forms.Textarea(attrs={'rows': 3}),
      'price': forms.NumberInput(attrs={'step': '0.01'}),
    }

class ProductVariantForm(forms.ModelForm):
  class Meta:
    model = ProductVariant
    fields = ['name', 'additional_price', 'stock']
    widgets = {
      'additional_price': forms.NumberInput(attrs={'step': '0.01'}),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['name'].required = False
    self.fields['additional_price'].required = False
    self.fields['stock'].required = False

ProductVariantFormSet = inlineformset_factory(
  Product,
  ProductVariant,
  form=ProductVariantForm,
  extra=1,
  can_delete=True
)


class ProfileUpdateForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ['username', 'email', 'phone_number', 'user_status', 'profile_image', 'description']
    widgets = {
      'user_status': forms.Select(choices=CustomUser.STATUS_CHOICES),
    }

  def clean_phone_number(self):
    phone = self.cleaned_data.get('phone_number')
    if phone and not phone.isdigit():
      raise forms.ValidationError("Nomor telepon harus berupa angka.")
    return phone