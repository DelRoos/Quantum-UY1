import json
from random import choice
from django.core.management.base import BaseCommand
from research.models import ResearchArea, Project
from team.models import TeamMember

class Command(BaseCommand):
    help = 'Load research data from JSON file'

    def handle(self, *args, **kwargs):
        file_path = "research/management/commands/research.json"

        # Charger le fichier JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        # Charger les domaines de recherche
        self.stdout.write("Loading research areas...")
        for area_data in data['research_areas']:
            area, created = ResearchArea.objects.get_or_create(
                name=area_data['name'],
                defaults={
                    'short_description': area_data['short_description'],
                    'description': area_data['description'],
                    'banner_image': area_data.get('banner_image', ''),
                    'order': area_data.get('order', 0),
                    'is_active': True
                }
            )
            area.tags.set(area_data['tags'])
            area.save()
            self.stdout.write(self.style.SUCCESS(f"  {'Created' if created else 'Updated'}: {area.name}"))

        # Charger les projets
        self.stdout.write("Loading projects...")
        team_members = list(TeamMember.objects.all())  # Récupérer tous les membres en base
        if not team_members:
            self.stderr.write(self.style.ERROR("No team members found in the database. Cannot assign leaders to projects."))
            return

        for project_data in data['projects']:
            try:
                research_area = ResearchArea.objects.get(name=project_data['research_area'])
                leader = choice(team_members)  # Choisir un leader aléatoire parmi les membres
                self.stdout.write(f"Assigning leader {leader.first_name} {leader.last_name} to project '{project_data['title']}'")
            except ResearchArea.DoesNotExist as e:
                self.stderr.write(self.style.ERROR(f"Error loading project {project_data['title']}: {e}"))
                continue

            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={
                    'research_area': research_area,
                    'leader': leader,
                    'status': project_data['status'],
                    'priority': project_data['priority'],
                    'funding_type': project_data['funding_type'],
                    'funding_amount': project_data['funding_amount'],
                    'start_date': project_data['start_date'],
                    'end_date': project_data['end_date'],
                    'summary': project_data['summary'],
                    'description': project_data['description'],
                    'objectives': project_data['objectives'],
                    'expected_results': project_data['expected_results'],
                    'is_public': True
                }
            )
            project.tags.set(project_data['tags'])
            project.save()
            self.stdout.write(self.style.SUCCESS(f"  {'Created' if created else 'Updated'}: {project.title}"))

        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
