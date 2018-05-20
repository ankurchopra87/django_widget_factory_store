from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html, mark_safe
from .forms import OrderForm


class StoreAdminSite(admin.AdminSite):
    """ Customizing Store Admin Site"""

    # Text to put at the end of each page's <title>.
    site_title = _('admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = _('Widget Factory')

    # Text to put at the top of the admin index page.
    index_title = _('Administration')


class OrderLineInline(admin.TabularInline):
    """Definition for Inline Tabular display of OrderLines"""

    model = OrderLine
    extra = 0  # No empty OrderLines (for adding) by default
    readonly_fields = (
        'sku', 'price', 'currency', 'quantity', 'ordering')


class OrderAdmin(admin.ModelAdmin):
    """Definition for admin display of Orders"""

    list_display = (
        'id', 'status_description', 'bill_to_address', 'ship_to_address',
        'created_timestamp', 'modified_timestamp',)
    list_filter = ('order_line_set__sku__product',)

    fieldsets = (
        (None, {
            'fields': ('id', 'status', 'contact')
        }),
        ('Bill To', {
            'fields': ('bill_to_address',),
        }),
        ('Ship To', {
            # 'classes': ('collapse',),
            'fields': ('ship_to_address',),
        }),
    )

    readonly_fields = ('id', 'bill_to_address', 'ship_to_address', )
    date_hierarchy = 'created_timestamp'
    inlines = (OrderLineInline, )
    form = OrderForm  # custom form to allow status selection

    @staticmethod
    def get_address_formatted_html(instance, field_name):
        """
        Returns html containing full address and a edit link
        """
        return format_html(
            """
            <span>{1}</span>
            <a
                class="related-widget-wrapper-link change-related"
                id="change_id_{2}"
                href="{0}?_to_field=id&_popup=1"
                data-href-template="/admin/{3}/{4}/__fk__/change/?_to_field=id&_popup=1">
                <img src="/static/admin/img/icon-changelink.svg" alt="Change">
            </a>
            """,
            instance.get_admin_change_url(),
            instance.street,
            field_name,
            instance._meta.app_label,
            instance._meta.model_name,
        )

    def bill_to_address(self, instance):
        """Readonly field accessor for bill to address"""

        # On Order add, show Address add html, on edit show edit html
        if(instance.pk is None):
            return Address.get_admin_inline_add_formatted_html()
        return self.get_address_formatted_html(instance.bill_to, 'bill_to')

    def ship_to_address(self, instance):
        """Readonly field accessor for ship to address"""

        # On Order add, show Address add html, on edit show edit html
        if(instance.pk is None):
            return Address.get_admin_inline_add_formatted_html()
        return self.get_address_formatted_html(instance.ship_to, 'ship_to')

    def status_description(self, instance):
        """List field accessor for status description"""
        return Order.STATUS_CHOICES[instance.status - 1][1]

    bill_to_address.short_description = _("Address")
    ship_to_address.short_description = _("Address")


class SKUAdmin(admin.ModelAdmin):
    """Definition for admin display of SKUs"""

    list_display = (
        'number', 'product', 'attribute_description', 'price', 'currency',
        'quantity',)
    list_filter = ('product', 'attributes',)

    search_fields = (
        'attributes__name', 'product__name', 'product__category__name'
    )

    def attribute_description(self, instance):
        """List field accessor for attribute description"""
        html = ""
        for attribute in instance.attributes.all():
            html += "<li>" + attribute.name + "</li>"

        return mark_safe("<ul>" + html + "</ul>")

    attribute_description.short_description = _("Attributes")

# Instantiate admin_site and register urls
admin_site = StoreAdminSite()
admin_site.register(ProductCategory)
admin_site.register(Product)
admin_site.register(AttributeType)
admin_site.register(Attribute)
admin_site.register(SKU, SKUAdmin)
admin_site.register(Address)
admin_site.register(Contact)
admin_site.register(Order, OrderAdmin)
