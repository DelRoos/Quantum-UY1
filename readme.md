# **README - Laboratoire de Recherche en Physique**

## **Introduction**

Bienvenue dans le projet de gestion du site web du Laboratoire de Recherche en Physique Théorique et Expérimentale. Ce projet utilise **Django**, un framework web Python, pour structurer et gérer les données relatives aux membres, sujets de recherche, et articles de blog. L’objectif principal est de fournir une plateforme intuitive permettant de :

- Présenter les membres et leurs travaux.
- Organiser et publier des articles scientifiques ou vulgarisés.
- Structurer les sujets de recherche et leurs domaines d’application.

---

## **Structure du Projet**

Le projet est divisé en plusieurs applications **Django** :

1. **`members`** : Gestion des membres, leurs titres et domaines d'expertise.
2. **`research`** : Gestion des sujets de recherche, leurs problématiques et méthodologies.
3. **`blog`** : Gestion des articles du blog, leurs catégories et auteurs.

---

## **Installation et Prérequis**

### **Prérequis**

- Python 3.12 ou supérieur
- Django 5 ou supérieur
- PostgreSQL ou SQLite pour la base de données
- Pip (gestionnaire de packages Python)
- Un environnement virtuel Python (recommandé)

### **Étapes d’installation**

1. **Cloner le Référentiel**
   ```bash
   git clone https://github.com/DelRoos/Quantum-UY1.git
   cd Quantum-UY1
   ```

2. **Créer et Activer un Environnement Virtuel**
   ```bash
   python3 -m venv env
   source env/bin/activate  # Sous Windows : env\Scripts\activate
   ```

3. **Installer les Dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la Base de Données**
   - Modifier le fichier `settings.py` dans la section `DATABASES` pour adapter les informations de connexion à votre base de données.

5. **Appliquer les Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer un Superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

7. **Démarrer le Serveur**
   ```bash
   python manage.py runserver
   ```

---

## **Utilisation**

### **1. Interface Administrateur**

L'interface administrateur Django permet de gérer tous les modèles (membres, sujets de recherche, articles, etc.).

- Accédez à l’interface à l’adresse : `http://127.0.0.1:8000/admin`.
- Connectez-vous avec vos identifiants superutilisateur.

### **2. Navigation sur le Site**

#### **Accueil**
- Présentation générale du laboratoire.
- Accès rapide aux sections Équipe, Travaux, Blog et Contact.

#### **Équipe**
- Liste des membres avec leurs rôles, domaines d’expertise et projets associés.

#### **Travaux**
- Présentation des sujets de recherche, leurs problématiques, et les découvertes récentes.

#### **Blog**
- Articles rédigés par les membres sur divers sujets, incluant vulgarisation et annonces importantes.

#### **Contact**
- Formulaire pour contacter le laboratoire et informations de localisation.

---

## **Structure des Applications**

### **1. Application : `members`**

- **Modèles** :
  - `Titre` : Représente les titres ou rôles attribués aux membres.
  - `DomaineExpertise` : Représente les spécialités des membres.
  - `Membre` : Stocke les informations sur les membres du laboratoire.

- **Fonctionnalités Clés** :
  - Ajouter/modifier des membres avec leurs titres et domaines d'expertise.
  - Filtrer et rechercher des membres par spécialité ou rôle.

---

### **2. Application : `research`**

- **Modèles** :
  - `SujetRecherche` : Représente les sujets de recherche.
  - `DomaineApplication` : Représente les domaines d’application des recherches.
  - `SujetMembre` : Relie les membres aux sujets de recherche.

- **Fonctionnalités Clés** :
  - Documenter les problématiques et méthodologies des recherches.
  - Associer les membres et domaines d’application aux sujets.
  - Visualiser les projets en cours et leurs impacts potentiels.

---

### **3. Application : `blog`**

- **Modèles** :
  - `Article` : Stocke les articles du blog.
  - `CategorieArticle` : Représente les catégories des articles.
  - `ArticleAuteur` : Relie les membres aux articles rédigés.

- **Fonctionnalités Clés** :
  - Publier et organiser les articles par catégorie.
  - Afficher les auteurs et leurs contributions.
  - Ajouter des images et utiliser le format Markdown pour rédiger les contenus.

---

## **Arborescence des Fichiers**

```plaintext
quantum_uy1/
├── members/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── members/
├── research/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── research/
├── blog/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── blog/
├── website/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── static/
└── manage.py
```

---

## **Personnalisation**

### **1. Modifier les Couleurs et le Design**
- Les fichiers CSS sont situés dans `project/static/`.
- Modifiez les fichiers HTML dans les répertoires `templates/`.

### **2. Ajouter de Nouvelles Fonctionnalités**
- Créez de nouvelles applications Django pour gérer des entités supplémentaires.
- Ajoutez des vues et des templates pour enrichir l’expérience utilisateur.

---

## **Déploiement**

### **1. Configurer les Variables d’Environnement**
- Utilisez des variables d’environnement pour la configuration de la base de données, la clé secrète, et d'autres paramètres sensibles.

### **2. Préparer les Fichiers Statiques**
```bash
python manage.py collectstatic
```

### **3. Utiliser un Serveur de Production**
- Configurez un serveur comme **Gunicorn** pour exécuter l’application :
  ```bash
  pip install gunicorn
  gunicorn project.wsgi:application
  ```

- Configurez un serveur proxy comme **Nginx** pour gérer les requêtes HTTP.

---

## **Contributions**

Les contributions sont les bienvenues pour améliorer ce projet. Veuillez suivre les étapes suivantes :

1. Forkez le projet.
2. Créez une branche pour vos modifications.
   ```bash
   git checkout -b ma-branche
   ```
3. Effectuez vos modifications et commitez-les.
4. Poussez vos changements.
   ```bash
   git push origin ma-branche
   ```
5. Soumettez une Pull Request.

---

## **Licence**

Ce projet est sous licence [MIT](LICENSE). Vous êtes libre de le réutiliser, modifier et distribuer en respectant les termes de la licence.

---

## **Contact**

Pour toute question ou suggestion, contactez-nous via l'adresse email suivante : **delanoroosvelt733@gmail.com**