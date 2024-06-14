from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from artd_shopify.models import (
    ShopifyAppCredential,
    ShopifyApiCredential,
    ShopifyProduct,
    ShopifyBrand,
    ShopifyCategory,
    ShopifyGraphQlCredential,
    ShopifyTag,
    ShopifyRootTag,
)


@admin.register(ShopifyAppCredential)
class ShopifyAppCredentialAdmin(admin.ModelAdmin):
    list_display = [
        "partner",
        "id",
        "store_url",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "status",
    ]
    search_fields = [
        "store_url",
        "id",
        "partner__name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Credential",
            {
                "fields": [
                    "partner",
                    "api_key",
                    "api_password",
                    "store_url",
                    "callback_url",
                    "api_version",
                    "auth_url",
                ],
            },
        ),
        (
            "Status",
            {
                "fields": ["status"],
            },
        ),
        (
            "Timestamps",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]


@admin.register(ShopifyApiCredential)
class ShopifyApiCredentialAdmin(admin.ModelAdmin):
    list_display = [
        "partner",
        "id",
        "vendor",
        "store_key",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "store_key",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Credential",
            {
                "fields": [
                    "partner",
                    "vendor",
                    "store_key",
                    "access_token",
                    "api_version",
                ],
            },
        ),
        (
            "Homologation",
            {
                "fields": [
                    "brand_prefix",
                    "category_regular_expression",
                ],
            },
        ),
        (
            "Status",
            {
                "fields": [
                    "status",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]


@admin.register(ShopifyProduct)
class ShopifyProductAdmin(admin.ModelAdmin):
    list_display = [
        "product_id",
        "name",
        "partner",
        "processed",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "partner__name",
        "processed",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "product_id",
        "name",
        "partner__name",
        "processed",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Product",
            {
                "fields": [
                    "product_id",
                    "name",
                    "json_data",
                    "partner",
                    "processed",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(ShopifyBrand)
class ShopifyBrandAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "artd_partner",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Brand",
            {
                "fields": [
                    "name",
                    "artd_partner",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]


@admin.register(ShopifyCategory)
class ShopifyCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "artd_partner",
        "artd_tax",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Category",
            {
                "fields": [
                    "name",
                    "artd_partner",
                    "artd_tax",
                    "json_data",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(ShopifyGraphQlCredential)
class ShopifyGraphQlCredentialAdmin(admin.ModelAdmin):
    list_display = [
        "partner",
        "store_key",
        "status",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "store_url",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Credential",
            {
                "fields": [
                    "partner",
                    "vendor",
                    "store_key",
                    "api_version",
                    "api_key",
                    "api_secret",
                    "access_token",
                ],
            },
        ),
        (
            "Homologation",
            {
                "fields": [
                    "product_counter",
                    "brand_prefix",
                    "category_regular_expression",
                ],
            },
        ),
        (
            "Status",
            {
                "fields": [
                    "status",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]


@admin.register(ShopifyTag)
class ShopifyTagAdmin(admin.ModelAdmin):
    list_display = [
        "tag",
        "artd_partner",
        "category",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "tag",
        "artd_partner__name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Tag",
            {
                "fields": [
                    "tag",
                    "artd_partner",
                    "category",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]


@admin.register(ShopifyRootTag)
class ShopifyRootTagAdmin(admin.ModelAdmin):
    list_display = [
        "artd_partner",
        "root_tag",
        "root_category",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "root_category__name",
        "artd_partner__name",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]
    fieldsets = [
        (
            "Shopify Tag",
            {
                "fields": [
                    "artd_partner",
                    "root_tag",
                    "root_category",
                ],
            },
        ),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                ],
            },
        ),
    ]
