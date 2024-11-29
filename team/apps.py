from django.apps import AppConfig
from django.db.models.signals import post_migrate



class TeamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'team'

    def ready(self):
        import os
        from django.core.management import call_command

        def team_load_data(sender, **kwargs):
            if os.path.exists("team/management/command/teams.json"):
                call_command("team_load_data")

        post_migrate.connect(team_load_data, sender=self)