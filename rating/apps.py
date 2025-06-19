from django.apps import AppConfig

"""
AppConfig for the rating app.
Ensures that signals are loaded when the app is ready.
"""


class RatingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rating"

    def ready(self):
        import rating.signals
