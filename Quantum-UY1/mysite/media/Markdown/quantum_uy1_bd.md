
## **1. Modèle `Titre`**

### **Description :**
Représente les titres ou rôles attribués aux membres. Ces titres peuvent indiquer leur position hiérarchique ou leur rôle dans le laboratoire (ex. : Dr., Professeur, Postdoctorant).

### **Champs :**

| Champ         | Type           | Description                                         |
|---------------|----------------|-----------------------------------------------------|
| `id`         | INT (PK, AI)  | Identifiant unique du titre.                        |
| `nom`        | VARCHAR(50)   | Nom du titre, par exemple : "Dr.", "Professeur".     |
| `created_at` | DATETIME      | Date de création du titre (géré automatiquement).   |
| `updated_at` | DATETIME      | Date de dernière modification du titre.            |

### **Relations :**
- **1:N** avec `Membre` : Un titre peut être associé à plusieurs membres.

### **Exemple de contenu :**

| id  | nom           | created_at          | updated_at          |
|-----|---------------|---------------------|---------------------|
| 1   | Dr.           | 2024-11-01 10:00:00| 2024-11-10 15:00:00|
| 2   | Professeur    | 2024-11-02 11:00:00| 2024-11-10 15:00:00|
| 3   | Postdoctorant | 2024-11-03 12:00:00| 2024-11-10 15:00:00|

---

## **2. Modèle `DomaineExpertise`**

### **Description :**
Représente les différents domaines d'expertise des membres, tels que leurs spécialités scientifiques ou techniques (ex. : "Physique Quantique", "Astrophysique").

### **Champs :**

| Champ         | Type           | Description                                         |
|---------------|----------------|-----------------------------------------------------|
| `id`         | INT (PK, AI)  | Identifiant unique du domaine d'expertise.          |
| `nom`        | VARCHAR(255)  | Nom du domaine, par exemple : "Physique Quantique".  |
| `created_at` | DATETIME      | Date de création du domaine.                        |
| `updated_at` | DATETIME      | Date de dernière modification du domaine.           |

### **Relations :**
- **M:N** avec `Membre` via `MembreDomaine` : Un membre peut avoir plusieurs domaines d'expertise, et un domaine peut être attribué à plusieurs membres.

### **Exemple de contenu :**

| id  | nom                       | created_at          | updated_at          |
|-----|---------------------------|---------------------|---------------------|
| 1   | Physique Quantique        | 2024-11-01 10:00:00| 2024-11-10 15:00:00|
| 2   | Astrophysique             | 2024-11-02 11:00:00| 2024-11-10 15:00:00|
| 3   | Nanotechnologies          | 2024-11-03 12:00:00| 2024-11-10 15:00:00|

---

## **3. Modèle `Membre`**

### **Description :**
Représente les chercheurs et contributeurs travaillant dans le laboratoire. Les membres ont des titres, des domaines d'expertise et peuvent contribuer à des sujets de recherche ou rédiger des articles.

### **Champs :**

| Champ               | Type           | Description                                                  |
|---------------------|----------------|--------------------------------------------------------------|
| `id`               | INT (PK, AI)  | Identifiant unique du membre.                               |
| `prenom`           | VARCHAR(100)  | Prénom du membre.                                            |
| `nom`              | VARCHAR(100)  | Nom de famille du membre.                                    |
| `email`            | VARCHAR(150)  | Adresse email professionnelle (unique).                     |
| `telephone`        | VARCHAR(20)   | Numéro de téléphone (optionnel).                            |
| `photo`            | TEXT          | URL de la photo de profil (peut être null).                 |
| `titre_id`         | INT (FK)      | Référence au titre du membre (`Titre.id`).                  |
| `created_at`       | DATETIME      | Date de création de l'enregistrement.                       |
| `updated_at`       | DATETIME      | Dernière modification de l'enregistrement.                  |

### **Relations :**
- **1:N** avec `Titre` : Un membre a un seul titre.
- **M:N** avec `DomaineExpertise` via `MembreDomaine`.
- **M:N** avec `Article` via `ArticleAuteur`.
- **M:N** avec `SujetRecherche` via `SujetMembre`.

### **Exemple de contenu :**

| id  | prenom  | nom      | email                       | titre_id | created_at          | updated_at          |
|-----|---------|----------|-----------------------------|----------|---------------------|---------------------|
| 1   | Anne    | Martin   | anne.martin@lab.com         | 1        | 2024-11-01 10:00:00| 2024-11-10 15:00:00|
| 2   | Paul    | Dupont   | paul.dupont@lab.com         | 2        | 2024-11-02 11:00:00| 2024-11-10 15:00:00|

---

## **4. Modèle `SujetRecherche`**

### **Description :**
Représente les projets ou sujets de recherche dans le laboratoire, incluant la définition du problème, la méthodologie et les domaines d'application.

### **Champs :**

| Champ                | Type           | Description                                                  |
|----------------------|----------------|--------------------------------------------------------------|
| `id`                | INT (PK, AI)  | Identifiant unique du sujet de recherche.                   |
| `titre`             | VARCHAR(255)  | Titre du sujet de recherche.                                |
| `probleme`          | TEXT          | Description du problème que le sujet cherche à résoudre.    |
| `methodologie`      | TEXT (NULL)   | Description de la méthodologie envisagée.                   |
| `description`       | TEXT          | Résumé général du sujet au format Markdown.                 |
| `date_debut`        | DATE          | Date de début du sujet.                                     |
| `date_fin`          | DATE (NULL)   | Date de fin (peut être null si le projet est en cours).     |
| `created_at`        | DATETIME      | Date de création de l'enregistrement.                       |
| `updated_at`        | DATETIME      | Dernière modification de l'enregistrement.                  |

### **Relations :**
- **M:N** avec `Membre` via `SujetMembre`.
- **M:N** avec `DomaineApplication` via `SujetDomaineApplication`.

### **Exemple de contenu :**

| id  | titre                        | probleme                          | methodologie         | date_debut | date_fin  | created_at          | updated_at          |
|-----|------------------------------|-----------------------------------|----------------------|------------|-----------|---------------------|---------------------|
| 1   | Étude des Particules Subatomiques | Comprendre les interactions fondamentales. | Analyse des collisions dans des accélérateurs. | 2024-01-01 | NULL      | 2024-11-01 10:00:00| 2024-11-10 15:00:00|

---

## **5. Modèle `DomaineApplication`**

### **Description :**
Représente les domaines dans lesquels les résultats des sujets de recherche peuvent être appliqués.

### **Champs :**

| Champ         | Type           | Description                              |
|---------------|----------------|------------------------------------------|
| `id`         | INT (PK, AI)  | Identifiant unique du domaine d'application. |
| `nom`        | VARCHAR(255)  | Nom du domaine, par exemple : "Médecine". |
| `created_at` | DATETIME      | Date de création.                        |
| `updated_at` | DATETIME      | Date de dernière modification.           |

### **Relations :**
- **M:N** avec `SujetRecherche` via `SujetDomaineApplication`.

### **Exemple de contenu :**

| id  | nom             | created_at          | updated_at          |
|-----|-----------------|---------------------|---------------------|
| 1   | Médecine        | 2024-11-01 10:00:00| 2024-11-10 15:00:00|
| 2   | Informatique    | 2024-11-02 11:00:00| 2024-11-10 15:00:00|

### **6. Modèle `CategorieArticle`**

### **Description :**
Représente les catégories des articles de blog. Chaque article peut être associé à une ou plusieurs catégories.

### **Champs :**

| Champ         | Type           | Description                              |
|---------------|----------------|------------------------------------------|
| `id`         | INT (PK, AI)  | Identifiant unique de la catégorie.       |
| `nom`        | VARCHAR(255)  | Nom de la catégorie (exemple : "Physique", "Astrophysique"). |
| `created_at` | DATETIME      | Date de création.                        |
| `updated_at` | DATETIME      | Date de dernière modification.           |

### **Relations :**
- **M:N** avec `Article` via la table pivot `ArticleCategorie`.

---

### **7. Modèle `Article`**

### **Description :**
Représente les articles de blog rédigés par les membres. Les articles peuvent être classés dans des catégories et avoir plusieurs auteurs.

### **Champs :**

| Champ               | Type           | Description                                                  |
|---------------------|----------------|--------------------------------------------------------------|
| `id`               | INT (PK, AI)  | Identifiant unique de l'article.                            |
| `titre`            | VARCHAR(255)  | Titre de l'article.                                          |
| `contenu`          | TEXT          | Contenu complet de l'article au format Markdown.            |
| `image_principale` | TEXT (NULL)   | URL de l'image principale de l'article.                     |
| `date_publication` | DATE          | Date de publication de l'article.                          |
| `slug`             | VARCHAR(255)  | Slug (URL-friendly) généré à partir du titre.               |
| `created_at`       | DATETIME      | Date de création de l'article.                              |
| `updated_at`       | DATETIME      | Dernière modification de l'article.                         |

### **Relations :**
- **M:N** avec `Membre` via `ArticleAuteur` : Un article peut avoir plusieurs auteurs.
- **M:N** avec `CategorieArticle` via `ArticleCategorie` : Un article peut appartenir à plusieurs catégories.

---

### **8. Modèle `ArticleAuteur`**

### **Description :**
Table pivot pour relier les membres (`Membre`) aux articles qu'ils ont rédigés.

### **Champs :**

| Champ              | Type           | Description                                                  |
|--------------------|----------------|--------------------------------------------------------------|
| `id`              | INT (PK, AI)  | Identifiant unique de la relation.                          |
| `article_id`      | INT (FK)      | Référence à l'article (`Article.id`).                       |
| `membre_id`       | INT (FK)      | Référence au membre (`Membre.id`).                          |
| `role`            | VARCHAR(100)  | Rôle dans l'article (exemple : "Auteur principal").          |
| `created_at`      | DATETIME      | Date de création de la relation.                            |
| `updated_at`      | DATETIME      | Dernière modification de la relation.                       |

---

### **9. Modèle `ArticleCategorie`**

### **Description :**
Table pivot pour relier les articles aux catégories.

### **Champs :**

| Champ              | Type           | Description                                                  |
|--------------------|----------------|--------------------------------------------------------------|
| `id`              | INT (PK, AI)  | Identifiant unique de la relation.                          |
| `article_id`      | INT (FK)      | Référence à l'article (`Article.id`).                       |
| `categorie_id`    | INT (FK)      | Référence à la catégorie (`CategorieArticle.id`).           |
| `created_at`      | DATETIME      | Date de création de la relation.                            |
| `updated_at`      | DATETIME      | Dernière modification de la relation.                       |

---

## **Relations entre les Tables**

1. **Membres (`Membre`) et Titres (`Titre`)** :
   - Relation **1:N** : Un titre peut être attribué à plusieurs membres, mais chaque membre a un seul titre.

2. **Membres (`Membre`) et Domaines d'Expertise (`DomaineExpertise`)** :
   - Relation **M:N** via la table pivot `MembreDomaine` : Un membre peut avoir plusieurs domaines d'expertise, et un domaine peut être partagé entre plusieurs membres.

3. **Membres (`Membre`) et Articles (`Article`)** :
   - Relation **M:N** via la table pivot `ArticleAuteur` : Un membre peut contribuer à plusieurs articles, et un article peut avoir plusieurs auteurs.

4. **Sujets de Recherche (`SujetRecherche`) et Membres (`Membre`)** :
   - Relation **M:N** via la table pivot `SujetMembre` : Un sujet peut impliquer plusieurs membres, et un membre peut travailler sur plusieurs sujets.

5. **Sujets de Recherche (`SujetRecherche`) et Domaines d'Application (`DomaineApplication`)** :
   - Relation **M:N** via la table pivot `SujetDomaineApplication` : Un sujet peut avoir plusieurs domaines d'application, et un domaine d'application peut concerner plusieurs sujets.

6. **Domaines d'Application (`DomaineApplication`) et Domaines d'Expertise (`DomaineExpertise`)** :
   - Pas de relation directe, mais des liens implicites peuvent exister à travers les sujets de recherche et les membres.

7. **Articles (`Article`) et Membres (`Membre`)** :
   - Relation **M:N** via `ArticleAuteur` : Un article peut avoir plusieurs auteurs, et un membre peut écrire plusieurs articles.

8. **Articles (`Article`) et Catégories (`CategorieArticle`)** :
   - Relation **M:N** via `ArticleCategorie` : Un article peut être classé dans plusieurs catégories, et une catégorie peut contenir plusieurs articles.

---

## **Workflow**

Voici un workflow complet impliquant toutes les tables :

---

### **1. Gestion des Titres**

**Étape 1 : Ajouter un nouveau titre**
- Ajouter un enregistrement dans la table `Titre` avec le champ `nom` (exemple : "Postdoctorant").

**Étape 2 : Assigner un titre à un membre**
- Lors de la création ou de la mise à jour d’un membre, associer son `titre_id` à l’identifiant du titre correspondant.

---

### **2. Gestion des Domaines d'Expertise**

**Étape 1 : Ajouter un nouveau domaine d'expertise**
- Ajouter un enregistrement dans `DomaineExpertise` avec le champ `nom` (exemple : "Physique Quantique").

**Étape 2 : Associer un domaine à un membre**
- Utiliser la table pivot `MembreDomaine` pour associer un `membre_id` (depuis `Membre`) et un `domaine_id` (depuis `DomaineExpertise`).

---

### **3. Gestion des Membres**

**Étape 1 : Ajouter un nouveau membre**
1. Ajouter un enregistrement dans `Membre` avec les champs `prenom`, `nom`, `email`, `titre_id`, et éventuellement une `photo`.
2. Assigner les domaines d'expertise à ce membre via `MembreDomaine`.

**Étape 2 : Mettre à jour un membre**
- Mettre à jour les informations dans la table `Membre`, y compris ses relations avec `Titre` et `DomaineExpertise`.

---

### **4. Gestion des Articles**

**Étape 1 : Ajouter un nouvel article**
1. Ajouter un enregistrement dans `Article` avec les champs `titre`, `contenu`, et `date_publication`.
2. Associer les auteurs à cet article via la table pivot `ArticleAuteur`.

**Étape 2 : Associer un membre à un article**
- Ajouter une relation dans `ArticleAuteur` entre `membre_id` et `article_id`, avec le rôle (exemple : "Auteur principal").

---

### **5. Gestion des Sujets de Recherche**

**Étape 1 : Créer un nouveau sujet de recherche**
1. Ajouter un enregistrement dans `SujetRecherche` avec :
   - Le titre du sujet (`titre`),
   - Le problème à résoudre (`probleme`),
   - La méthodologie (`methodologie`, si applicable),
   - La description (`description`),
   - La date de début (`date_debut`) et éventuellement une date de fin (`date_fin`).

**Étape 2 : Associer des membres au sujet**
- Utiliser la table pivot `SujetMembre` pour relier les membres (`membre_id`) au sujet (`sujet_id`).

**Étape 3 : Associer des domaines d'application au sujet**
- Utiliser la table pivot `SujetDomaineApplication` pour relier les domaines d'application (`domaine_id`) au sujet (`sujet_id`).

---

### **6. Gestion des Domaines d'Application**

**Étape 1 : Ajouter un domaine d'application**
- Ajouter un enregistrement dans `DomaineApplication` avec un nom descriptif (exemple : "Médecine").

**Étape 2 : Associer un domaine d'application à un sujet**
- Utiliser la table pivot `SujetDomaineApplication` pour associer le domaine au sujet.

---

### **Exemple d’utilisation complète**

#### **Cas pratique : Ajouter un nouveau sujet de recherche**

1. **Créer un sujet de recherche :**
   - Titre : Étude des Particules Subatomiques.
   - Problème : Comprendre les interactions fondamentales.
   - Méthodologie : Analyse des collisions dans des accélérateurs.
   - Description : Résumé en Markdown.
   - Date de début : 2024-01-01.

2. **Associer des domaines d'application :**
   - Ajouter des relations dans `SujetDomaineApplication` :
     - Domaine 1 : Physique Quantique.
     - Domaine 2 : Informatique.

3. **Associer des membres :**
   - Ajouter des relations dans `SujetMembre` :
     - Membre 1 : Anne Martin.
     - Membre 2 : Paul Dupont.

4. **Associer des articles liés :**
   - Si un article existe déjà sur ce sujet, associer les membres via `ArticleAuteur`.

---

## **Workflow Complet avec le Blog**

---

### **Étape 1 : Ajouter une Catégorie d'Article**

- Insérer un enregistrement dans `CategorieArticle` avec le champ `nom` (exemple : "Physique Quantique").
- Exemple :
  ```plaintext
  id: 1
  nom: Physique Quantique
  created_at: 2024-11-01 10:00:00
  updated_at: 2024-11-01 10:00:00
  ```

---

### **Étape 2 : Ajouter un Article**

1. **Créer l'article :**
   - Insérer un enregistrement dans `Article` avec :
     - `titre`: "Les avancées en physique quantique",
     - `contenu`: Texte au format Markdown,
     - `image_principale`: URL d'une image,
     - `date_publication`: Date prévue pour la publication.

   Exemple :
   ```plaintext
   id: 1
   titre: Les avancées en physique quantique
   contenu: **Markdown content**
   image_principale: /images/quantique.jpg
   date_publication: 2024-11-10
   created_at: 2024-11-01 10:00:00
   updated_at: 2024-11-01 10:00:00
   ```

2. **Associer des auteurs :**
   - Insérer dans `ArticleAuteur` pour lier les auteurs à cet article.
   - Exemple :
     ```plaintext
     id: 1
     article_id: 1
     membre_id: 1
     role: Auteur principal
     created_at: 2024-11-01 10:00:00
     ```

3. **Associer des catégories :**
   - Insérer dans `ArticleCategorie` pour classer l'article dans une ou plusieurs catégories.
   - Exemple :
     ```plaintext
     id: 1
     article_id: 1
     categorie_id: 1
     created_at: 2024-11-01 10:00:00
     ```

---

### **Étape 3 : Mettre à Jour un Article**

- Mettre à jour les champs `titre`, `contenu`, ou les relations avec les auteurs et catégories via les tables pivots `ArticleAuteur` et `ArticleCategorie`.

---


### **Séparation en Applications Django**

Pour ce projet, voici les applications nécessaires, leurs rôles et les modèles qu'elles doivent contenir :

---

## **1. Application : `members`**

### **Rôle :**
Gérer les informations liées aux membres du laboratoire, y compris leurs titres, domaines d'expertise, et les relations avec les autres entités.

### **Modèles :**
- **`Titre`** : Représente les titres ou rôles attribués aux membres.
- **`DomaineExpertise`** : Représente les domaines d'expertise des membres.
- **`Membre`** : Stocke les informations des membres.
- **`MembreDomaine`** (table pivot) : Relie les membres et leurs domaines d'expertise.

---

## **2. Application : `research`**

### **Rôle :**
Gérer les sujets de recherche, leurs problématiques, méthodologies, domaines d'application et les membres impliqués.

### **Modèles :**
- **`SujetRecherche`** : Représente les sujets de recherche.
- **`DomaineApplication`** : Représente les domaines où les résultats des recherches peuvent être appliqués.
- **`SujetMembre`** (table pivot) : Relie les membres aux sujets de recherche.
- **`SujetDomaineApplication`** (table pivot) : Relie les sujets de recherche à leurs domaines d'application.

---

## **3. Application : `blog`**

### **Rôle :**
Gérer les articles du blog, y compris leurs contenus, auteurs, et catégories.

### **Modèles :**
- **`Article`** : Stocke les informations des articles.
- **`CategorieArticle`** : Représente les catégories des articles.
- **`ArticleAuteur`** (table pivot) : Relie les articles et leurs auteurs.
- **`ArticleCategorie`** (table pivot) : Relie les articles à leurs catégories.

---


## **Structure des Applications**

### **1. `members`**
Contiendra :
- Modèles : `Titre`, `DomaineExpertise`, `Membre`, `MembreDomaine`.
- Vues : Gestion des membres (ajout, mise à jour, suppression), affichage des profils.
- URLs : Routes pour accéder aux fonctionnalités liées aux membres.
- Templates : Pages pour lister les membres, afficher leurs détails, etc.

---

### **2. `research`**
Contiendra :
- Modèles : `SujetRecherche`, `DomaineApplication`, `SujetMembre`, `SujetDomaineApplication`.
- Vues : Gestion des sujets de recherche (création, mise à jour, suppression), affichage des détails des sujets.
- URLs : Routes pour accéder aux fonctionnalités liées aux sujets de recherche.
- Templates : Pages pour lister les sujets, afficher les détails, et associer des membres ou des domaines d'application.

---

### **3. `blog`**
Contiendra :
- Modèles : `Article`, `CategorieArticle`, `ArticleAuteur`, `ArticleCategorie`.
- Vues : Gestion des articles (ajout, modification, suppression), affichage des articles et des catégories.
- URLs : Routes pour accéder aux articles par auteur, par catégorie, ou par sujet.
- Templates : Pages pour afficher les articles, leurs détails, et les listes par catégorie.

---

## **Structure Générale du Projet**

Voici une structure hypothétique pour organiser le projet :

```
project/
    ├── members/
    │   ├── models.py      # Modèles liés aux membres
    │   ├── views.py       # Vues pour gérer les membres
    │   ├── urls.py        # Routes pour accéder aux membres
    │   ├── templates/     # Modèles HTML liés aux membres
    │   └── tests.py       # Tests unitaires pour les membres
    ├── research/
    │   ├── models.py      # Modèles liés aux sujets de recherche
    │   ├── views.py       # Vues pour gérer les sujets
    │   ├── urls.py        # Routes pour accéder aux sujets
    │   ├── templates/     # Modèles HTML liés aux sujets
    │   └── tests.py       # Tests unitaires pour les sujets
    ├── blog/
    │   ├── models.py      # Modèles liés aux articles de blog
    │   ├── views.py       # Vues pour gérer les articles
    │   ├── urls.py        # Routes pour accéder aux articles
    │   ├── templates/     # Modèles HTML liés aux articles
    │   └── tests.py       # Tests unitaires pour les articles
    ├── project/           # Configuration globale du projet Django
    │   ├── settings.py    # Configuration du projet
    │   ├── urls.py        # Routes globales
    │   ├── wsgi.py        # Interface avec le serveur web
    │   └── asgi.py        # Interface pour les applications asynchrones
    ├── manage.py          # Commande principale de gestion du projet
```

---



# **1. Application `members`**

### **Modèle `Titre`**

#### **Description :**
Représente les titres ou rôles attribués aux membres, tels que "Dr.", "Professeur", ou "Postdoctorant".

```python
from django.db import models

class Titre(models.Model):
    nom = models.CharField(max_length=50, unique=True, help_text="Nom du titre, par exemple : 'Dr.', 'Professeur'.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
```

---

### **Modèle `DomaineExpertise`**

#### **Description :**
Représente les spécialités scientifiques ou techniques des membres.

```python
class DomaineExpertise(models.Model):
    nom = models.CharField(max_length=255, unique=True, help_text="Nom du domaine d'expertise, par exemple : 'Physique Quantique'.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
```

---

### **Modèle `Membre`**

#### **Description :**
Stocke les informations des membres, y compris leurs titres et domaines d'expertise.

```python
class Membre(models.Model):
    prenom = models.CharField(max_length=100, help_text="Prénom du membre.")
    nom = models.CharField(max_length=100, help_text="Nom du membre.")
    email = models.EmailField(unique=True, help_text="Adresse email professionnelle.")
    telephone = models.CharField(max_length=20, null=True, blank=True, help_text="Numéro de téléphone.")
    photo = models.ImageField(upload_to='photos_membres/', null=True, blank=True, help_text="Photo du membre.")
    titre = models.ForeignKey(Titre, on_delete=models.SET_NULL, null=True, related_name="membres", help_text="Titre du membre.")
    domaines_expertise = models.ManyToManyField(DomaineExpertise, related_name="membres", blank=True, help_text="Domaines d'expertise associés.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
```

---

# **2. Application `research`**

### **Modèle `DomaineApplication`**

#### **Description :**
Représente les domaines dans lesquels les résultats des recherches peuvent être appliqués, comme "Médecine", "Informatique", ou "Nanotechnologie".

```python
class DomaineApplication(models.Model):
    nom = models.CharField(max_length=255, unique=True, help_text="Nom du domaine d'application, par exemple : 'Médecine'.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
```

---

### **Modèle `SujetRecherche`**

#### **Description :**
Représente les sujets de recherche, incluant le problème à résoudre, la méthodologie utilisée, et les membres impliqués.

```python
class SujetRecherche(models.Model):
    titre = models.CharField(max_length=255, unique=True, help_text="Titre du sujet de recherche.")
    probleme = models.TextField(help_text="Description du problème à résoudre.")
    methodologie = models.TextField(null=True, blank=True, help_text="Description de la méthodologie (Markdown autorisé).")
    description = models.TextField(help_text="Résumé général du sujet au format Markdown.")
    contenu_markdown = models.TextField(help_text="Contenu détaillé du sujet au format Markdown.")
    date_debut = models.DateField(help_text="Date de début du sujet.")
    date_fin = models.DateField(null=True, blank=True, help_text="Date de fin (peut être null si en cours).")
    membres = models.ManyToManyField('members.Membre', through='SujetMembre', related_name='sujets_recherche', help_text="Membres travaillant sur ce sujet.")
    domaines_application = models.ManyToManyField(DomaineApplication, through='SujetDomaineApplication', related_name='sujets_recherche', help_text="Domaines d'application liés au sujet.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
```

---

### **Modèle `SujetMembre`**

#### **Description :**
Gère la relation entre les membres et les sujets de recherche, en enregistrant leur rôle spécifique.

```python
class SujetMembre(models.Model):
    sujet = models.ForeignKey(SujetRecherche, on_delete=models.CASCADE, related_name="relations_membres")
    membre = models.ForeignKey('members.Membre', on_delete=models.CASCADE, related_name="relations_sujets")
    role = models.CharField(max_length=100, null=True, blank=True, help_text="Rôle du membre dans le sujet de recherche.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sujet', 'membre')
```

---

### **Modèle `SujetDomaineApplication`**

#### **Description :**
Gère la relation entre les sujets de recherche et leurs domaines d'application.

```python
class SujetDomaineApplication(models.Model):
    sujet = models.ForeignKey(SujetRecherche, on_delete=models.CASCADE, related_name="relations_domaines")
    domaine = models.ForeignKey(DomaineApplication, on_delete=models.CASCADE, related_name="relations_sujets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sujet', 'domaine')
```

---

# **3. Application `blog`**

### **Modèle `CategorieArticle`**

#### **Description :**
Représente les catégories des articles du blog, comme "Actualités", "Recherche", ou "Événements".

```python
class CategorieArticle(models.Model):
    nom = models.CharField(max_length=255, unique=True, help_text="Nom de la catégorie de l'article.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
```

---

### **Modèle `Article`**

#### **Description :**
Stocke les articles de blog, y compris le titre, le contenu en Markdown, et les catégories associées.

```python
class Article(models.Model):
    titre = models.CharField(max_length=255, help_text="Titre de l'article.")
    contenu = models.TextField(help_text="Contenu complet de l'article au format Markdown.")
    image_principale = models.ImageField(upload_to='images_articles/', null=True, blank=True, help_text="Image principale de l'article.")
    date_publication = models.DateField(help_text="Date de publication de l'article.")
    slug = models.SlugField(unique=True, help_text="Slug pour l'URL de l'article.")
    categories = models.ManyToManyField(CategorieArticle, through='ArticleCategorie', related_name='articles', help_text="Catégories associées à l'article.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
```

---

### **Modèle `ArticleAuteur`**

#### **Description :**
Gère la relation entre les articles et leurs auteurs (membres).

```python
class ArticleAuteur(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="auteurs")
    membre = models.ForeignKey('members.Membre', on_delete=models.CASCADE, related_name="articles")
    role = models.CharField(max_length=100, null=True, blank=True, help_text="Rôle du membre dans l'article (exemple : 'Auteur principal').")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('article', 'membre')
```

---

### **Modèle `ArticleCategorie`**

#### **Description :**
Gère la relation entre les articles et leurs catégories.

```python
class ArticleCategorie(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="relations_categories")
    categorie = models.ForeignKey(CategorieArticle, on_delete=models.CASCADE, related_name="relations_articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('article', 'categorie')
```

---
