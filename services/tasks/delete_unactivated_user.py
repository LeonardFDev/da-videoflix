from django.contrib.auth import get_user_model

User = get_user_model()

def delete_unactivated_user(user_id):
    User.objects.filter(id=user_id, is_active=False).delete()