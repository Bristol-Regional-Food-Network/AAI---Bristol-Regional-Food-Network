import os, sys, csv, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.contrib.auth.models import User
from producers.models import Producer
from users.models import UserProfile

PRODUCERS_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DATA', 'producers_dataset.csv')

producer_usernames = []
with open(PRODUCERS_CSV, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        producer_usernames.append(row['username'])

# Step 1: Delete existing producer users
print("Deleting existing producer users...")
deleted = 0
for username in producer_usernames:
    try:
        User.objects.get(username=username).delete()
        print(f"  [DELETED] {username}")
        deleted += 1
    except User.DoesNotExist:
        print(f"  [NOT FOUND] {username} - skipping")

print(f"\n{deleted} users deleted.\n")

# Step 2: Recreate with correct role
# The signal flow is:
#   create_user -> UserProfile created with role='customer'
#   set role='producer' -> signal auto-creates a blank Producer
#   then we update that Producer with the real data
print("Recreating producers with correct role...")
created = 0

with open(PRODUCERS_CSV, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        user = User.objects.create_user(
            username=row['username'],
            email=row['email'],
            password=row['password'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )

        # Setting role to 'producer' triggers the signal which auto-creates a blank Producer
        profile = UserProfile.objects.get(user=user)
        profile.role = 'producer'
        profile.save()

        # Update the auto-created Producer with real data
        Producer.objects.filter(user=user).update(
            display_name=row['display_name'],
            bio=row['bio'],
            location=row['location'],
            postcode=row['postcode'],
            phone=row['phone'],
            website=row['website'],
        )

        print(f"  [OK] {row['display_name']} ({row['username']})")
        created += 1

print(f"\nDone. {created} producers recreated with correct role.")
