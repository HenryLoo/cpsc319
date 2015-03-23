import os

def populate():

    notification_attendance = NotificationType.objects.create(notification_type='Attendance', condition=3, content='Student missed 3 classes in row')
    notification_performance = NotificationType.objects.create(notification_type='Performance', condition=50, content='Student performance is lowest than 50%')
    notification_assignment = NotificationType.objects.create(notification_type='Assignment', condition=3, content='Student did not deliver 3 assignments')

    system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=None, school=None)

if __name__ == '__main__':

    print ('Starting population script..')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplus.settings')

    from dashboard.models import *
    from accounts.models import *

    populate()

    print ('.. Done!')
