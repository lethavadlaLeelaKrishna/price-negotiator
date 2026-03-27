from django.contrib import admin
from .models import Product, NegotiationSession, ChatMessage, PriceOffer, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_price', 'minimum_price', 'discount_percentage', 'stock', 'image_tag')
    list_editable = ('discount_percentage', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('discount_percentage', 'created_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'stock', 'image')
        }),
        ('Pricing', {
            'fields': ('original_price', 'minimum_price', 'discount_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def image_tag(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' style='max-height:50px; max-width:80px;' />"
        return ''
    image_tag.allow_tags = True
    image_tag.short_description = 'Image'


@admin.register(NegotiationSession)
class NegotiationSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'product', 'status', 'original_price', 'final_agreed_price', 'discount_percentage')
    list_filter = ('status', 'created_at')
    search_fields = ('session_id', 'user__username', 'product__name')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Session Info', {
            'fields': ('session_id', 'user', 'product', 'status')
        }),
        ('Pricing Details', {
            'fields': ('original_price', 'offered_price', 'final_agreed_price', 'discount_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('message_type', 'content', 'offered_price', 'created_at')


class PriceOfferInline(admin.TabularInline):
    model = PriceOffer
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('offered_price', 'status', 'discount_percentage', 'reason', 'created_at')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'message_type', 'offered_price', 'created_at')
    list_filter = ('message_type', 'created_at')
    search_fields = ('session__session_id', 'content')
    readonly_fields = ('created_at',)


@admin.register(PriceOffer)
class PriceOfferAdmin(admin.ModelAdmin):
    list_display = ('session', 'offered_price', 'discount_percentage', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('session__session_id', 'reason')
    readonly_fields = ('created_at',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at',)
    fields = ('product', 'quantity', 'negotiated_price', 'original_price', 'added_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_items_count', 'get_total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Items'
    
    def get_total(self, obj):
           return f"₹{obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'negotiated_price', 'get_total_price', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('cart__user__username', 'product__name')
    readonly_fields = ('added_at',)
    
    def get_total_price(self, obj):
        return f"₹{obj.get_total_price():.2f}"
    get_total_price.short_description = 'Total Price'
