from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE

class FlatPageForm(FlatpageForm):

    class Meta:
        model = FlatPage
        fields = '__all__'
        widgets = {
            'content' : TinyMCE(attrs={'cols': 100, 'rows': 15}),
        }

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    form = FlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'registration_required',
                'template_name',
            ),
        }),
    )

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)