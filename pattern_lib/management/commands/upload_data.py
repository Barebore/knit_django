import os
from contextlib import ExitStack
from random import randint

from django.core.files import File
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from PIL import Image

from ...models import Category, Pattern


def crop_image_square(image_path, input_image_dir):
    img = Image.open(image_path)
    width, height = img.size
    new_size = min(width, height)

    left = 0
    bottom = height - new_size
    right = left + new_size
    top = height
    img = img.crop((left, bottom, right, top))
    filename = input_image_dir + os.path.splitext(os.path.basename(image_path))[0] + '_mini.jpg'
    img.save(filename)
    return filename



class Command(BaseCommand):
    help = 'Loads data from information.txt and saves to models'

    def handle(self, *args, **options):
        file_path = 'information.txt'
        image_dir = 'upload_image/'

        with ExitStack() as stack:
            f = stack.enter_context(open(file_path, 'r'))
            for line in f:
                nothing_number, title, category_title = line.strip().split('. ')
                pattern_description = next(f).strip()
                self.stdout.write(self.style.SUCCESS(f'Loading data for {nothing_number},, {title} and {category_title}'))
                
                category, created = Category.objects.get_or_create(title=category_title)
                pattern = Pattern.objects.create(
                    title=title,
                    category=category,
                    pattern_description=pattern_description,
                    pattern = ImageFile(open(image_dir + f'{nothing_number}.00.jpg', 'rb')),
                    #mini_pattern = ImageFile(open(crop_image_square(image_dir + f'{nothing_number}.00.jpg', image_dir), 'rb')),
                    scheme = ImageFile(open(image_dir + f'{nothing_number}.10.jpg', 'rb')),
                    scheme_description = ImageFile(open(image_dir + f'{nothing_number}.11.jpg', 'rb')),
                )
                pattern.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
