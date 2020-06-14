from django.apps import AppConfig


class SocialideaConfig(AppConfig):
    name = "socialidea"

    def ready(self):
        import socialidea.signals
