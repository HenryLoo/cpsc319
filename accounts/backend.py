from django.contrib.auth.models import User

class NoHashBackend(object):
    def authenticate(self, username=None, password=None):
        user = User.objects.all().filter(username=username, password=password)

        if user.exists():
            return user[0]
        else:
            return None
        
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
        
