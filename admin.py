from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from .models import WebEvent

class WebEventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget}
    }

admin.site.register(WebEvent, WebEventAdmin)
    