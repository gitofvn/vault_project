from django.contrib import admin

from credentials.models import Credential, Category


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'categories_list', 'user', 'created_at')
    search_fields = ('site_name', 'email')
    list_filter = ('categories',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    exclude = ('password_encrypted', 'other', 'phone_number')

    def categories_list(self, obj):
        names = obj.categories.values_list('name', flat=True)
        return ", ".join(names) if names else "-"
    categories_list.short_description = 'Categories'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)
    ordering = ('name',)
