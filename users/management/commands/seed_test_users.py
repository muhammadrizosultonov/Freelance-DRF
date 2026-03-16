from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or reset test users: client1 and freelancer1."

    def handle(self, *args, **options):
        User = get_user_model()
        users = [
            {
                "username": "client1",
                "email": "client1@example.com",
                "password": "client123",
                "role": User.Role.CLIENT,
            },
            {
                "username": "freelancer1",
                "email": "freelancer1@example.com",
                "password": "freelancer123",
                "role": User.Role.FREELANCER,
            },
        ]

        for data in users:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={"email": data["email"], "role": data["role"]},
            )
            updated_fields = []

            if user.email != data["email"]:
                user.email = data["email"]
                updated_fields.append("email")

            if user.role != data["role"]:
                user.role = data["role"]
                updated_fields.append("role")

            user.set_password(data["password"])
            updated_fields.append("password")

            if created:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created {user.username}"))
            else:
                user.save(update_fields=updated_fields)
                self.stdout.write(self.style.WARNING(f"Updated {user.username}"))
