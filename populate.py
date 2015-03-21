import os

def populate():

    notification_attendance = NotificationType.objects.create(notification_type='Attendance', condition=3, content='Student missed 3 classes in row')
    notification_performance = NotificationType.objects.create(notification_type='Performance', condition=50, content='Student performance is lowest than 50%')
    notification_assignment = NotificationType.objects.create(notification_type='Assignment', condition=3, content='Student did not deliver 3 assignments')

if __name__ == '__main__':

    print ('Starting population script..')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplus.settings')

    from dashboard.models import *
    populate()

    print ('.. Done!')
