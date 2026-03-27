from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product
import os
import re
from PIL import Image, ImageDraw, ImageFont


def slugify_name(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    return s


class Command(BaseCommand):
    help = 'Delete existing JPGs in media/product_images and generate placeholder JPGs for each product'

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT or ''
        img_dir = os.path.join(media_root, 'product_images')
        os.makedirs(img_dir, exist_ok=True)

        # Delete existing .jpg/.jpeg files
        deleted = 0
        for fname in os.listdir(img_dir):
            if fname.lower().endswith(('.jpg', '.jpeg')):
                try:
                    os.remove(os.path.join(img_dir, fname))
                    deleted += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not delete {fname}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted} jpg/jpeg files from {img_dir}'))

        # Prepare font (use a default PIL font if no TTF available)
        try:
            font = ImageFont.truetype('arial.ttf', 28)
        except Exception:
            font = ImageFont.load_default()

        generated = 0
        # Create a placeholder image for each product
        for product in Product.objects.all():
            slug = slugify_name(product.name)
            filename = f"{slug}.jpg"
            path = os.path.join(img_dir, filename)

            # create image 800x600 with background color and product name centered
            img = Image.new('RGB', (800, 600), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            text = product.name
            # wrap text if long
            max_width = 40
            lines = []
            words = text.split()
            line = ''
            for w in words:
                if len(line + ' ' + w) <= max_width:
                    line = (line + ' ' + w).strip()
                else:
                    lines.append(line)
                    line = w
            if line:
                lines.append(line)

            # getsize may not exist for FreeTypeFont in some PIL versions; use textbbox fallback
            total_h = 0
            line_sizes = []
            for l in lines:
                try:
                    w, h = font.getsize(l)
                except Exception:
                    bbox = draw.textbbox((0, 0), l, font=font)
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                line_sizes.append((w, h))
                total_h += h
            total_h += (len(lines)-1)*6
            y = (600 - total_h) // 2
            for idx, l in enumerate(lines):
                w, h = line_sizes[idx]
                x = (800 - w) // 2
                draw.text((x, y), l, fill=(30, 30, 30), font=font)
                y += h + 6

            try:
                img.save(path, 'JPEG', quality=85)
                product.image.name = os.path.join('product_images', filename)
                product.save()
                generated += 1
                self.stdout.write(self.style.SUCCESS(f'Generated {filename} for {product.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to generate {filename}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Total generated and assigned: {generated}'))
