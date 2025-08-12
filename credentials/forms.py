from django import forms
from django.core.exceptions import ValidationError

from utils.encryption import encrypt_password
from credentials.models import Credential, Category


class CredentialForm(forms.ModelForm):
    password = forms.CharField(strip=False)
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)  # validates format only if provided

    # select existing categories
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 6})
    )
    # add new categories by typing (comma-separated)
    categories_input = forms.CharField(
        required=False,
        label="Add categories",
        help_text="Comma-separated. Example: Work, Personal, Banking",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Work, Personal"})
    )

    class Meta:
        model = Credential
        fields = [
            # order matters for template
            "categories", "categories_input",
            "site_name", "username", "email", "phone_number",
            "site_url", "other", "password",
        ]
        widgets = {
            "other": forms.Textarea(attrs={"rows": 2, "style": "resize: vertical;"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        show_password = kwargs.pop("show_password", False)
        super().__init__(*args, **kwargs)

        # scope categories to this user
        if self.user:
            self.fields["categories"].queryset = Category.objects.filter(user=self.user)

        # show/hide password as text
        self.fields["password"].widget = (
            forms.TextInput() if show_password else forms.PasswordInput()
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        # Require at least one of username/email
        if not username and not email:
            self.add_error("username", "Enter either a username or an email.")
            self.add_error("email", "Enter either a username or an email.")
        return cleaned_data

    # ---- categories helpers ----
    def _parse_new_categories(self):
        raw = self.cleaned_data.get("categories_input") or ""
        names = [n.strip() for n in raw.split(",") if n.strip()]
        unique = []
        seen = set()
        for n in names:
            key = n.lower()
            if key not in seen:
                seen.add(key)
                unique.append(n)
        return unique

    def _ensure_categories_exist(self, names):
        created_ids = []
        for name in names:
            cat, _ = Category.objects.get_or_create(user=self.user, name=name)
            created_ids.append(cat.id)
        return created_ids

    def save(self, commit=True, **kwargs):
        user = kwargs.pop("user", None) or self.user
        instance = super().save(commit=False)
        instance.user = user
        instance.password_encrypted = encrypt_password(user, self.cleaned_data["password"])
        if commit:
            instance.save()

        selected = list(self.cleaned_data.get("categories", []))
        new_names = self._parse_new_categories()
        if new_names:
            new_ids = self._ensure_categories_exist(new_names)
            selected += list(Category.objects.filter(id__in=new_ids))
        instance.categories.set(selected)
        return instance

