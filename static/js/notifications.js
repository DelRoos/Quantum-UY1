'use strict';

class NotificationSystem {
  constructor() {
    this.setupFormHandlers();
  }

  showFormNotification(form, message, type = 'info') {
    // Supprimer toute notification existante dans le formulaire
    const existingNotification = form.querySelector('.form-notification');
    if (existingNotification) {
      existingNotification.remove();
    }

    // Créer la nouvelle notification
    const notification = document.createElement('div');
    notification.className = `form-notification ${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <span class="notification-text">${message}</span>
        <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
      </div>
    `;

    // Insérer la notification après le dernier input-wrapper
    const lastInputWrapper = form.querySelector('.input-wrapper:last-of-type');
    lastInputWrapper.after(notification);

    // Auto-supprimer après 5 secondes
    setTimeout(() => {
      if (notification.parentNode === form) {
        notification.remove();
      }
    }, 5000);
  }

  showLoader(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalContent = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <div class="button-loader">
        <ion-icon name="sync-outline" class="spin"></ion-icon>
      </div>
    `;
    return () => {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalContent;
    };
  }

  clearErrors(form) {
    form.querySelectorAll('.error-message').forEach(error => {
      error.textContent = '';
    });
  }

  setupFormHandlers() {
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
      newsletterForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        this.clearErrors(newsletterForm);
        const hideLoader = this.showLoader(newsletterForm);
        
        try {
          const formData = new FormData(newsletterForm);
          const csrfToken = newsletterForm.querySelector('[name=csrfmiddlewaretoken]').value;
          
          const response = await fetch(newsletterForm.action, {
            method: 'POST',
            body: formData,
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'X-CSRFToken': csrfToken
            }
          });

          const data = await response.json();
          hideLoader();
          
          if (data.success) {
            this.showFormNotification(newsletterForm, data.message, 'success');
            newsletterForm.reset();
          } else {
            this.showFormNotification(newsletterForm, data.message, 'error');
            
            // Afficher les erreurs sous les champs
            if (data.errors) {
              Object.keys(data.errors).forEach(field => {
                const errorDiv = newsletterForm.querySelector(`#newsletter-${field}-error`);
                if (errorDiv) {
                  errorDiv.textContent = data.errors[field].join(', ');
                }
              });
            }
          }
        } catch (error) {
          hideLoader();
          this.showFormNotification(newsletterForm, 'Erreur de connexion au serveur', 'error');
        }
      });
    }
  }
}

// Initialiser le système de notifications
document.addEventListener('DOMContentLoaded', () => {
  window.notificationSystem = new NotificationSystem();
});