from django.apps import AppConfig


class MswiggyConfig(AppConfig):
    name = 'mswiggy'

    def ready(self):
        import mswiggy.signals