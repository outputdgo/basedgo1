from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from contact.models import ContactSubmission

class Command(BaseCommand):
    help = 'Clean up spam contact submissions and old submissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete submissions older than this many days (default: 30)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
        parser.add_argument(
            '--spam-only',
            action='store_true',
            help='Only delete spam submissions (honeypot field not empty)'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        spam_only = options['spam_only']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Query for submissions to delete
        if spam_only:
            # Delete only spam submissions (honeypot field not empty)
            queryset = ContactSubmission.objects.exclude(honeypot='')
            self.stdout.write(f"Finding spam submissions...")
        else:
            # Delete old submissions (both legitimate and spam)
            queryset = ContactSubmission.objects.filter(created_at__lt=cutoff_date)
            self.stdout.write(f"Finding submissions older than {days} days...")
        
        # Count what we're about to delete
        total_count = queryset.count()
        
        if total_count == 0:
            self.stdout.write(
                self.style.SUCCESS('No submissions found matching criteria.')
            )
            return
        
        # Show details of what will be deleted
        if dry_run:
            self.stdout.write(f"DRY RUN - Would delete {total_count} submissions:")
            for submission in queryset[:10]:  # Show first 10
                spam_indicator = " [SPAM]" if submission.honeypot else ""
                self.stdout.write(f"  - {submission.name} ({submission.email}) - {submission.created_at}{spam_indicator}")
            
            if total_count > 10:
                self.stdout.write(f"  ... and {total_count - 10} more")
                
            self.stdout.write(
                self.style.WARNING(f'Run without --dry-run to actually delete these {total_count} submissions')
            )
        else:
            # Actually delete the submissions
            deleted_count, _ = queryset.delete()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} contact submissions.')
            )
            
            # Log the cleanup
            import logging
            logger = logging.getLogger(__name__)
            if spam_only:
                logger.info(f"Cleaned up {deleted_count} spam contact submissions")
            else:
                logger.info(f"Cleaned up {deleted_count} contact submissions older than {days} days")
