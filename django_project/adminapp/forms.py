from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from mainapp.models import Product
from django import forms


class UserAdminRegisterForm(UserRegisterForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class ProductAdminCreateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Product
        fields = ('name', 'description', 'short_description', 'image', 'price', 'quantity', 'category')

    def __init__(self, *args, **kwargs):
        super(ProductAdminCreateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
