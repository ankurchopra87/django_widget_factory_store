from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.utils.html import format_html

CURRENCY_CHOICES = (
    ('BTC', _("BitCoin")),
)


class ModelBase(models.Model):
    """Common fields for all models"""
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Create Timestamp'))
    modified_timestamp = models.DateTimeField(
        auto_now=True, verbose_name=_('Modified Timestamp'))

    class Meta:
        abstract = True

    def get_admin_change_url(self):
        """Returns the admin url for instance edit"""

        return reverse(
            "admin:%s_%s_change" % (
                self._meta.app_label,
                self._meta.model_name
            ), args=(self.pk,))

    @classmethod
    def get_admin_add_url(cls):
        """Returns the admin url for add"""

        return reverse(
            "admin:%s_%s_add" % (
                cls._meta.app_label,
                cls._meta.model_name
            ))

    @classmethod
    def get_admin_inline_add_formatted_html(cls):
        """Returns the formated html for inline add on the admin site"""

        format_string = """<a
            class="related-widget-wrapper-link add-related"
            id="add_id_{1}"
            href="{2}?_to_field=id&_popup=1"
            title="Add {1}">
            <img src="/static/admin/img/icon-addlink.svg" alt="Add">
        </a>"""

        return format_html(
            format_string,
            cls._meta.app_label,
            cls._meta.model_name,
            cls.get_admin_add_url()
        )


class ProductCategory(MPTTModel):
    """
    Model definition for ProductType. MPTT model for Hierarchial Tree
    Structure.
    """

    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children', verbose_name=_('Parent'))
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.CharField(
        max_length=256, verbose_name=_('Description'))

    class MPTTMeta:
        """Meta definition for ProductCategory."""
        order_insertion_by = ['name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        """Unicode representation of ProductCategory."""
        return self.name


class Product(ModelBase):
    """Model definition for Product."""

    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.CharField(
        max_length=256, verbose_name=_('Description'))
    manufacturer = models.CharField(
        max_length=50, verbose_name=_('Manufacturer'))
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, verbose_name=_('Category'))

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name


class AttributeType(ModelBase):
    """Model definition for AttributeType."""

    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.CharField(
        max_length=256, verbose_name=_('Description'))

    class Meta:
        """Meta definition for AttributeType."""

        verbose_name = 'AttributeType'
        verbose_name_plural = 'AttributeType'

    def __str__(self):
        """Unicode representation of AttributeType."""
        return self.name


class Attribute(ModelBase):
    """Model definition for Attribute."""

    type = models.ForeignKey(
        AttributeType, on_delete=models.PROTECT, verbose_name=_('Type'),
        related_name='attribute_set')
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.CharField(
        max_length=256, blank=True, verbose_name=_('Description'))

    class Meta:
        """Meta definition for Attribute."""

        verbose_name = 'Attribute'
        verbose_name_plural = 'Attribute'

    def __str__(self):
        """Unicode representation of Attribute."""
        return self.name


class SKU(ModelBase):
    """Model definition for SKU."""

    number = models.CharField(max_length=40, verbose_name=_('Number'))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    price = models.DecimalField(
        verbose_name=_('Price'), max_digits=8, decimal_places=8)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, verbose_name=_('Currency'))
    attributes = models.ManyToManyField(
        Attribute, verbose_name=_('Attributes'), related_name='sku_set')
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))

    class Meta:
        """Meta definition for SKU."""

        verbose_name = 'SKU'
        verbose_name_plural = 'SKU'

    def __str__(self):
        """Unicode representation of SKU."""
        return self.number


class Address(ModelBase):
    """Model definition for Address."""

    country = models.CharField(
        max_length=5, blank=False, verbose_name=_('Country'))
    street = models.CharField(
        max_length=50, blank=False, verbose_name=_('Street Address'))
    city = models.CharField(max_length=40, blank=False, verbose_name=_('City'))
    postal_code = models.CharField(
        max_length=20, blank=True, verbose_name=_('Postal Code'))
    state = models.CharField(
        max_length=50, verbose_name=_('State'), blank=True)
    department = models.CharField(
        max_length=50, verbose_name=_('Department'), blank=True)
    district = models.CharField(
        max_length=50, verbose_name=_('District'), blank=True)
    prefecture = models.CharField(
        max_length=50, verbose_name=_('Prefecture'), blank=True)
    province = models.CharField(
        max_length=50, verbose_name=_('Province'), blank=True)
    region = models.CharField(
        max_length=50, verbose_name=_('Region'), blank=True)
    municipality = models.CharField(
        max_length=50, verbose_name=_('Municipality'), blank=True)
    county = models.CharField(
        max_length=50, verbose_name=_('County'), blank=True)
    nation = models.CharField(
        max_length=50, verbose_name=_('Nation'), blank=True)
    phone = models.CharField(
        max_length=30, verbose_name=_('Phone Number'), blank=True)
    mobile_phone = models.CharField(
        max_length=30, verbose_name=_("Mobile Phone Number"), blank=True)

    class Meta:
        """Meta definition for Address."""

        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        """Unicode representation of Address."""
        return self.street


class Contact(ModelBase):
    """Model definition for Contact."""

    full_name = models.CharField(max_length=150, verbose_name=_('Full Name'))
    email = models.EmailField(max_length=255, verbose_name=_('Email Address'))

    class Meta:
        """Meta definition for Contact."""

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of Contact."""
        return self.full_name + " <" + self.email + ">"


class Order(ModelBase):
    """Model definition for Order."""

    PENDING_PAYMENT = 1
    FAILED = 2
    PROCESSING = 3
    COMPLETED = 4
    ON_HOLD = 5
    CANCELLED = 6
    REFUNDED = 7

    STATUS_CHOICES = (
        (PENDING_PAYMENT, _('Pending Payment')),
        (FAILED, _('Failed')),
        (PROCESSING, _('Processing')),
        (COMPLETED, _('Completed')),
        (ON_HOLD, _('On-Hold')),
        (CANCELLED, _('Cancelled')),
        (REFUNDED, _('Refunded'))
    )

    status = models.PositiveIntegerField(
        verbose_name=_('Status'), default=PROCESSING)

    ship_to = models.ForeignKey(
        Address, on_delete=models.CASCADE, verbose_name=_('Ship To'),
        related_name='ship_to_set')
    bill_to = models.ForeignKey(
        Address, on_delete=models.CASCADE, verbose_name=_('Bill To'),
        related_name='bill_to_set')
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, verbose_name=_('Contact'),
        related_name='contact_set')

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return str(self.id)


class OrderLine(ModelBase):
    """Model definition for OrderLine."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name=_('Order'),
        related_name="order_line_set")
    sku = models.ForeignKey(
        SKU, on_delete=models.CASCADE, verbose_name=_('SKU'))
    price = models.DecimalField(
        verbose_name=_('Price'), max_digits=8, decimal_places=8)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, verbose_name=_('Currency'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    ordering = models.PositiveIntegerField(verbose_name=_('Ordering'))

    class Meta:
        """Meta definition for OrderLine."""

        verbose_name = 'OrderLine'
        verbose_name_plural = 'OrderLines'

    def __str__(self):
        """Unicode representation of OrderLine."""
        return str(self.ordering)


# class OrderLineShippingInfo(ModelBase):
#     """Model definition for OrderLineShippingInfo."""

#     AWAITING_FULFILLMENT = 1
#     AWAITING_SHIPPMENT = 2
#     SHIPPED = 3
#     COMPLETED = 4
#     BACKORDERED = 5
#     CANCELLED = 6
#     REFUNDED = 7

#     STATUS_CHOICES = (
#         (AWAITING_FULFILLMENT, _('Awaiting Fulfillment')),
#         (AWAITING_SHIPPMENT, _('Awaiting Shipment')),
#         (SHIPPED, _('Shipped')),
#         (COMPLETED, _('Completed')),
#         (BACKORDERED, _('Backordered')),
#         (CANCELLED, _('Cancelled')),
#         (REFUNDED, _('Refunded'))
#     )

#     status = models.PositiveIntegerField(
#         choices=STATUS_CHOICES, verbose_name=_('Status'))
#     tracking = models.CharField(
#         max_length=100, verbose_name=_('Tracking'), default='')

#     class Meta:
#         """Meta definition for OrderLineShippingInfo."""

#         verbose_name = 'OrderLineShippingInfo'
#         verbose_name_plural = 'OrderLineShippingInfos'

#     def __str__(self):
#         """Unicode representation of OrderLineShippingInfo."""
#         pass
