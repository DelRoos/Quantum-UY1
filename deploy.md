
Pour déployer un blog développé avec Django sur un VPS Hostinger, suivez les étapes suivantes :

1. **Achat d'un nom de domaine** : Rendez-vous sur le site de Hostinger, recherchez le nom de domaine souhaité, ajoutez-le à votre panier et finalisez l'achat en suivant les instructions fournies.

2. **Choix et configuration du VPS** : Sélectionnez un plan VPS adapté à vos besoins. Hostinger propose des plans VPS avec des configurations variées, par exemple :

   - **KVM 1** : 1 vCPU, 4 Go de RAM, 50 Go d'espace disque NVMe, 4 To de bande passante, à partir de 5,49 € par mois.

   - **KVM 2** : 2 vCPU, 8 Go de RAM, 100 Go d'espace disque NVMe, 8 To de bande passante, à partir de 5,99 € par mois.

   - **KVM 4** : 4 vCPU, 16 Go de RAM, 200 Go d'espace disque NVMe, 16 To de bande passante, à partir de 8,99 € par mois.

   - **KVM 8** : 8 vCPU, 32 Go de RAM, 400 Go d'espace disque NVMe, 32 To de bande passante, à partir de 17,99 € par mois.

   Choisissez le plan qui correspond le mieux à vos besoins en termes de performance et de budget.

3. **Configuration du serveur** : Une fois le VPS acquis, connectez-vous via SSH pour installer les logiciels nécessaires :

   - **Mise à jour du système** : `sudo apt update && sudo apt upgrade -y`

   - **Installation de Python et pip** : `sudo apt install python3 python3-pip -y`

   - **Installation de virtualenv** : `sudo pip3 install virtualenv`

   - **Installation de Git** : `sudo apt install git -y`

4. **Déploiement de l'application Django** :

   - **Clonage du projet** : Utilisez Git pour cloner votre projet sur le serveur.

   - **Création d'un environnement virtuel** : `virtualenv venv` puis activez-le avec `source venv/bin/activate`.

   - **Installation des dépendances** : `pip install -r requirements.txt`

   - **Migrations de la base de données** : `python manage.py migrate`

   - **Collecte des fichiers statiques** : `python manage.py collectstatic`

5. **Configuration du serveur web** :

   - **Installation de Gunicorn** : `pip install gunicorn`

   - **Lancement de l'application** : `gunicorn --workers 3 nom_du_projet.wsgi:application`

   - **Installation de Nginx** : `sudo apt install nginx -y`

   - **Configuration de Nginx** : Créez un fichier de configuration pour votre site dans `/etc/nginx/sites-available/` et créez un lien symbolique vers `/etc/nginx/sites-enabled/`. Assurez-vous que Nginx pointe vers Gunicorn.

6. **Sécurisation du site** :

   - **Installation de Certbot** : `sudo apt install certbot python3-certbot-nginx -y`

   - **Obtention d'un certificat SSL** : `sudo certbot --nginx` et suivez les instructions pour obtenir et installer le certificat SSL.

En ce qui concerne les coûts, ils se décomposent comme suit :

- **Nom de domaine** : Le prix varie en fonction de l'extension choisie (.com, .fr, etc.) et des promotions en cours.

- **Hébergement VPS** : Les plans commencent à partir de 5,49 € par mois pour le plan KVM 1.

- **Certificat SSL** : Hostinger offre des certificats SSL gratuits avec ses plans VPS.

Veuillez noter que ces prix sont susceptibles de changer en fonction des promotions et des conditions de Hostinger.

Pour une démonstration visuelle du processus de déploiement, vous pouvez consulter la vidéo suivante :



Cette vidéo offre une formation complète et pratique sur le déploiement d'une application Django en utilisant Docker, Nginx et un serveur VPS. 

https://www.hostinger.com/tutorials/django-tutorial