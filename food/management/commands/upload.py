from django.core.management.base import BaseCommand, CommandError
import csv
from food.models import Food

class Command(BaseCommand):
    help = 'Load a food from csv file into database'

    def add_arguments(self,parser):
        parser.add_argument('--path', type=str)

    def handle(self,*args, **kwargs):
        path= kwargs['path']
        with open(path, 'rt',encoding='iso-8859-2') as f:
            reader = csv.reader(f, delimiter=';',dialect='excel')
            for row in reader:
                print(row)
                food = Food.objects.create(
                    name=row[0],
                    category=row[1],
                    quantity=row[2],
                    kcal=row[3],
                    proteins=row[4],
                    carbs=row[5],
                    fats=row[6],
                    fiber=row[7]
                )