import time
from django.core.management.base import BaseCommand, CommandError
from dekdjseed.core import create_project_entities


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = '...'
        parser.add_argument('--seed', nargs='?', type=int, default=0, const=0, help=help_text)

    def handle(self, *args, **options):
        try:
            seed = int(options['seed'])
        except ValueError:
            raise CommandError('The value of --seed must be an integer')
        time_begin = time.time()
        create_project_entities(seed)
        print(f'Total cost: {time.time() - time_begin}s')
