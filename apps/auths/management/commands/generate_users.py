# apps/auths/management/commands/generate_users.py
import random
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker
from apps.auths.models import CustomUser

class Command(BaseCommand):
    help = 'Generate 10,000 fake user records using bulk_create'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default = 5000,
            help='Total number of users to create (default: 5000)',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=500,
            help='Batch size for bulk_create (default: 500)',
        )

    def handle(self, *args, **options):
        total_users = options['total']
        batch_size = options['batch_size']
        
        DEPARTMENTS = [
            'IT', 'HR', 'Sales', 'Finance', 'Marketing', 
            'Operations', 'Engineering', 'Support'
        ]
        
        ROLES = ['admin', 'manager', 'employee']
        
        SALARY_RANGES = {
            'admin': (60000, 120000),
            'manager': (50000, 90000),
            'employee': (30000, 70000),
        }
        POPULAR_DOMAINS = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
            'aol.com', 'icloud.com', 'protonmail.com', 'mail.com',
            'yandex.com', 'zoho.com', 'gmx.com', 'hubspot.com'
        ]
        COMPANY_DOMAINS = [
            'company.com', 'corporation.com', 'business.com', 
            'enterprise.com', 'tech.com', 'solutions.com',
            'global.com', 'innovations.com', 'group.com', 'ltd.com'
        ]
        ALL_DOMAINS = POPULAR_DOMAINS + COMPANY_DOMAINS
        
        fake = Faker()
        password = "12345"
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Starting to generate {total_users} users in batches of {batch_size}...'
            )
        )
        
        users_created = 0
        batch_count = 0
        
        for i in range(0, total_users, batch_size):
            current_batch_size = min(batch_size, total_users - users_created)
            batch_users = []
            
            try:
                with transaction.atomic():
                    for j in range(current_batch_size):
                        first_name = fake.first_name()
                        last_name = fake.last_name()
                        full_name = f"{first_name} {last_name}"
                        
                        unique_id = users_created + j + 1
                        
                        domain = random.choice(ALL_DOMAINS)
                        
                        email_format = random.choice([
                            f"{first_name.lower()}.{last_name.lower()}",  # john.doe
                            f"{first_name.lower()}{last_name.lower()}",   # johndoe
                            f"{first_name[0].lower()}{last_name.lower()}", # jdoe
                            f"{first_name.lower()}_{last_name.lower()}",   # john_doe
                            f"{last_name.lower()}.{first_name.lower()}",   
                        ])
                        
                        if random.random() < 0.3:
                            random_num = random.randint(1, 999)
                            email_format = f"{email_format}{random_num}"
                        
                        email = f"{email_format}@{domain}"
                        
                        phone = f"1{fake.random_number(digits=10, fix_len=True)}"
                        
                        country = fake.country()[:255]
                        city = fake.city()
                        department = random.choice(DEPARTMENTS)
                        role = random.choice(ROLES)
                        
                        birth_date = fake.date_between_dates(
                            date_start=date(1975, 1, 1), 
                            date_end=date(2005, 12, 31)
                        )
                        
                        min_salary, max_salary = SALARY_RANGES[role]
                        salary = random.randint(min_salary, max_salary)
                        
                        user = CustomUser(
                            email=email,
                            full_name=full_name,
                            phone=phone,
                            country=country,
                            department=department,
                            role=role,
                            birth_date=birth_date,
                            salary=salary,
                            is_active=True,
                            is_staff=(role == 'admin'), 
                            is_superuser=(role == 'admin'),
                        )
                        user.set_password(password)
                        batch_users.append(user)
                    
                    CustomUser.objects.bulk_create(batch_users, batch_size=batch_size)
                    
                    users_created += current_batch_size
                    batch_count += 1
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Batch {batch_count}: Created {current_batch_size} users '
                            f'({users_created}/{total_users})'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error in batch {batch_count}: {str(e)}')
                )
                if hasattr(fake, 'unique'):
                    fake.unique.clear()
                break
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {users_created} users in {batch_count} batches!'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                f'All users have password: {password}'
            )
        )