from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Setup live configuration for Render'

    def handle(self, *args, **options):
        # 1. Update Site
        domain = 'personal-bookmark-manager-api.onrender.com'
        site = Site.objects.get_current()
        site.domain = domain
        site.name = 'Bookmark Manager'
        site.save()
        self.stdout.write(self.style.SUCCESS(f'Updated site domain to {domain}'))

        # 2. Setup Social App
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        
        if not client_id or not secret:
            self.stdout.write(self.style.ERROR('GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in environment'))
        else:
            app, created = SocialApp.objects.update_or_create(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': client_id,
                    'secret': secret,
                }
            )
            app.sites.add(site)
            self.stdout.write(self.style.SUCCESS('Configured Google SocialApp'))

        # 3. Create Superuser if not exists
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            self.stdout.write(self.style.NOTICE('Superuser admin already exists'))

        self.stdout.write(self.style.SUCCESS('✅ Live configuration complete!'))
