# filepath: /Users/admin/Desktop/output/django/outreach/management/commands/generate_fake_posts.py
from django.core.management.base import BaseCommand
from outreach.models import OutreachPost
from faker import Faker

class Command(BaseCommand):
    help = 'Generate fake outreach posts for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake posts to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        for _ in range(count):
            OutreachPost.objects.create(
                title=fake.sentence(nb_words=6),
                description=fake.paragraph(nb_sentences=3),
                date=fake.date_time_this_year(),
                slug=fake.slug(),
                body=fake.text(max_nb_chars=700),
            )

        self.stdout.write(self.style.SUCCESS(f'{count} fake outreach posts created successfully!'))