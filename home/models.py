
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('mehndi_favors', 'Mehndi Favors'),
        ('wedding_favours', 'Wedding Favours'),
        ('nikah_essentials', 'Nikah Essentials'),
        ('bridal_shower', 'Bridal Shower'),
        ('baby_shower', 'Baby Shower'),
        ('wedding_cards', 'Wedding Cards'),
        ('floral_jewellery', 'Floral Jewellery'),
        ('engagement', 'Engagement'),
    ]

    CUSTOMIZATION_CHOICES = [
        ('full', 'Full Customization'),
        ('name_only', 'Name Only'),
        ('none', 'No Customization'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    customization_type = models.CharField(
        max_length=20,
        choices=CUSTOMIZATION_CHOICES,
        default='none'
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} Image"


class ProductOption(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='options'
    )
    option_name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} - {self.option_name}"

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('mastercard', 'Mastercard'),
        ('debit_card', 'Debit Card'),
        ('sadapay', 'SadaPay'),
    ]
    full_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=30)
    delivery_address = models.TextField()

    additional_information = models.TextField(
        blank=True,
        null=True
    )
    payment_reference = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delivery_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=350
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product_name = models.CharField(
        max_length=200
    )

    selected_option = models.CharField(
        max_length=200,
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    bride_name = models.CharField(
        max_length=200,
        blank=True
    )

    groom_name = models.CharField(
        max_length=200,
        blank=True
    )

    event_type = models.CharField(
        max_length=100,
        blank=True
    )

    event_date = models.CharField(
        max_length=100,
        blank=True
    )

    additional_information = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.product_name} - Order #{self.order.id}"