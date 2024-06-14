from artd_partner.models import Partner
from django.db.models import Count
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
    ShopifyGraphQlCredential,
    ShopifyProduct,
    ShopifyBrand,
    ShopifyCategory,
    ShopifyTag,
    ShopifyRootTag,
)
import os
from urllib.parse import urlparse
import requests
import json
import requests
from io import BytesIO
from PIL import Image
from django.core.files import File
from artd_shopify.utils.graphql.queries import (
    MAIN_NODE_REQUIRED_INFO,
    NODE_REQUIRED_INFO,
)
from artd_price_list.models import PriceList
from artd_stock.models import Stock
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_PATH = os.path.join("media/product/images/")


class ShopifyGraphQl:
    __partner = None
    __shopify_credential = None
    __vendor = None
    __shopify_credential = None
    __store_key = None
    __api_version = None
    __api_key = None
    __api_secret = None
    __access_token = None
    __product_counter = None
    __brand_prefix = None
    __category_regular_expression = None
    __endpoint = None

    def __init__(self, partner: Partner):
        self.__partner = partner
        self.__shopify_credential = ShopifyGraphQlCredential.objects.get(
            partner=partner
        )
        self.__vendor = self.__shopify_credential.vendor
        self.__store_key = self.__shopify_credential.store_key
        self.__api_version = self.__shopify_credential.api_version
        self.__api_key = self.__shopify_credential.api_key
        self.__api_secret = self.__shopify_credential.api_secret
        self.__access_token = self.__shopify_credential.access_token
        self.__product_counter = self.__shopify_credential.product_counter
        self.__brand_prefix = self.__shopify_credential.brand_prefix
        self.__category_regular_expression = (
            self.__shopify_credential.category_regular_expression
        )
        self.__endpoint = f"https://{self.__store_key}.myshopify.com/admin/api/{self.__api_version}/graphql.json"
        self.__headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.__access_token,
        }

    def make_shopify_graphql_request(self, query, variables=None):
        self.__endpoint = f"https://{self.__store_key}.myshopify.com/admin/api/{self.__api_version}/graphql.json"
        data = {
            "query": query,
            "variables": variables,
        }
        response = requests.post(
            self.__endpoint,
            headers=self.__headers,
            data=json.dumps(data),
        )

        return response.json()

    def get_products(self, page_size=20):
        cursor = None
        all_products = []

        while True:
            graphql_query = """
            query ($pageSize: Int!, $cursor: String) {
                products(first: $pageSize, after: $cursor) {
                    edges {
                        node {
                            %s
                            variants(first: 50) {
                                edges {
                                    node {
                                        %s
                                    }
                                }
                            }
                        }
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
            """ % (
                MAIN_NODE_REQUIRED_INFO,
                NODE_REQUIRED_INFO,
            )
            variables = {
                "pageSize": page_size,
                "cursor": cursor,
            }
            response = self.make_shopify_graphql_request(
                graphql_query,
                variables,
            )
            products = (
                response.get("data", {})
                .get("products", {})
                .get(
                    "edges",
                    [],
                )
            )
            all_products.extend(products)
            page_info = (
                response.get("data", {})
                .get("products", {})
                .get(
                    "pageInfo",
                    {},
                )
            )
            has_next_page = page_info.get(
                "hasNextPage",
                False,
            )
            cursor = page_info.get(
                "endCursor",
                None,
            )

            if not has_next_page:
                break

        return all_products

    def create_or_check_folder(self, folder_path):
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"The folder '{folder_path}' has been created.")
            except OSError as e:
                print(f"Error creating the folder '{folder_path}': {e}")
        else:
            print(f"The folder '{folder_path}' already exists.")

    def get_id_from_gid_string(self, string: str):
        splited_string = string.split("/")
        return splited_string[-1]

    def get_extension_from_url(self, url):
        file_path = urlparse(url).path
        file_name, extension = os.path.splitext(file_path)
        return extension

    def store_image_locally(self, src, id):
        try:
            # Generar el nombre del archivo
            extension = self.get_extension_from_url(src)
            name = f"{id}{extension}"

            # Reemplazar caracteres problemáticos en el nombre del archivo
            name = (
                name.replace("..png", ".png")
                .replace("..jpg", ".jpg")
                .replace("..jpeg", ".jpeg")
                .replace("..gif", ".gif")
                .replace("..webp", ".webp")
                .replace("..bmp", ".bmp")
                .replace("..tiff", ".tiff")
                .replace("..svg", ".svg")
                .replace("..ico", ".ico")
            )

            # Verificar si la imagen ya existe localmente
            local_path = os.path.join("media/product/images/", name)
            print(f"Local path: {local_path}")
            if os.path.exists(local_path):
                print(f"La imagen {name} ya existe localmente.")
                return File(open(local_path, "rb"), name=name)

            # Descargar la imagen
            response = requests.get(src)
            # response.raise_for_status()

            # Almacenar la imagen localmente
            with open(local_path, "wb") as file:
                file.write(response.content)

            print(f"La imagen {name} se almacenó localmente correctamente.")

            # Crear y retornar el objeto File
            image = File(open(local_path, "rb"), name=name)
            return image
        except Exception as e:
            print(e)
            return None

    def store_image_locally_old(self, src, id):
        try:
            response = requests.get(src)
            response.raise_for_status()
            extension = self.get_extension_from_url(src)
            name = f"{id}{extension}"
            name = name.replace("..png", ".png")
            name = name.replace("..jpg", ".jpg")
            name = name.replace("..jpeg", ".jpeg")
            name = name.replace("..gif", ".gif")
            name = name.replace("..webp", ".webp")
            name = name.replace("..bmp", ".bmp")
            name = name.replace("..tiff", ".tiff")
            name = name.replace("..svg", ".svg")
            name = name.replace("..ico", ".ico")
            print(f"Image {name} stored successfully.")
            image = File(BytesIO(response.content), name=name)
            return image
        except Exception as e:
            print(e)
            return None

    def delete_image_file(self, file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    def save_artd_images(self, images):
        stored_images = []
        image_list = images.get("edges", [])
        self.create_or_check_folder(LOCAL_PATH)
        for image_node in image_list:
            image = image_node.get("node", {})
            src = image.get("src", None)
            id = self.get_id_from_gid_string(image.get("id", None))
            image_source = {
                "name": "shopify",
                "id": id,
                "partner": self.__partner.id,
            }
            if (
                ShopifyImage.objects.filter(
                    external_id=id,
                    partner=self.__partner,
                ).count()
                == 0
            ):
                local_image = self.store_image_locally(src, id)
                if local_image is not None:
                    image = ShopifyImage.objects.create(
                        image=local_image,
                        alt=f"{id}",
                        external_id=id,
                        partner=self.__partner,
                        source=image_source,
                    )
                    stored_images.append(image)
            else:
                image = ShopifyImage.objects.filter(
                    external_id=id,
                    partner=self.__partner,
                ).first()
                stored_images.append(image)

        return stored_images

    def store_products_from_shopify(self):
        products = self.get_products(250)
        for product in products:
            node = product.get("node", {})
            id = self.get_id_from_gid_string(node.get("id", None))
            title = node.get("title", None)
            if (
                ShopifyProduct.objects.filter(
                    product_id=id,
                    partner=self.__partner,
                ).count()
                == 0
            ):
                shopify_product = ShopifyProduct(
                    product_id=id,
                    json_data=product,
                    partner=self.__partner,
                    name=title,
                )
                shopify_product.save()
            else:
                ShopifyProduct.objects.filter(
                    product_id=id,
                    partner=self.__partner,
                ).update(json_data=product)
        return True

    def get_categories_from_full_name(self, full_name):
        categories = full_name.split(">")
        categories_list = []
        for category in categories:
            category = category.strip()
            categories_list.append(category)
        return categories_list

    def store_categories(self):
        if (
            RootCategory.objects.filter(
                name=self.__vendor,
                partner=self.__partner,
            ).count()
            == 0
        ):
            root_category = RootCategory.objects.create(
                name=self.__vendor,
                partner=self.__partner,
            )
        else:
            root_category = RootCategory.objects.get(
                name=self.__vendor,
                partner=self.__partner,
            )

        first_category = True

        products = ShopifyProduct.objects.all()
        for product in products:
            node = product.json_data.get("node", {})
            category = node.get("productCategory", None)
            print(category)
            tax = Tax.objects.first()
            if category is not None:
                product_taxonomy_node = category.get("productTaxonomyNode", {})
                full_name = product_taxonomy_node.get("fullName", None)
                categories = self.get_categories_from_full_name(full_name)
                print(categories)
                counter = 0
                first_category = True
                for category_name in categories:
                    # ArtD Categories
                    if first_category:
                        artd_first_category_count = Category.objects.filter(
                            name=category_name,
                            root_category=root_category,
                            partner=self.__partner,
                        ).count()
                        print(f"ArtD first category count: {artd_first_category_count}")
                        if artd_first_category_count == 0:
                            category = Category.objects.create(
                                name=category_name,
                                root_category=root_category,
                                partner=self.__partner,
                            )
                            print(f"ArtD category created: {category}")
                        else:
                            print(f"ArtD category found: {category}")
                        first_category = False
                    else:
                        previous_category = Category.objects.filter(
                            name=categories[counter - 1],
                            partner=self.__partner,
                        ).first()
                        if (
                            Category.objects.filter(
                                name=category_name,
                                partner=self.__partner,
                                parent=previous_category,
                            ).count()
                            == 0
                        ):
                            category = Category.objects.create(
                                name=category_name,
                                partner=self.__partner,
                                parent=previous_category,
                            )
                    # Shopify categories
                    if (
                        ShopifyCategory.objects.filter(
                            name=category_name,
                            artd_partner=self.__partner,
                        ).count()
                        == 0
                    ):
                        ShopifyCategory.objects.create(
                            name=category_name,
                            artd_partner=self.__partner,
                            json_data=product_taxonomy_node,
                            artd_tax=tax,
                        )
                    else:
                        ShopifyCategory.objects.filter(
                            name=category_name,
                            artd_partner=self.__partner,
                        ).update(json_data=product_taxonomy_node)
                    counter = counter + 1

    def store_vendors(self):
        products = ShopifyProduct.objects.all()
        for product in products:
            node = product.json_data.get("node", {})
            vendor = node.get("vendor", None)
            if vendor is not None:
                if (
                    ShopifyBrand.objects.filter(
                        name=vendor,
                        artd_partner=self.__partner,
                    ).count()
                    == 0
                ):
                    ShopifyBrand.objects.create(
                        name=vendor,
                        artd_partner=self.__partner,
                    )
                if (
                    Brand.objects.filter(
                        name=vendor,
                    ).count()
                    == 0
                ):
                    Brand.objects.create(
                        name=vendor,
                    )

    def store_products_from_shopify_to_artd(self):
        all_products = ShopifyProduct.objects.all()
        for product in all_products:
            node = product.json_data.get("node", {})
            id = node.get("id", None)
            main_product_id = self.get_id_from_gid_string(id)
            title = node.get("title", None)
            description = node.get("description", None)
            description_html = node.get("descriptionHtml", None)
            images = node.get("images", [])
            handle = node.get("handle", None)
            options = node.get("options", [])
            product_category = node.get("productCategory", None)
            print(product_category)
            product_taxonomy_node = None
            if product_category is not None:
                product_taxonomy_node = product_category.get(
                    "productTaxonomyNode", None
                )
                print(f"product_taxonomy_node: {product_taxonomy_node}")
            seo = node.get("seo", None)
            meta_description = seo.get("description", None)
            meta_description = "" if meta_description is None else meta_description
            meta_title = seo.get("title", None)
            meta_title = "" if meta_title is None else meta_title
            tags = node.get("tags", None)
            vendor = node.get("vendor", None)
            variants = node.get("variants", {}).get("edges", [])
            first_product = True
            option_list = []
            print(f"---->{product_taxonomy_node}")
            if product_taxonomy_node is not None:
                if product_category is None:
                    category = None
                    artd_category = Category.objects.first()
                    tax = Tax.objects.first()
                else:
                    category = ShopifyCategory.objects.filter(
                        name=product_category.get("productTaxonomyNode", {}).get(
                            "name", None
                        ),
                        artd_partner=self.__partner,
                    ).first()
                    artd_category = Category.objects.filter(
                        name=category.name,
                        partner=self.__partner,
                    ).first()
                    tax = category.artd_tax
            else:
                artd_category = None
                tax = Tax.objects.first()
            for option in options:
                id = self.get_id_from_gid_string(option.get("id", None))
                name = option.get("name", None)
                values = option.get("values", [])
                option_list.append(
                    {
                        "id": id,
                        "name": name,
                        "values": values,
                    }
                )

            shopify_images = self.save_artd_images(images)
            variant_products = []
            brand = Brand.objects.filter(name=vendor).first()
            print(f"Brand: {brand}")
            if brand is None:
                brand = Brand.objects.first()
            for variant in variants:
                variant_node = variant.get("node", {})
                variant_id = variant_node.get("id", None)
                variant_id = self.get_id_from_gid_string(variant_id)
                variant_title = variant_node.get("title", None)
                variant_sku = variant_node.get("sku", None)
                variant_price = variant_node.get("price", None)
                variant_weight = variant_node.get("weight", None)
                variant_inventory_quantity = variant_node.get("inventoryQuantity", None)

                if variant_title == "Default Title":
                    variant_title = title

                source = {
                    "name": "shopify",
                    "id": variant_id,
                    "partner": self.__partner.id,
                }
                if first_product:
                    sku = variant_sku
                    first_product = False
                if (
                    Product.objects.filter(
                        partner=self.__partner,
                        external_id=variant_id,
                    ).count()
                    == 0
                ):
                    try:
                        product_obj = Product.objects.create(
                            partner=self.__partner,
                            source=source,
                            json_data=variant,
                            external_id=variant_id,
                            url_key=handle,
                            meta_title=meta_title,
                            meta_description=meta_description,
                            meta_keywords="",
                            type="physical",
                            name=variant_title,
                            tax=tax,
                            sku=variant_sku,
                            description=description_html,
                            short_description=description,
                            weight=variant_weight,
                            unit_of_measure="kg",
                            measure=variant_weight,
                            variations=option_list,
                            brand=brand,
                        )
                        if artd_category is not None:
                            product_obj.categories.add(artd_category)
                            product_obj.save()

                        Stock.objects.create(
                            partner=self.__partner,
                            product=product_obj,
                            stock=variant_inventory_quantity,
                        )
                        PriceList.objects.create(
                            partner=self.__partner,
                            product=product_obj,
                            regular_price=variant_price,
                        )

                    except Exception as e:
                        print(f"Error creating product: {e}")
                        product_obj = None
                else:
                    try:
                        product_obj = Product.objects.filter(
                            partner=self.__partner,
                            external_id=variant_id,
                        ).first()
                        Product.objects.filter(
                            partner=self.__partner,
                            external_id=variant_id,
                        ).update(
                            json_data=variant,
                            url_key=handle,
                            meta_title=meta_title,
                            meta_description=meta_description,
                            meta_keywords="",
                            type="physical",
                            name=variant_title,
                            sku=variant_sku,
                            description=description_html,
                            short_description=description,
                            weight=variant_weight,
                            unit_of_measure="kg",
                            measure=variant_weight,
                            variations=option_list,
                            brand=brand,
                            tax=tax,
                        )
                        if artd_category is not None:
                            product_obj.categories.clear()
                            product_obj.categories.add(artd_category)
                            product_obj.save()

                        Stock.objects.filter(
                            partner=self.__partner,
                            product=product_obj,
                        ).update(stock=variant_inventory_quantity)
                        PriceList.objects.filter(
                            partner=self.__partner,
                            product=product_obj,
                        ).update(regular_price=variant_price)

                    except Exception as e:
                        print(f"Error updating product: {e}")
                        product_obj = None
                if product_obj is not None:
                    variant_products.append(product_obj)

                    for shopify_image in shopify_images:
                        if (
                            ProductImage.objects.filter(
                                product=product_obj,
                                image=shopify_image,
                            ).count()
                            == 0
                        ):
                            source = {
                                "name": "shopify",
                                "id": variant_id,
                                "partner": self.__partner.id,
                            }
                            ProductImage.objects.create(
                                source=source,
                                external_id=variant_id,
                                product=product_obj,
                                image=shopify_image,
                            )

            if (
                GroupedProduct.objects.filter(
                    partner=self.__partner,
                    external_id=main_product_id,
                ).count()
                == 0
            ):
                try:
                    grouped_product_source = {
                        "name": "shopify",
                        "id": main_product_id,
                        "partner": self.__partner.id,
                    }
                    grouped_product = GroupedProduct.objects.create(
                        source=grouped_product_source,
                        json_data=node,
                        external_id=main_product_id,
                        partner=self.__partner,
                        url_key=handle,
                        name=title,
                        sku=sku,
                        description=description_html,
                        short_description=description,
                        variations=options,
                    )
                    for variant_product in variant_products:
                        grouped_product.products.add(variant_product)

                except Exception as e:
                    print(f"Error creating grouped product: {e}")
            else:
                try:
                    grouped_product_source = {
                        "name": "shopify",
                        "id": main_product_id,
                        "partner": self.__partner.id,
                    }
                    grouped_product = GroupedProduct.objects.filter(
                        partner=self.__partner,
                        external_id=main_product_id,
                    ).first()
                    GroupedProduct.objects.filter(
                        partner=self.__partner,
                        external_id=main_product_id,
                    ).update(
                        source=grouped_product_source,
                        json_data=node,
                        url_key=handle,
                        name=title,
                        sku=sku,
                        description=description_html,
                        short_description=description,
                        variations=options,
                    )
                    grouped_product.products.clear()
                    for variant_product in variant_products:
                        grouped_product.products.add(variant_product)

                except Exception as e:
                    print(f"Error updating grouped product: {e}")
            product.processed = True
            product.save()

    def store_tags(self, partner: Partner):
        all_products = ShopifyProduct.objects.all()
        tags_list = []
        for product in all_products:
            node = product.json_data.get("node", {})
            tags = node.get("tags", None)

            for tag in tags:
                print(tag)
                if tag not in tags_list:
                    tags_list.append(tag)

        for tag in tags_list:
            count = ShopifyTag.objects.filter(
                tag=tag,
                artd_partner=partner,
            ).count()
            if count == 0:
                ShopifyTag.objects.create(
                    tag=tag,
                    artd_partner=partner,
                )
                print(f"Tag {tag} created.")
            else:
                print(f"Tag {tag} already exist.")

    def transform_text(self, text):
        parts = text.split("_")
        transformed_text = " ".join(part.capitalize() for part in parts)
        return transformed_text

    def tags_to_categories(self, partner: Partner):
        all_tags = ShopifyTag.objects.values(
            "tag",
            "id",
        ).annotate(tag_count=Count("tag"))
        root_tags = ShopifyRootTag.objects.filter(artd_partner=partner)

        root_tags_dict = {}
        for root_tag in root_tags:
            root_tag_text_base = root_tag.root_tag
            root_tag_text = self.transform_text(root_tag_text_base[:-1])
            root_tags_dict[root_tag_text_base] = {
                "root_category": root_tag.root_category,
                "root_tag_text": root_tag_text,
            }
            if (
                Category.objects.filter(
                    name=root_tag_text,
                    root_category=root_tag.root_category,
                    partner=partner,
                ).count()
                == 0
            ):
                category = Category.objects.create(
                    name=root_tag_text,
                    partner=partner,
                    root_category=root_tag.root_category,
                )

            else:
                category = Category.objects.filter(
                    name=root_tag_text,
                    root_category=root_tag.root_category,
                    partner=partner,
                ).last()

            root_tags_dict[root_tag_text_base]["category"] = category

        for tag in all_tags:
            tag_text = tag["tag"]
            tag_id = tag["id"]
            splited_tag = tag_text.split("_")
            splited_root_tag = f"{splited_tag[0]}_"
            if splited_root_tag in root_tags_dict:
                base_category = self.transform_text(
                    tag_text.replace(splited_root_tag, "")
                )
                if (
                    Category.objects.filter(
                        name=base_category,
                        parent=root_tags_dict[splited_root_tag]["category"],
                        partner=partner,
                    ).count()
                    == 0
                ):
                    category = Category.objects.create(
                        name=base_category,
                        parent=root_tags_dict[splited_root_tag]["category"],
                        partner=partner,
                    )
                    print(f"Category {base_category} created")
                else:
                    category = Category.objects.filter(
                        name=base_category,
                        parent=root_tags_dict[splited_root_tag]["category"],
                        partner=partner,
                    ).last()
                    print(f"Category {base_category} already exist")

                tag_object = ShopifyTag.objects.get(id=tag_id)
                tag_object.category = category
                tag_object.save()

    def update_categories_for_all_products(self):
        all_grouped_products = GroupedProduct.objects.all()
        for grouped_product in all_grouped_products:
            grouped_product_shopify_id = grouped_product.external_id
            shopify_product_queryset = ShopifyProduct.objects.filter(
                product_id=grouped_product_shopify_id,
            )
            if shopify_product_queryset.count() > 0:
                product = shopify_product_queryset.last()
                json_data = product.json_data
                node = json_data.get("node", None)
                if node is not None:
                    id_string = node.get("id", None)
                    splited_id = id_string.split("/")
                    id = splited_id[-1]
                    shopify_product_queryset = ShopifyProduct.objects.filter(
                        product_id=id
                    )
                    if shopify_product_queryset.count() > 0:
                        categories = []
                        category_ids = []
                        shopify_product = shopify_product_queryset.last()
                        json_data = shopify_product.json_data
                        node = json_data.get("node", None)
                        if node is not None:
                            tags = node.get("tags", None)
                            if tags is not None:
                                for tag in tags:
                                    splited_tag = tag.split("_")
                                    if len(splited_tag) > 1:

                                        splited_root_tag = f"{splited_tag[0]}_"
                                        parent_category = self.transform_text(
                                            splited_tag[0]
                                        )
                                        base_category = self.transform_text(
                                            tag.replace(splited_root_tag, "")
                                        )
                                        parent_category_object = (
                                            Category.objects.filter(
                                                name=parent_category,
                                                partner=product.partner,
                                            )
                                        )
                                        if parent_category_object.count() > 0:
                                            parent_category_object = (
                                                parent_category_object.first()
                                            )
                                            base_category_object = (
                                                Category.objects.filter(
                                                    name=base_category,
                                                    partner=product.partner,
                                                    parent=parent_category_object,
                                                )
                                            )
                                            if base_category_object.count() > 0:
                                                base_category_object = (
                                                    base_category_object.first()
                                                )

                                                category_to_add = (
                                                    Category.objects.filter(
                                                        name=base_category,
                                                        partner=product.partner,
                                                        parent=parent_category_object,
                                                    ).first()
                                                )
                                                if (
                                                    category_to_add.id
                                                    not in category_ids
                                                ):
                                                    category_ids.append(
                                                        category_to_add.id
                                                    )
                                                    categories.append(category_to_add)

                            else:
                                print(f"No tags for product {id}")
                    all_products = grouped_product.products.all()

                    for product in all_products:
                        for category in categories:
                            product.categories.add(category)
