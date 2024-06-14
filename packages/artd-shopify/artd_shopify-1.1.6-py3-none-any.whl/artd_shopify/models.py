from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_partner.models import Partner
from artd_product.models import Tax


class ShopifyBaseModel(models.Model):
    status = models.BooleanField(
        _("Status"),
        help_text=_("Designates whether this record is active or not."),
        default=True,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        help_text=_("Date time on which the object was created."),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Date time on which the object was last updated."),
        auto_now=True,
    )

    class Meta:
        abstract = True


class ShopifyAppCredential(ShopifyBaseModel):
    """Model definition for Shopify Credential."""

    partner = models.OneToOneField(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Partner associated with this credential."),
        on_delete=models.CASCADE,
    )
    vendor = models.CharField(
        _("Vendor"),
        help_text=_("Shopify Vendor."),
        max_length=100,
    )

    api_version = models.CharField(
        _("API version"),
        help_text=_("Shopify API Version."),
        max_length=255,
    )
    api_key = models.CharField(
        _("API key"),
        help_text=_("Shopify API Key."),
        max_length=255,
    )
    api_password = models.CharField(
        _("API password"),
        help_text=_("Shopify API Password."),
        max_length=255,
    )
    store_url = models.CharField(
        _("Store URL"),
        help_text=_("Shopify Store URL."),
        max_length=255,
    )
    callback_url = models.URLField(
        _("Callback URL"),
        help_text=_("Shopify Callback URL."),
    )
    auth_url = models.TextField(
        _("Auth URL"),
        help_text=_("Shopify Auth URL."),
        blank=True,
        null=True,
    )
    access_token = models.TextField(
        _("Access token"),
        help_text=_("Shopify Access Token."),
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Shopify Credential."""

        verbose_name = _("Shopify Credential")
        verbose_name_plural = _("Shopify Credentials")

    def __str__(self):
        """Unicode representation of Shopify Credential."""
        return self.store_url


class ShopifyApiCredential(ShopifyBaseModel):
    """Model definition for Shopify Credential."""

    partner = models.OneToOneField(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Partner associated with this credential."),
        on_delete=models.CASCADE,
    )
    vendor = models.CharField(
        _("Vendor"),
        help_text=_("Shopify Vendor."),
        max_length=100,
    )
    store_key = models.CharField(
        _("Store key"),
        help_text=_("Shopify Store Key."),
        max_length=255,
    )
    api_version = models.CharField(
        _("API version"),
        help_text=_("Shopify API Version."),
        max_length=255,
    )
    access_token = models.TextField(
        _("Access token"),
        help_text=_("Shopify Access Token."),
        blank=True,
        null=True,
    )
    product_counter = models.PositiveIntegerField(
        _("Product counter"),
        help_text=_("Shopify Product Counter."),
        default=0,
    )
    brand_prefix = models.CharField(
        _("Brand prefix"),
        help_text=_("Shopify Brand Prefix."),
        max_length=255,
        blank=True,
        null=True,
    )
    category_regular_expression = models.CharField(
        _("Category regular expression"),
        help_text=_("Shopify Category Regular Expression."),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Shopify Credential."""

        verbose_name = _("Shopify API Credential")
        verbose_name_plural = _("Shopify API Credentials")

    def __str__(self):
        """Unicode representation of Shopify Credential."""
        return self.store_key


class ShopifyGraphQlCredential(ShopifyBaseModel):
    """Model definition for Shopify GraphQl Credential."""

    partner = models.OneToOneField(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Partner associated with this credential."),
        on_delete=models.CASCADE,
    )
    vendor = models.CharField(
        _("Vendor"),
        help_text=_("Shopify Vendor."),
        max_length=100,
    )
    store_key = models.CharField(
        _("Store key"),
        help_text=_("Shopify Store Key."),
        max_length=255,
    )
    api_version = models.CharField(
        _("API version"),
        help_text=_("Shopify API Version."),
        max_length=255,
    )
    api_key = models.CharField(
        _("API key"),
        help_text=_("Shopify API Key."),
        max_length=255,
    )
    api_secret = models.CharField(
        _("API secret"),
        help_text=_("Shopify API Secret."),
        max_length=255,
    )
    access_token = models.TextField(
        _("Access token"),
        help_text=_("Shopify Access Token."),
        blank=True,
        null=True,
    )
    product_counter = models.PositiveIntegerField(
        _("Product counter"),
        help_text=_("Shopify Product Counter."),
        default=0,
    )
    brand_prefix = models.CharField(
        _("Brand prefix"),
        help_text=_("Shopify Brand Prefix."),
        max_length=255,
        blank=True,
        null=True,
    )
    category_regular_expression = models.CharField(
        _("Category regular expression"),
        help_text=_("Shopify Category Regular Expression."),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Shopify GraphQl Credential."""

        verbose_name = _("Shopify GraphQl Credential")
        verbose_name_plural = _("Shopify GraphQl Credentials")

    def __str__(self):
        """Unicode representation of Shopify GraphQl Credential."""
        return self.store_key


class ShopifyProduct(ShopifyBaseModel):
    """Model definition for Shopfy Product."""

    product_id = models.CharField(
        _("Product id"),
        help_text=_("Shopify Product ID."),
        max_length=255,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Shopify Product Name."),
        max_length=255,
        blank=True,
        null=True,
    )
    json_data = models.JSONField(
        _("Json data"),
        help_text=_("Shopify Product JSON Data."),
        default=dict,
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Partner associated with this product."),
        on_delete=models.CASCADE,
    )
    processed = models.BooleanField(
        _("Processed"),
        help_text=_("Designates whether this product is processed or not."),
        default=False,
    )

    class Meta:
        """Meta definition for Shopfy Product."""

        verbose_name = _("Shopfy Product")
        verbose_name_plural = _("Shopfy Products")

    def __str__(self):
        """Unicode representation of Shopfy Product."""
        return self.product_id


class ShopifyCategory(ShopifyBaseModel):
    """Model definition for Shopify Category."""

    name = models.CharField(
        _("Name"),
        help_text=_("Shopify Category Name."),
        max_length=255,
    )
    artd_partner = models.ForeignKey(
        Partner,
        verbose_name=_("Artd partner"),
        help_text=_("ArtD Partner associated with this category."),
        on_delete=models.CASCADE,
    )
    artd_tax = models.ForeignKey(
        Tax,
        verbose_name=_("Artd tax"),
        help_text=_("ArtD Tax associated with this category."),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    json_data = models.JSONField(
        _("Json data"),
        help_text=_("Shopify Category JSON Data."),
        default=dict,
    )

    class Meta:
        """Meta definition for Shopify Category."""

        verbose_name = _("Shopify Category")
        verbose_name_plural = _("Shopify Categories")

    def __str__(self):
        """Unicode representation of Shopify Category."""
        return self.name


class ShopifyBrand(ShopifyBaseModel):
    """Model definition for Shopify Brand."""

    name = models.CharField(
        _("Name"),
        help_text=_("Shopify Brand Name."),
        max_length=255,
    )
    artd_partner = models.ForeignKey(
        "artd_partner.Partner",
        verbose_name=_("Artd partner"),
        help_text=_("ArtD Partner associated with this category."),
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Shopify Brand."""

        verbose_name = _("Shopify Brand")
        verbose_name_plural = _("Shopify Brands")

    def __str__(self):
        """Unicode representation of Shopify Brand."""
        return self.name


class ShopifyTag(ShopifyBaseModel):
    """Model definition for Shopify Tag."""

    tag = models.CharField(
        _("Tag"),
        help_text=_("Shopify Tag."),
        max_length=255,
    )
    artd_partner = models.ForeignKey(
        "artd_partner.Partner",
        verbose_name=_("Artd partner"),
        help_text=_("ArtD Partner associated with this tag."),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        "artd_product.Category",
        verbose_name=_("Category"),
        help_text=_("ArtD Category associated with this tag."),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Shopify Tag."""

        verbose_name = _("Shopify Tag")
        verbose_name_plural = _("Shopify Tags")

    def __str__(self):
        """Unicode representation of Shopify Tag."""
        return self.tag


class ShopifyRootTag(ShopifyBaseModel):
    """Model definition for Shopify Root Tag."""

    artd_partner = models.ForeignKey(
        "artd_partner.Partner",
        verbose_name=_("Partner"),
        help_text=_("ArtD Partner associated with this tag."),
        on_delete=models.CASCADE,
    )
    root_tag = models.CharField(
        _("Root tag"),
        help_text=_("Shopify Root Tag."),
        max_length=255,
    )
    root_category = models.ForeignKey(
        "artd_product.RootCategory",
        verbose_name=_("Root category"),
        help_text=_("ArtD Category associated with this tag."),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta definition for Shopify Root Tag."""

        verbose_name = _("Shopify Root Tag")
        verbose_name_plural = _("Shopify Root Tags")

    def __str__(self):
        """Unicode representation of Shopify Root Tag."""
        return self.root_tag
