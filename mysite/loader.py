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
        from members.models import Title, ExpertiseField, Role, Profile
        from taggit.models import Tag
        from blog.models import Post
        from research.models import ProjetRecherche
        from faker import Faker

        fake = Faker()


        # Fonction pour créer des titres
        def create_titles():
            for title_choice in Title.TITLE_CHOICES:
                Title.objects.get_or_create(name=title_choice[0])

        # Fonction pour créer des rôles
        def create_roles():
            for role_choice in Role.ROLE_CHOICES:
                Role.objects.get_or_create(name=role_choice[0])



        def create_expertises(max = 10):
            for _ in range(max):
                ExpertiseField.objects.create(
                    name=fake.word(),
                )

        def create_users_with_profiles(max=50):
            for _ in range(max):
                user = User.objects.create(
                    username=fake.user_name(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                )
                
                title = Title.objects.order_by('?').first()
                role = Role.objects.order_by('?').first()
                

                # Créer un profil pour chaque utilisateur
                profile = Profile.objects.create(
                    user=user,
                    biographie=fake.text(max_nb_chars=150),  
                    date_of_birth=fake.date(),
                    website=fake.url(), 
                    google_scholar=fake.url(), 
                    researchgate=fake.url(), 
                    orcid=fake.uuid4(),  
                    linkedin=fake.url(),  
                    twitter=fake.url(), 
                    role=role,
                    title=title  
                )
                # Ajouter des expertises aléatoires au profil
                expertise_fields = ExpertiseField.objects.all()
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

                # Mettre à jour le champ photo du profil
                profile.photo = os.path.join('users', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'), image_file)
                profile.save()



       

        def create_posts(max=70):
            image_folder = 'media/Images'  # Remplacez par le chemin vers votre dossier d'images
            images = os.listdir(image_folder)  # Liste des fichiers d'images dans le dossier
            markdown_folder = 'media/Markdown' 
            markdown_files = [f for f in os.listdir(markdown_folder) if f.endswith('.md')]  



            for _ in range(max):
                title = fake.sentence()
                image_file = random.choice(images)  # Choisir une image aléatoire
                image_path = os.path.join(image_folder, image_file)
                today = datetime.date.today()
                destination_folder = os.path.join('media/blog', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'))
                os.makedirs(destination_folder, exist_ok=True)  # Créer le dossier si il n'existe pas
                destination_path = os.path.join(destination_folder, image_file)
                shutil.copy(image_path, destination_path)

                # Lire le contenu d'un fichier Markdown aléatoire
                markdown_file = random.choice(markdown_files)
                markdown_path = os.path.join(markdown_folder, markdown_file)
                with open(markdown_path, 'r', encoding='utf-8') as f:
                    body_content = f.read()  # Lire le contenu du fichier Markdown

    

                # Créer un post avec l'image
                post =Post.objects.create(
                    title=title,
                    photo=os.path.join('blog', today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'), image_file),
                    author=User.objects.order_by('?').first(),
                    body=body_content,
                    publish=fake.date_time(),
                    status=random.choice(['DF', 'PB']),
                )
                tags = [fake.word() for _ in range(random.randint(1, 5))]  # Générer entre 1 et 5 tags aléatoires
                post.tags.add(*tags)



        def create_projet_recherche(max=55):
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
                members = random.sample(list(Profile.objects.all()), 10)
                for member in members:
                    projet_recherche.members.add(member.id)



        create_titles()  
        create_roles()
        create_expertises(10)
        create_users_with_profiles(50)
        create_posts(70)
        create_projet_recherche(55)
        



    except Exception as err:
       print("Error : "+ str(err))


if __name__ == '__main__':
    main()
