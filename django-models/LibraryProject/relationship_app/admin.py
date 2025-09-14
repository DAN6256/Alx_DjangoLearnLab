from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.html import format_html
from .models import CustomUser, Author, Book, Library, Librarian

# Custom User Forms
class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating users in admin"""
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'role')

class CustomUserChangeForm(UserChangeForm):
    """Custom form for changing users in admin"""
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'

# Custom User Admin
class CustomUserAdmin(BaseUserAdmin):
    """Custom admin interface for CustomUser"""
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    
    # Fields to display in the user list
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'role',
        'age_display',
        'profile_photo_display',
        'is_staff',
        'is_active',
        'date_joined'
    )
    
    # Fields to filter by
    list_filter = (
        'role', 
        'is_staff', 
        'is_superuser', 
        'is_active', 
        'date_joined',
        'date_of_birth'
    )
    
    # Fields to search by
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Ordering
    ordering = ('username',)
    
    # Fields to display when viewing/editing a user
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')
        }),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
        ('Role', {
            'classes': ('wide',),
            'fields': ('role',),
        }),
    )
    
    # Custom methods for display
    def age_display(self, obj):
        """Display user's age"""
        age = obj.age
        return age if age is not None else 'Not specified'
    age_display.short_description = 'Age'
    
    def profile_photo_display(self, obj):
        """Display profile photo thumbnail"""
        if obj.profile_photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_photo.url
            )
        return 'No photo'
    profile_photo_display.short_description = 'Photo'

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models with enhanced admin interfaces
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    filter_horizontal = ('books',)
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library', 'user')
    list_filter = ('library',)
    search_fields = ('name', 'library__name', 'user__username')
    raw_id_fields = ('user',)  # Use raw ID field for user selection