from django.contrib import admin
from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('user',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    exclude = ('content',)
