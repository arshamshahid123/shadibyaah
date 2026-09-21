from django.contrib import admin
from .models import Product, ProductImage, ProductOption, Order, OrderItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'customization_type')
    list_filter = ('category', 'customization_type')
    search_fields = ('name',)
    inlines = [ProductImageInline, ProductOptionInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'option_name', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'contact_number',
        'delivery_address',
        'payment_method',
        'payment_reference',
        'total_amount',
        'created_at'
    )

    list_filter = (
        'payment_method',
        'created_at',
    )

    search_fields = (
        'full_name',
        'contact_number',
    )

    inlines = [OrderItemInline]

    @admin.register(OrderItem)
    class OrderItemAdmin(admin.ModelAdmin):
        list_display = (
            'id',
            'order',
            'product_name',
            'bride_name',
            'groom_name',
            'event_type',
            'additional_information',
            'selected_option',
            'price',
            'quantity',
            'subtotal',
        )