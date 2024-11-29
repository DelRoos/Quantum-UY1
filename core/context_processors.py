from .models import SiteConfig

def site_settings(request):
    """
    Ajoute les paramètres du site au contexte global des templates
    """
    try:
        config = SiteConfig.objects.first()
        return {
            'site_name': config.site_name,
            'site_description': config.site_description,
            'contact_email': config.contact_email,
            'social_links': {
                'twitter': config.twitter_url,
                'linkedin': config.linkedin_url,
                'researchgate': config.researchgate_url,
            }
        }
    except (SiteConfig.DoesNotExist, AttributeError):
        return {
            'site_name': 'Quantum UY1',
            'site_description': 'Laboratoire de Recherche en Physique Quantique',
            'contact_email': 'contact@quantum-uy1.com',
            'social_links': {}
        }