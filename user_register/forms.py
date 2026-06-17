from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import phonenumbers

from user_register.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class PhoneForm(forms.Form):
    phone = forms.CharField(
        label="Номер телефона",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+996 555 123 456",
        }),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_phone(self):
        raw = self.cleaned_data["phone"]
        # Нормализация в E.164 через phonenumbers
        try:
            parsed = phonenumbers.parse(raw, None)
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Некорректный номер телефона.")
        if not phonenumbers.is_valid_number(parsed):
            raise forms.ValidationError("Номер телефона невалиден.")
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        # Проверка уникальности: исключаем профиль текущего юзера
        qs = Profile.objects.filter(phone=e164)
        if self.user:
            qs = qs.exclude(user=self.user)
        if qs.exists():
            raise forms.ValidationError("Этот номер уже привязан к другому аккаунту.")
        return e164
