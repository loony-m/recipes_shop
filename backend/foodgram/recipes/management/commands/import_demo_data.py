import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    help = "Команда для импорта рецептов из csv"

    def data_ingredients(self):
        path = (settings.BASE_DIR / 'data/ingredients.csv')

        with open(path) as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                Ingredients.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )

    def handle(self, *args, **kwargs):
        self.data_ingredients()
