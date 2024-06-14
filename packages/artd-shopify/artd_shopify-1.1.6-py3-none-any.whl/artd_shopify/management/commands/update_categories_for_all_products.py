from django.core.management.base import BaseCommand
from artd_partner.models import Partner
from artd_shopify.utils.shopify_graphql import ShopifyGraphQl


class Command(BaseCommand):
    help = "Update categories in all products for a specific partner"

    def add_arguments(self, parser):
        # Define aquí los parámetros del comando
        parser.add_argument("partner_slug", type=str, help="Partner slug")

    def handle(self, *args, **kwargs):
        partner_slug = kwargs["partner_slug"]
        partner_slug = partner_slug.split("=")[1]
        print(partner_slug)
        try:
            partner = Partner.objects.filter(
                partner_slug=partner_slug,
            ).first()
            sgq = ShopifyGraphQl(partner)
            sgq.update_categories_for_all_products()
            self.stdout.write(self.style.SUCCESS("Categories updated"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
