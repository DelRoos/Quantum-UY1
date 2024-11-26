from django.contrib import admin
from .models import SiteConfig, Newsletter, Contact

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email')
    
    def has_add_permission(self, request):
        # Empêcher la création de plusieurs configurations
        if self.model.objects.exists():
            return False
        return True

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('email',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent', 'is_read')
    list_filter = ('is_read', 'date_sent')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('date_sent',)