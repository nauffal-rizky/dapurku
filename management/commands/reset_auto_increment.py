from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
  help = 'Reset the auto-increment value of a specified MySQL table to 1.'

  def add_arguments(self, parser):
    parser.add_argument(
      'table_name',
      type=str,
      help='The name of the table to reset (e.g., your_app_cart).'
    )

  def handle(self, *args, **options):
    table_name = options['table_name']
    with connection.cursor() as cursor:
      cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
    self.stdout.write(
      self.style.SUCCESS(f'Successfully reset auto-increment for table "{table_name}" to 1.')
    )