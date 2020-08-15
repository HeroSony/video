from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('user', )
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(Video, VideoAdmin)