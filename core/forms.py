from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Car

User = get_user_model()

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"autocomplete": "username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required = True
    )
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class MultipleImageField(forms.Field):
    widget = MultipleFileInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def clean(self, data):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        image_field = forms.ImageField(required=False)
        cleaned_files = []
        errors = []

        for f in data:
            try:
                cleaned_files.append(image_field.clean(f))
            except forms.ValidationError as e:
                errors.extend(e.error_list)

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_files

class CarForm(forms.ModelForm):
    additional_images = MultipleImageField(
        label="Additional images",
    )

    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "import_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(field, forms.BooleanField):
                widget.attrs.update({
                    "class": "form-check-input",
                })
                continue

            if isinstance(widget, forms.FileInput):
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    existing + " form-control bg-dark text-light border-secondary"
                ).strip()
                continue

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = (
                existing + " form-control bg-dark text-light border-secondary"
            ).strip()

        if "description" in self.fields:
            self.fields["description"].widget.attrs.setdefault("rows", 4)
        if "additional_features" in self.fields:
            self.fields["additional_features"].widget.attrs.setdefault("rows", 3)