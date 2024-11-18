import pandas as pd
from django.core.management.base import BaseCommand
from tabledatacenter.models import DataCountryByEconomic
from datetime import datetime

class Command(BaseCommand):
    help = 'Import data from an Excel file into the DataCountryByEconomic model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        data = pd.read_excel(file_path)

        for _, row in data.iterrows():
            date_obj = pd.to_datetime(row['date']).date()

            # Create or update the database entry
            DataCountryByEconomic.objects.update_or_create(
                country=row['country'],
                topic=row['topic'],
                web=row['web'],
                name=row['name'],
                unit=row['unit'],
                date=date_obj,
                defaults={
                    'data': row['data']
                }
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
