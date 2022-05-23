from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import UserDetail, Item

@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
  pass

admin.site.register(UserDetail)

