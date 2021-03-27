from django.contrib import admin
from .models import Post, Profile, Comment, Follow, Like, File


class PostAdmin(admin.ModelAdmin):
    list_display = ['text', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(File)
