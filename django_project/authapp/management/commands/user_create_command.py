from django.core.management.base import BaseCommand
from authapp.models import User
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = 'Create user'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help='How many users create')

    def handle(self, *args, **options):
        for i in range(options['number']):
            User.objects.create_user(username=get_random_string(), email=f'{get_random_string()}@mail.ru', password=f'{get_random_string()}777')
        print('Users add')
