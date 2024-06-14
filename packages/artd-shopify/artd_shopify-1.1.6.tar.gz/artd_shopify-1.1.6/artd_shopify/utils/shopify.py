from artd_partner.models import Partner
from artd_product.models import (
    Product,
    Category,
    RootCategory,
    Brand,
    Tax,
    Image as ShopifyImage,
    ProductImage,
    GroupedProduct,
)
from artd_shopify.models import (
    ShopifyAppCredential,
    ShopifyApiCredential,
    ShopifyProduct,
    ShopifyBrand,
    ShopifyCategory,
)
from bs4 import BeautifulSoup
import shopify
import os
import binascii
import requests
import json
import re
import spacy
import requests
from io import BytesIO
from PIL import Image
from django.core.files import File


SCOPES = ["read_products", "read_orders"]


class ShopifyAppUtil:
    __shopify_credential = None
    __api_key = None
    __api_password = None
    __store_url = None
    __shopify_session = None
    __callback_url = None
    __api_version = None
    __access_token = None

    def __init__(self, partner: Partner):
        self.partner = partner
        self.__shopify_credential = ShopifyAppCredential.objects.get(partner=partner)
        self.__api_key = self.__shopify_credential.api_key
        self.__api_password = self.__shopify_credential.api_password
        self.__store_url = self.__shopify_credential.store_url
        self.__callback_url = self.__shopify_credential.callback_url
        self.__api_version = self.__shopify_credential.api_version
        self.__access_token = self.__shopify_credential.access_token

    def get_shopify_auth_url(self):
        try:
            shopify.Session.setup(api_key=self.__api_key, secret=self.__api_password)
            shop_url = self.__store_url
            api_version = self.__api_version
            state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
            redirect_uri = self.__callback_url
            scopes = ["read_products", "read_orders"]

            newSession = shopify.Session(shop_url, api_version)
            auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

        except Exception as e:
            auth_url = None

        return auth_url

    def get_access_token(self):
        try:
            session = shopify.Session(self.__store_url, self.__api_version)
            access_token = session.request_token({"code": self.__access_token})
        except Exception as e:
            access_token = None

    def get_shopify_products(self):
        shopify = self.get_shopify_credential()
        if shopify:
            products = shopify.get("products.json").json()["products"]
            return products
        return None


class ShopifyApiUtil:
    __partner = None
    __store_key = None
    __api_version = None
    __access_token = None
    __vendor = None
    __brand_prefix = None
    __category_regular_expression = None
    __stored_shopify_products = None

    def __init__(self, partner: Partner):
        self.__partner = partner
        self.__shopify_credential = ShopifyApiCredential.objects.get(partner=partner)
        self.__store_key = self.__shopify_credential.store_key
        self.__api_version = self.__shopify_credential.api_version
        self.__access_token = self.__shopify_credential.access_token
        self.__vendor = self.__shopify_credential.vendor
        self.__brand_prefix = self.__shopify_credential.brand_prefix
        self.__category_regular_expression = (
            self.__shopify_credential.category_regular_expression
        )

    def remove_html_tags(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        text_without_tags = soup.get_text(separator=" ", strip=True)
        return text_without_tags

    def extract_metadata(self, description):
        nlp = spacy.load("es_core_news_sm")
        doc = nlp(description)
        meta_title = " ".join(token.text for token in doc[:3])
        meta_description = " ".join(token.text for token in doc[:20])
        meta_keywords = " ".join(
            token.text for token in doc if token.pos_ in ("NOUN", "ADJ")
        )

        return meta_title, meta_description, meta_keywords

    def get_shopify_products(self):
        print("*** Getting products from Shopify ***")
        url = f"https://{self.__store_key}.myshopify.com/admin/api/{self.__api_version}/products.json?limit=250&vendor=CEBA&since_id=1&fields=id,title,vendor,product_type,created_at,handle,updated_at,published_scope,tags,status,variants,images,image,body_html"
        payload = {}
        headers = {
            "X-Shopify-Access-Token": f"{self.__access_token}",
            "Content-Type": "application/json",
        }
        products = []
        page = 1
        try:
            while True:
                print(f"Getting products from page {page}")
                page += 1
                response = requests.request("GET", url, headers=headers, data=payload)
                response.raise_for_status()

                data = response.json()
                products.extend(data["products"])

                # Verifica si hay más páginas de productos
                if "Link" in response.headers:
                    links = requests.utils.parse_header_links(response.headers["Link"])
                    next_link = next(
                        (link["url"] for link in links if link["rel"] == "next"), None
                    )
                    if not next_link:
                        break

                    url = next_link
        except Exception as e:
            print(f"Error al obtener productos de Shopify: {e}")
            return None

        return products

    def get_custom_collections_from_shopify(self):
        print("*** Getting custom collections from Shopify ***")
        url = f"https://{self.__store_key}.myshopify.com/admin/api/{self.__api_version}/custom_collections.json"
        payload = {}
        headers = {
            "X-Shopify-Access-Token": f"{self.__access_token}",
            "Content-Type": "application/json",
        }
        custom_collections = []
        page = 1
        try:
            while True:
                print(f"Getting custom collections from page {page}")
                page += 1
                response = requests.request("GET", url, headers=headers, data=payload)
                response.raise_for_status()

                data = response.json()
                custom_collections.extend(data["custom_collections"])

                # Verifica si hay más páginas de productos
                if "Link" in response.headers:
                    links = requests.utils.parse_header_links(response.headers["Link"])
                    next_link = next(
                        (link["url"] for link in links if link["rel"] == "next"), None
                    )
                    if not next_link:
                        break

                    url = next_link
        except Exception as e:
            print(f"Error al obtener colecciones personalizadas de Shopify: {e}")
            return None

        return custom_collections

    def store_products_from_shopify(self, products):
        print("*** Storing products from Shopify ***")
        for product in products:
            if (
                ShopifyProduct.objects.filter(
                    product_id=product["id"],
                    partner=self.__partner,
                ).count()
                == 0
            ):
                print(f"Storing product {product['id']}")
                shopify_product = ShopifyProduct(
                    product_id=product["id"],
                    json_data=product,
                    partner=self.__partner,
                    name=product["title"],
                )
                shopify_product.save()
            else:
                print(f"Updating product {product['id']}")
                ShopifyProduct.objects.filter(
                    product_id=product["id"],
                    partner=self.__partner,
                ).update(json_data=product)
        return True

    def store_tags_from_shopify(self):
        print("*** Storing categories from Shopify ***")
        if (
            RootCategory.objects.filter(
                name=self.__vendor, partner=self.__partner
            ).count()
            == 0
        ):
            root_category = RootCategory(
                name=self.__vendor,
                partner=self.__partner,
            )
            root_category.save()
        else:
            print(f"Root category {self.__vendor} already exists")

        shopify_products = ShopifyProduct.objects.filter(partner=self.__partner)
        # Categories
        for product in shopify_products:
            tags = product.json_data["tags"].split(",")
            for tag in tags:
                tag_striped = tag.strip()
                if not tag_striped.startswith(self.__brand_prefix):
                    if Brand.objects.filter(name__icontains=tag_striped).count() == 0:
                        if (
                            Category.objects.filter(
                                name=tag_striped, partner=self.__partner
                            ).count()
                            == 0
                        ):
                            # evaluate if tag_striped matches the regular expression
                            if self.__category_regular_expression:
                                pattern = re.compile(
                                    rf"{self.__category_regular_expression}"
                                )
                                if pattern.search(tag_striped):
                                    print(f"Storing category {tag_striped}")
                                    if not "label" in tag_striped:
                                        category = Category(
                                            name=tag_striped,
                                            partner=self.__partner,
                                        )
                                        category.save()
                                        # Add Shopify Category
                                        tax = Tax.objects.first()

                                        if (
                                            ShopifyCategory.objects.filter(
                                                name=tag_striped,
                                                artd_partner=self.__partner,
                                            ).count()
                                            == 0
                                        ):
                                            shopify_category = ShopifyCategory(
                                                name=tag_striped,
                                                artd_partner=self.__partner,
                                                artd_tax=tax,
                                            )
                                            shopify_category.save()
                                else:
                                    # Create as brand
                                    if (
                                        Brand.objects.filter(name=tag_striped).count()
                                        == 0
                                    ):
                                        print(f"Storing brand {tag_striped}")
                                        brand = Brand(
                                            name=tag_striped,
                                        )
                                        brand.save()
                                        # Add Shopify Brand
                                        if (
                                            ShopifyBrand.objects.filter(
                                                name=tag_striped,
                                                artd_partner=self.__partner,
                                            ).count()
                                            == 0
                                        ):
                                            shopify_brand = ShopifyBrand(
                                                name=tag_striped,
                                                artd_partner=self.__partner,
                                            )
                                            shopify_brand.save()
                                    else:
                                        print(f"Brand {tag_striped} already exists")
                            else:
                                print(
                                    f"Product {tag_striped} has no category regular expression"
                                )
                                # Create as brand
                                if Brand.objects.filter(name=tag_striped).count() == 0:
                                    print(f"Storing brand {tag_striped}")
                                    brand = Brand(
                                        name=tag_striped,
                                    )
                                    brand.save()
                                    # Add Shopify Brand
                                    if (
                                        ShopifyBrand.objects.filter(
                                            name=tag_striped,
                                            artd_partner=self.__partner,
                                        ).count()
                                        == 0
                                    ):
                                        shopify_brand = ShopifyBrand(
                                            name=tag_striped,
                                            artd_partner=self.__partner,
                                        )
                                        shopify_brand.save()
                                else:
                                    print(f"Brand {tag_striped} already exists")
                            print(f"Storing category {tag_striped}")
                        else:
                            print(f"Category {tag_striped} already exists")

        # Brands
        for product in shopify_products:
            tags = product.json_data["tags"].split(",")
            for tag in tags:
                tag_striped = tag.strip()
                if tag_striped.startswith(self.__brand_prefix):
                    brand_name = tag_striped.replace(self.__brand_prefix, "")
                    if Brand.objects.filter(name=brand_name).count() == 0:
                        print(f"Storing brand {brand_name}")
                        brand = Brand(
                            name=brand_name,
                        )
                        brand.save()
                        # Add Shopify Brand
                        if (
                            ShopifyBrand.objects.filter(
                                name=tag_striped,
                                artd_partner=self.__partner,
                            ).count()
                            == 0
                        ):
                            shopify_brand = ShopifyBrand(
                                name=tag_striped,
                                artd_partner=self.__partner,
                            )
                            shopify_brand.save()
                    else:
                        print(f"Brand {brand_name} already exists")

    def get_brand_for_tags(self, tags):
        for tag in tags:
            tag_striped = tag.strip()
            if tag_striped.startswith(self.__brand_prefix):
                print(f"Brand tag {tag_striped}")
                brand_tag = tag_striped.replace(self.__brand_prefix, "")
                if Brand.objects.filter(name=brand_tag).count() > 0:
                    return Brand.objects.get(name=brand_tag)
        return None

    def get_categories_from_tags(self, tags):
        if "ALLPRODUCTS" in tags:
            tags.remove("ALLPRODUCTS")
        if "TODOSLOSPRODUCTOS" in tags:
            tags.remove("TODOSLOSPRODUCTOS")
        categories = []
        for tag in tags:
            tag_striped = tag.strip()
            if not tag_striped.startswith(self.__brand_prefix):
                if Category.objects.filter(name=tag_striped).count() > 0:
                    categories.append(Category.objects.get(name=tag_striped))
        return categories

    def get_variant_options(self, variant):
        options = []
        for key, value in variant.items():
            if key.startswith("option"):
                options.append(
                    {
                        key: value,
                    }
                )
        return options

    def get_stored_shopify_products(self) -> ShopifyProduct:
        self.__stored_shopify_products = ShopifyProduct.objects.filter(
            partner=self.__partner
        )
        return self.__stored_shopify_products

    def store_artd_products_from_shopify(self):
        print("*** Storing Artd products from Shopify ***")
        shopify_products = self.__stored_shopify_products
        for product in shopify_products:
            product_data = product.json_data

            if "handle" in product_data:
                # Product image
                images = product_data["images"]
                image_list = []
                for image in images:
                    id = image["id"]
                    image_source = {
                        "name": "shopify",
                        "id": id,
                        "partner": self.__partner.id,
                    }
                    image_external_id = id
                    if image["alt"] is None:
                        alt = id
                    else:
                        alt = image["alt"]
                    src = image["src"]
                    alt = alt
                    response = requests.get(src)
                    response.raise_for_status()
                    name = f"{id}.jpg"
                    if (
                        ShopifyImage.objects.filter(
                            external_id=image_external_id,
                            partner=self.__partner,
                        ).count()
                        == 0
                    ):
                        image = ShopifyImage.objects.create(
                            image=File(BytesIO(response.content), name=name),
                            alt=alt,
                            external_id=image_external_id,
                            partner=self.__partner,
                            source=image_source,
                        )
                        image_list.append(image)
                    else:
                        image = ShopifyImage.objects.filter(
                            external_id=image_external_id,
                            partner=self.__partner,
                        )
                        image_list.append(image)

                source = {
                    "name": "shopify",
                    "id": product_data["id"],
                    "partner": self.__partner.id,
                }

                brand = self.get_brand_for_tags(product_data["tags"].split(","))
                categories = self.get_categories_from_tags(
                    product_data["tags"].split(",")
                )
                first_category = categories[0] if len(categories) > 0 else None
                if first_category is not None:
                    category_name = first_category.name
                else:
                    category_name = None

                shopify_category = ShopifyCategory.objects.filter(
                    name=category_name,
                    artd_partner=self.__partner,
                ).first()

                meta_title, meta_description, meta_keywords = self.extract_metadata(
                    self.remove_html_tags(product_data["body_html"])
                )

                if brand is not None:
                    product_data["brand"] = brand
                # Main product
                main_variants = product_data["variants"][0]
                options = self.get_variant_options(main_variants)
                product_list = []
                product = Product.objects.create(
                    source=source,
                    json_data=product_data,
                    external_id=product_data["id"],
                    url_key=product_data["handle"],
                    meta_title=meta_title,
                    meta_description=meta_description,
                    meta_keywords=meta_keywords,
                    type="physical",
                    name=product_data["title"],
                    sku=product_data["variants"][0]["sku"],
                    description=product_data["body_html"],
                    short_description=product_data["title"],
                    tax=shopify_category.artd_tax,
                    weight=product_data["variants"][0]["weight"],
                    unit_of_measure="kg",
                    measure=product_data["variants"][0]["weight"],
                    variations=options,
                )
                for image in image_list:
                    ProductImage.objects.create(product=product, image=image)
                product.categories.set(categories)
                product_list.append(product)
                variants = product_data["variants"]
                variants.pop(0)
                # Variant products
                for variant in variants:
                    source = {
                        "name": "shopify",
                        "id": variant["id"],
                        "partner": self.__partner.id,
                    }
                    variant_options = self.get_variant_options(variant)
                    product = Product.objects.create(
                        source=source,
                        json_data=variant,
                        external_id=variant["id"],
                        url_key=product_data["handle"],
                        meta_title=meta_title,
                        meta_description=meta_description,
                        meta_keywords=meta_keywords,
                        type="physical",
                        name=variant["title"],
                        sku=variant["sku"],
                        description=product_data["body_html"],
                        short_description=product_data["title"],
                        tax=shopify_category.artd_tax,
                        weight=product_data["variants"][0]["weight"],
                        unit_of_measure="kg",
                        measure=product_data["variants"][0]["weight"],
                        variations=variant_options,
                    )
                    for image in image_list:
                        ProductImage.objects.create(product=product, image=image)
                    product_list.append(product)

                # print(images)
