# import csv
# from django.core.management.base import BaseCommand
# from electricity.models import Product, MarketData
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Load sample CSV data into MarketData model'

#     def add_arguments(self, parser):
#         parser.add_argument('csv_file', type=str)

#     def handle(self, *args, **kwargs):
#         csv_file = kwargs['csv_file']
#         with open(csv_file, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 product, _ = Product.objects.get_or_create(name=row['product'])
#                 MarketData.objects.update_or_create(
#                     product=product,
#                     date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
#                     interval=int(row['interval']),
#                     defaults={
#                         'purchase_bid': float(row['purchase_bid']),
#                         'sell_bid': float(row['sell_bid']),
#                         'mcp': float(row['mcp']),
#                         'mcv': float(row['mcv']),
#                     }
#                 )
#         self.stdout.write(self.style.SUCCESS('Sample data loaded successfully.'))

import pandas as pd
from django.core.management.base import BaseCommand
from electricity.models import Product, MarketData  # replace with your actual model
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample data from an Excel or CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            else:
                self.stdout.write(self.style.ERROR('Unsupported file type.'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load file: {e}"))
            return

        for _, row in df.iterrows():
            try:
                # Replace with your actual column names and model logic
                date_str = str(row['Date']).strip()
                time_block = str(row['Time Block']).split('-')[0].strip()
                timestamp = datetime.strptime(f"{date_str} {time_block}", "%d-%m-%Y %H:%M")

                Product.objects.update_or_create(
                    timestamp=timestamp,
                    defaults={
                        'purchase_bid': row['Purchase Bid'],
                        'sell_bid': row['Sell Bid'],
                        # add other fields here
                    }
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Skipped row due to error: {e}"))

        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
