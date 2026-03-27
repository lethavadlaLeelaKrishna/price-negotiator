from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product
import os
import re
import difflib


class Command(BaseCommand):
    help = 'Assign product images from media/product_images to products based on name'

    def handle(self, *args, **options):
        media_dir = os.path.join(settings.MEDIA_ROOT or '', 'product_images')
        if not os.path.isdir(media_dir):
            self.stdout.write(self.style.ERROR(f'No media product_images directory found at {media_dir}'))
            return

        files = os.listdir(media_dir)
        if not files:
            self.stdout.write(self.style.ERROR('No files found in product_images'))
            return

        # Map lowercased filenames to original filename
        files_map = {f.lower(): f for f in files}
        bases = [os.path.splitext(f.lower())[0] for f in files]

        assigned = 0
        for product in Product.objects.all():
            if product.image:
                continue

            # Normalize product name to hyphenated lowercase alnum
            name_norm = re.sub(r'[^a-z0-9\-]', '', re.sub(r'\s+', '-', product.name.lower()))

            chosen = None

            # Exact match on base filename
            for fname_lower, fname_orig in files_map.items():
                if os.path.splitext(fname_lower)[0] == name_norm:
                    chosen = fname_orig
                    break

            # Try underscore variant
            if not chosen:
                name_underscore = name_norm.replace('-', '_')
                for fname_lower, fname_orig in files_map.items():
                    if os.path.splitext(fname_lower)[0] == name_underscore:
                        chosen = fname_orig
                        break

            # Fallback: fuzzy match on base names
            if not chosen:
                close = difflib.get_close_matches(name_norm, bases, n=1, cutoff=0.6)
                if close:
                    for f in files:
                        if os.path.splitext(f.lower())[0] == close[0]:
                            chosen = f
                            break

            # Final heuristic: token intersection scoring (e.g., 'laptop' in 'laptop-pro-15')
            if not chosen:
                name_tokens = set([t for t in re.split(r'[-_\s]+', name_norm) if t])
                best_score = 0
                best_file = None
                for f in files:
                    base = os.path.splitext(f.lower())[0]
                    file_tokens = set([t for t in re.split(r'[-_\s]+', base) if t])
                    score = len(name_tokens & file_tokens)
                    if score > best_score:
                        best_score = score
                        best_file = f
                if best_score >= 1 and best_file:
                    chosen = best_file

            if chosen:
                # assign relative path within MEDIA_ROOT
                product.image.name = os.path.join('product_images', chosen)
                product.save()
                assigned += 1
                self.stdout.write(self.style.SUCCESS(f'Assigned {chosen} -> {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'No match for {product.name}'))

        self.stdout.write(self.style.SUCCESS(f'Total images assigned: {assigned}'))
