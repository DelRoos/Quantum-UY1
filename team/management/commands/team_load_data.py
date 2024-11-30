import json
import random
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

        # # Chargement des membres
        # for item in data.get("TeamMember", []):
        #     position = Position.objects.get(id=item.pop("position"))
        #     department = Department.objects.get(id=item.pop("department"))
        #     TeamMember.objects.get_or_create(position=position, department=department, **item)
        for item in data.get("TeamMember", []):
            # Récupérer et supprimer les spécialités de l'objet JSON
            specialties_ids = item.pop("specialties", [])
            tags = item.pop("tags", [])

            position_id = item.pop("position")
            try:
                position = Position.objects.get(id=position_id)
            except Position.DoesNotExist:
                # Si la position n'existe pas, prendre une position aléatoire
                position = random.choice(Position.objects.all())
                print(f"Position ID {position_id} introuvable. Assigné aléatoirement à {position.name}.")
            
            department_id = item.pop("department")
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                # Si le département n'existe pas, prendre un département aléatoire
                department = random.choice(Department.objects.all())
                print(f"Département ID {department_id} introuvable. Assigné aléatoirement à {department.name}.")

            # Créer ou récupérer le membre de l'équipe
            team_member, created = TeamMember.objects.get_or_create(
                position=position,
                department=department,
                **item
            )

            # Gérer les relations Many-to-Many pour specialties
            team_member.specialties.set(specialties_ids)
            
            team_member.tags.set(tags)
        
        for item in data.get("Publication", []):
            # Récupérer les IDs des auteurs et des tags
            authors_ids = item.pop("authors", [])
            tags_list = item.pop("tags", [])

            # Créer ou récupérer la publication
            publication, created = Publication.objects.get_or_create(**item)

            # Associer les auteurs (Many-to-Many)
            publication.authors.set(authors_ids)

            # Associer les tags (TaggableManager)
            publication.tags.set(tags_list)
            

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
