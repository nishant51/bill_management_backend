from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
# your_app/apps.py
    def ready(self):
        import product.signals  # Replace 'your_app' with the name of your app
