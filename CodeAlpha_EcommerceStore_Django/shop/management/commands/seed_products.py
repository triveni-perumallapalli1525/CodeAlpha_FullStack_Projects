from django.core.management.base import BaseCommand
from shop.models import Product
class Command(BaseCommand):
    help = "Create sample ShopLite products"
    def handle(self, *args, **options):
        products = [
            ("Wireless Headphones", "Comfortable wireless headphones for music, study and calls.", "1499.00", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"),
            ("Everyday Backpack", "A practical backpack for college, travel and everyday essentials.", "899.00", "https://images.unsplash.com/photo-1553062407-98eeb64c6a62"),
            ("Classic Watch", "A clean, simple watch design for daily use.", "1199.00", "https://images.unsplash.com/photo-1523275335684-37898b6baf30"),
            ("Desk Lamp", "A compact desk lamp for reading and working.", "699.00", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c"),
            ("Coffee Mug", "A sturdy ceramic mug for your favourite hot drink.", "249.00", "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d"),
            ("Running Shoes", "Lightweight everyday shoes for walking and casual running.", "1899.00", "https://images.unsplash.com/photo-1542291026-7eec264c27ff"),
        ]
        created = 0
        for name, description, price, image_url in products:
            _, was_created = Product.objects.get_or_create(name=name, defaults={"description": description, "price": price, "image_url": image_url, "stock": 20})
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Sample data ready. Created {created} new products."))
