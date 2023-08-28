from django.contrib import admin
from .models import CustomUser, Follow

# Define an inline admin descriptor for Follow model
class FollowInline(admin.TabularInline):
    model = Follow
    extra = 1
    fk_name = 'follower'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
    inlines = [FollowInline]  # This will allow you to see and manage related Follow instances directly within the CustomUser edit page.

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__email', 'following__email')
