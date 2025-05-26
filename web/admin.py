from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class CategoryFilter(admin.SimpleListFilter):
    title = 'Category'
    parameter_name = 'catagory'

    def lookups(self, request, model_admin):
        categories = set([c.catagory for c in Character.objects.all()])
        return [(cat.id, cat.name) for cat in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(character__catagory__id=self.value())
        return queryset

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image_preview', 'description')
    def get_image_preview(self, obj):
        return mark_safe(f'<img src="{obj.Catagory_image_url}" style="max-height: 100px; max-width: 100px;" />')

    get_image_preview.short_description = 'Image Preview'
    get_image_preview.allow_tags = True

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name',  'get_image_preview', 'description','priority')
    def get_image_preview(self, obj):
        return mark_safe(f'<img src="{obj.Character_image_url}" style="max-height: 100px; max-width: 100px;" />')
    get_image_preview.short_description = 'Image Preview'
    get_image_preview.allow_tags = True
    
    list_filter = ['priority']
    search_fields = ['name']

#class CharacterAdmin(admin.ModelAdmin):
#    list_display = ('name', 'get_catagories', 'get_image_preview', 'description', 'priority')
#    list_filter = ['catagories__name', 'priority']  # Corrected list filter
#    search_fields = ['name']

#    def get_image_preview(self, obj):
#        return mark_safe(
#            f'<img src="{obj.Character_image_url}" style="max-height: 100px; max-width: 100px;" />'
#        )

#    def get_catagories(self, obj):
#        return ", ".join([cat.name for cat in obj.catagories.all()])

#    get_image_preview.short_description = 'Image Preview'
#    get_catagories.short_description = 'Categories'

class CharacterDetailsAdmin(admin.ModelAdmin):
    list_display = ('character', 'title', 'short_body', 'hide_title')
    list_filter = ['character', 'hide_title', CategoryFilter]
    search_fields = ['body', 'title']
    def short_body(self, obj):
        return obj.body[:100] + ('...' if len(obj.body) > 100 else '')
    short_body.short_description = 'Body'

admin.site.register(Catagory, CategoryAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Character_Details, CharacterDetailsAdmin)