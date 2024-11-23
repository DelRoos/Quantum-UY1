function showContent(articleId) {
    // Cacher tous les articles
    const articles = document.querySelectorAll('.article');
    articles.forEach(article => {
        article.style.display = 'none';
    });

    // Afficher l'article sélectionné
    const selectedArticle = document.getElementById(articleId);
    if (selectedArticle) {
        selectedArticle.style.display = 'block';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour afficher l'article correspondant
    function showArticle(articleId) {
        showContent(articleId);
    }

    // Vérifier l'URL et afficher l'article correspondant
    const hash = window.location.hash;
    if (hash) {
        showArticle(hash.substring(1)); // Enlever le '#' et afficher l'article
    } else {
        // Afficher le premier article par défaut
        showContent('article1');
    }

    // Écouteur d'événements pour les liens dans la sidebar
    const sidebarLinks = document.querySelectorAll('.sidebar a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const articleId = this.getAttribute('href').substring(1); // Enlever le '#'
            showArticle(articleId);
        });
    });
});