from django.contrib import admin
from . models import *
from django import forms
from tinymce.widgets import TinyMCE

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email','created_date')

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

# Register your models here.
admin.site.register(Events)
admin.site.register(SubscribedUsers,SubscribedUsersAdmin)
