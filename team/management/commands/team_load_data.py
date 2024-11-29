import json
from django.core.management.base import BaseCommand
from team.models import Department, Position, TeamMember, Specialty, Publication, Award, Education, Experience

class Command(BaseCommand):
    help = "Charge les données initiales depuis un fichier JSON."

    def handle(self, *args, **kwargs):
        with open("team/management/commands/teams.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Chargement des départements
        for item in data.get("Department", []):
            Department.objects.get_or_create(**item)

        # Chargement des positions
        for item in data.get("Position", []):
            Position.objects.get_or_create(**item)

        # Chargement des spécialités
        for item in data.get("Specialty", []):
            Specialty.objects.get_or_create(**item)

        # Chargement des membres
        for item in data.get("TeamMember", []):
            position = Position.objects.get(id=item.pop("position"))
            department = Department.objects.get(id=item.pop("department"))
            TeamMember.objects.get_or_create(position=position, department=department, **item)

        # Chargement des publications
        for item in data.get("Publication", []):
            authors = item.pop("authors")
            publication = Publication.objects.get_or_create(**item)[0]
            publication.authors.set(authors)

        # Chargement des prix
        for item in data.get("Award", []):
            recipient = TeamMember.objects.get(id=item.pop("recipient"))
            Award.objects.get_or_create(recipient=recipient, **item)

        # Chargement des formations
        for item in data.get("Education", []):
            member = TeamMember.objects.get(id=item.pop("member"))
            Education.objects.get_or_create(member=member, **item)

        # Chargement des expériences
        for item in data.get("Experience", []):
            member = TeamMember.objects.get(id=item.pop("member"))
            Experience.objects.get_or_create(member=member, **item)

        self.stdout.write(self.style.SUCCESS("Données initiales chargées avec succès."))
