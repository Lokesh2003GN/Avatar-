from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django import forms

# Filter to allow category filtering in admin
class CategoryFilter(admin.SimpleListFilter):
    title = 'Category'
    parameter_name = 'catagory'  # Keeping the original spelling mistake

    def lookups(self, request, model_admin):
        categories = set([c.catagory for c in Character.objects.all()])  # Keeping 'catagory' as per your code
        return [(cat.id, cat.name) for cat in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(character__catagory__id=self.value())  # Keeping 'catagory' as per your code
        return queryset


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image_preview', 'description')

    def get_image_preview(self, obj):
        return mark_safe(f'<img src="{obj.Catagory_image_url}" style="max-height: 100px; max-width: 100px;" />')

    get_image_preview.short_description = 'Image Preview'
    get_image_preview.allow_tags = True


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image_preview', 'description', 'priority')

    def get_image_preview(self, obj):
        return mark_safe(f'<img src="{obj.Character_image_url}" style="max-height: 100px; max-width: 100px;" />')

    get_image_preview.short_description = 'Image Preview'
    get_image_preview.allow_tags = True
    
    list_filter = ['priority']
    search_fields = ['name']


class CharacterDetailsAdmin(admin.ModelAdmin):
    list_display = ('character', 'title', 'short_body', 'hide_title')
    list_filter = ['character', 'hide_title', CategoryFilter]
    search_fields = ['body', 'title']
    
    def short_body(self, obj):
        return obj.body[:100] + ('...' if len(obj.body) > 100 else '')

    short_body.short_description = 'Body'


class QuizeAdminForm(forms.ModelForm):
    class Meta:
        model = Quize
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Dynamically populate answer choices
            choices = self.instance.get_answer_choices()
            self.fields['ans'].widget = forms.Select(choices=choices)


class QuizeAdmin(admin.ModelAdmin):
    form = QuizeAdminForm
    list_display = (
       'question', 'defaculty' ,'op1', 'op1_img_preview', 'op2', 'op2_img_preview', 
        'op3', 'op3_img_preview', 'op4', 'op4_img_preview', 'ans'
    )

    fields = (
        'question', 'op1', 'op1_img_url', 'op2', 'op2_img_url', 
        'op3', 'op3_img_url', 'op4', 'op4_img_url', 'ans', 'defaculty'
    )

    def op1_img_preview(self, obj):
        return mark_safe(f'<img src="{obj.op1_img_url}" style="max-height: 100px; max-width: 100px;" />')

    op1_img_preview.short_description = 'Option 1 Image'

    def op2_img_preview(self, obj):
        return mark_safe(f'<img src="{obj.op2_img_url}" style="max-height: 100px; max-width: 100px;" />')

    op2_img_preview.short_description = 'Option 2 Image'

    def op3_img_preview(self, obj):
        return mark_safe(f'<img src="{obj.op3_img_url}" style="max-height: 100px; max-width: 100px;" />')

    op3_img_preview.short_description = 'Option 3 Image'

    def op4_img_preview(self, obj):
        return mark_safe(f'<img src="{obj.op4_img_url}" style="max-height: 100px; max-width: 100px;" />')

    op4_img_preview.short_description = 'Option 4 Image'


# Register models with admin site
admin.site.register(Catagory, CategoryAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Character_Details, CharacterDetailsAdmin)
admin.site.register(Quize, QuizeAdmin)
