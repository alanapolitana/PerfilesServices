from django.apps import AppConfig


class ParqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AlParque'

def ready(self):
        import AlParque.load_initial_data