from PIL import Image

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms import ModelChoiceField, ModelForm, ValidationError

from .models import *




class MaskAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields('image').help_text = mark_safe(
            '<span style = "color:red; font-size: 14px;">Загружайте изображениес минимальным разрешением {}x{}</span>'.format(
                *Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height < max_height or img.width < max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image


class MaskAdmin(admin.ModelAdmin):

    form = MaskAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Masks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TshirtAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Tshirts'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HoodieAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='Hoodies'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Mask, MaskAdmin)
admin.site.register(Tshirt, TshirtAdmin)
admin.site.register(Hoodie, HoodieAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)

