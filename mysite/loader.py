#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import django
import sys
import shutil
import random
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


def main():
    """Run administrative tasks."""
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    try:
        from django.contrib.auth.models import User
        from administrateur.models import Title, ExpertiseField
        from members.models import Profile
        from blog.models import Post
        from research.models import ProjetRecherche
        from faker import Faker

        fake = Faker()

        def create_users(max = 10):
            for _ in range(max):
                User.objects.create(
                    username = fake.user_name(),
                    first_name = fake.first_name(),
                    last_name = fake.last_name(),
                    email = fake.email(),
                )

        def create_expertises(max = 10):
            for _ in range(max):
                ExpertiseField.objects.create(
                    name=fake.word(),
                )

        def create_profiles(max=10):
            expertise_fields = ExpertiseField.objects.all()
            for _ in range(max):
                user = User.objects.order_by('?').first()
                try:
                    profile = Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    profile = Profile.objects.create(
                        user=user,
                        title=Title.objects.order_by('?').first(),
                        date_of_birth=fake.date(),
                    )
                    profile.expertise.add(*random.sample(list(expertise_fields), random.randint(1, 5)))

                    # Copier une image dans le dossier MEDIA_ROOT
                    image_folder = 'media/Images'  # Remplacez par le chemin vers votre dossier d'images
                    images = os.listdir(image_folder)  # Liste des fichiers d'images dans le dossier
                    image_file = random.choice(images)  # Choisir une image aléatoire
                    image_path = os.path.join(image_folder, image_file)
                    today = datetime.date.today()
                    destination_folder = os.path.join('media/users', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'))
                    os.makedirs(destination_folder, exist_ok=True)  # Créer le dossier si il n'existe pas
                    destination_path = os.path.join(destination_folder, image_file)
                    shutil.copy(image_path, destination_path)

                    # Mettre à jour le champ photo du profile
                    profile.photo = os.path.join('users', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'), image_file)
                    profile.save()




        def create_posts(max=20):
            image_folder = 'media/Images'  # Remplacez par le chemin vers votre dossier d'images
            images = os.listdir(image_folder)  # Liste des fichiers d'images dans le dossier

            for _ in range(max):
                title = fake.sentence()
                image_file = random.choice(images)  # Choisir une image aléatoire
                image_path = os.path.join(image_folder, image_file)
                today = datetime.date.today()
                destination_folder = os.path.join('media/blog', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'))
                os.makedirs(destination_folder, exist_ok=True)  # Créer le dossier si il n'existe pas
                destination_path = os.path.join(destination_folder, image_file)
                shutil.copy(image_path, destination_path)

                # Créer un post avec l'image
                Post.objects.create(
                    title=title,
                    photo=os.path.join('blog', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'), image_file),
                    author=User.objects.order_by('?').first(),
                    body=fake.text(),
                    publish=fake.date_time(),
                    status=random.choice(['DF', 'PB']),
                )

        def create_projet_recherche(max=20):
            image_folder = 'media/Images'  # Remplacez par le chemin vers votre dossier d'images
            images = os.listdir(image_folder)  # Liste des fichiers d'images dans le dossier

            for _ in range(max):
                titre = fake.sentence()
                image_file = random.choice(images)  # Choisir une image aléatoire
                image_path = os.path.join(image_folder, image_file)
                today = datetime.date.today()
                destination_folder = os.path.join('media/research', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'))
                os.makedirs(destination_folder, exist_ok=True)  # Créer le dossier si il n'existe pas
                destination_path = os.path.join(destination_folder, image_file)
                shutil.copy(image_path, destination_path)

                # Créer un projet de recherche avec l'image
                projet_recherche = ProjetRecherche.objects.create(
                    titre=titre,
                    photo=os.path.join('research', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'), image_file),
                    problematique=fake.text(),
                    methode_recherche=fake.text(),
                    domaines_application=fake.text(),
                    resultats_impacts=fake.text(),
                    resumé=fake.text(),
                )
                members = random.sample(list(Profile.objects.all()), 5)
                for member in members:
                    projet_recherche.members.add(member.id)

        # create_users(10)
        # create_expertises(10)
        # create_profiles(10)
        # create_posts(20)
        create_projet_recherche(20)
        



    except Exception as err:
       print("Error : "+ str(err))


if __name__ == '__main__':
    main()
