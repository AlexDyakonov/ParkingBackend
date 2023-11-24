from django.contrib import admin
from api.models import Mock

# Register your models here.
class MockAdmin(admin.ModelAdmin):
    list_display = ['pk', 'text']

admin.site.register(Mock, MockAdmin)