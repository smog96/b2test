from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').count() == 0:
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@admin.ru'
            )
            admin.set_password('admin')
            admin.is_active = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no admin exist')