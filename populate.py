import os

def populate():

    notification_attendance = NotificationType.objects.create(notification_type='Attendance', condition=3, content='Student missed 3 classes in row')
    notification_performance = NotificationType.objects.create(notification_type='Performance', condition=50, content='Student performance is lowest than 50%')
    notification_assignment = NotificationType.objects.create(notification_type='Assignment', condition=3, content='Student did not deliver 3 assignments')

    # system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    # system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=None, school=None)

    #testdata

    school =  School.objects.create(title='Surrey, BC', phone='604-930-2122', address='8820 168 St, Surrey, BC V4N 6G7', comments="Gobind Sarvar School was established in 2005 as a learning institute under the premise Today's Learner...Tomorrow's Guide.")
    period = Period.objects.create(description='Summer 2015', start_date='2015-03-25', end_date='2015-03-31', comments='First school year of the system', school= school)

    system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    system_admin_user.password = 'admin'
    system_admin_user.save()
    system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=period, school=school)

if __name__ == '__main__':

    print ('Starting population script..')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplus.settings')

    from dashboard.models import *
    from accounts.models import *
    from school_components.models import *

    populate()

    print ('.. Done!')
