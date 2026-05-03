from django.apps import AppConfig

class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Bu yerda 'posts' emas, to'liq yo'l bo'lishi kerak
    name = 'config.posts'

    def ready(self):
        # Signallarni yuklash uchun to'liq yo'lni ko'rsating
        import config.posts.models