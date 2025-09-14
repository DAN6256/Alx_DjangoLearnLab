from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Book, CustomUser

# Get the custom user model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.
    Extends Django's built-in UserAdmin to include our custom fields.
    """
    
    # Fields to display in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'date_joined')
    
    # Fields that can be searched
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Fields that can be filtered
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    
    # Fields to display when editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
            'classes': ('collapse',),  # Make this section collapsible
        }),
    )
    
    # Fields to display when creating a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    # Make email field required in admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Creating new user
            form.base_fields['email'].required = True
        return form


class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for the Book model with improved display and functionality.
    """
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year', 'author')
    ordering = ['title']
    
    # Add pagination for large datasets
    list_per_page = 25


# Register the models with their respective admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)

# Customize the admin site header and title
admin.site.site_header = 'Advanced Features Library Administration'
admin.site.site_title = 'Library Admin Portal'
admin.site.index_title = 'Welcome to Library Administration'