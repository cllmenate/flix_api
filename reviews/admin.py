from django.contrib import admin
from reviews.models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'rating', 'comment',)
    search_fields = ('movie__title',)
    list_filter = ('rating',)

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated