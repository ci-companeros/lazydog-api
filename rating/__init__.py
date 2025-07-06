"""
Ensures that the custom AppConfig (RatingConfig) is used for the rating app.
This guarantees that application configuration, including signal registration,
is properly initialized when the app is loaded.
"""
default_app_config = 'rating.apps.RatingConfig'
