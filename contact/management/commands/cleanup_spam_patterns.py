from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from contact.models import ContactSubmission
import re

class Command(BaseCommand):
    help = 'Clean up spam submissions based on known patterns'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Known spam patterns from recent submissions
        spam_patterns = [
            r'.*nib$',  # Names ending in 'nib'
            r'^(leenib|nikita|robertnib|simonnib|georgenib|charlesmic)$',
            r'.*rocketdigitaltech.*',
            r'.*dgtlsolution.*',
            r'sdasddsdsdsdsds',
            r'zekisuquc419',
            r'dinanikolskaya99',
            r'irinademenkova86',
        ]
        
        spam_emails = [
            'nikita.rocketdigitaltech@gmail.com',
            'deepa.dgtlsolution@gmail.com',
            'zekisuquc419@gmail.com',
            'dinanikolskaya99@gmail.com',
            'irinademenkova86@gmail.com',
            'sdasddsdsdsdsds@gmail.com',
        ]
        
        # Find submissions matching spam patterns
        spam_submissions = []
        
        for submission in ContactSubmission.objects.all():
            is_spam = False
            reason = ""
            
            # Check name patterns
            name_lower = submission.name.lower().strip()
            for pattern in spam_patterns:
                if re.match(pattern, name_lower, re.IGNORECASE):
                    is_spam = True
                    reason = f"Name pattern: {submission.name}"
                    break
            
            # Check email patterns
            if not is_spam:
                email_lower = submission.email.lower().strip()
                if email_lower in spam_emails:
                    is_spam = True
                    reason = f"Known spam email: {submission.email}"
                else:
                    for pattern in spam_patterns:
                        if re.search(pattern, email_lower, re.IGNORECASE):
                            is_spam = True
                            reason = f"Email pattern: {submission.email}"
                            break
            
            if is_spam:
                spam_submissions.append((submission, reason))
        
        if not spam_submissions:
            self.stdout.write(
                self.style.SUCCESS('No spam submissions found matching known patterns.')
            )
            return
        
        self.stdout.write(f"Found {len(spam_submissions)} spam submissions:")
        
        if dry_run:
            for submission, reason in spam_submissions:
                self.stdout.write(f"  - {submission.name} ({submission.email}) - {reason}")
            
            self.stdout.write(
                self.style.WARNING(f'Run without --dry-run to actually delete these {len(spam_submissions)} submissions')
            )
        else:
            # Actually delete the spam submissions
            deleted_count = 0
            for submission, reason in spam_submissions:
                self.stdout.write(f"Deleting: {submission.name} ({submission.email}) - {reason}")
                submission.delete()
                deleted_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} spam submissions.')
            )
