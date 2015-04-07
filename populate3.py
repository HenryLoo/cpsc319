import os

def populate():

    notification_attendance = NotificationType.objects.create(notification_type='Attendance', condition=3, content='Student missed 3 classes in row')
    notification_performance = NotificationType.objects.create(notification_type='Performance', condition=50, content='Student performance is lowest than 50%')
    notification_assignment = NotificationType.objects.create(notification_type='Assignment', condition=3, content='Student did not deliver 3 assignments')

    # system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    # system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=None, school=None)
    school1 =  School.objects.create(title='Surrey, BC', phone='604-930-2122', address='8820 168 St, Surrey, BC V4N 6G7', comments="Gobind Sarvar School was established in 2005 as a learning institute under the premise Today's Learner...Tomorrow's Guide.")
    period1 = Period.objects.create(description='Summer 2015', start_date='2015-03-25', end_date='2015-03-31', comments='First school year of the system', school= school1)
    school2 =  School.objects.create(title='Vancouver, BC', phone='604-888-2122', address='5100 000 St, Surrey, BC V6N 0I8', comments="2nd school")
    period2 = Period.objects.create(description='Summer 2015', start_date='2015-03-25', end_date='2015-03-31', comments='First school year of the system', school= school2)

    system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    system_admin_user.password = 'admin'
    system_admin_user.save()
    system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=period1, school=school1)

    department1 = Department.objects.create(school=school1, name='Language', description='description here')
    department2 = Department.objects.create(school=school2, name='Language2', description='description here')

    course1 = Course.objects.create(school=school1, period=period1, department=department1, name='Basic Language 1', age_requirement=4, description='description here')
    course2 = Course.objects.create(school=school2, period=period2, department=department2, name='Basic Language 2', age_requirement=4, description='description here')

    teaching1 = TeachingAvailability.objects.create(monday=False);
    teaching2 = TeachingAvailability.objects.create(monday=False);

    teacher_user = User.objects.create_user(username='teacher1@email.com', email='teacher1@email.com', password='teacher', first_name='John', last_name='Doe')
    teacher_userprofile = UserProfile.objects.create(user= teacher_user, phone='778-666-000', role='TEACHER', period=period1, school=school1)
    teacher1 = TeacherUser.objects.create(user=teacher_userprofile, teaching_availability= teaching1, comments='comments here')

    teacher_user2 = User.objects.create_user(username='teacher2@email.com', email='teacher2@email.com', password='teacher', first_name='John', last_name='Doe')
    teacher_userprofile2 = UserProfile.objects.create(user= teacher_user2, phone='778-666-000', role='TEACHER', period=period2, school=school2)
    teacher2 = TeacherUser.objects.create(user=teacher_userprofile2, teaching_availability= teaching2, comments='comments here')
   
    class1 = Class.objects.create(course=course1,school=school1, period=period1, section='1', description='description here', class_size=20, room='X')
    class2 = Class.objects.create(course=course2,school=school2, period=period2, section='1', description='description here', class_size=20, room='X')

    class_teacher = ClassTeacher.objects.create(primary_teacher=teacher1, secondary_teacher=None, taught_class=class1)
    class_teacher2 = ClassTeacher.objects.create(primary_teacher=teacher2, secondary_teacher=None, taught_class=class2)

    class_schedule = ClassSchedule.objects.create(sch_class=class1)
    class_schedule2 = ClassSchedule.objects.create(sch_class=class2)
    
    parent1 = Parent.objects.create(
        first_name="Julie", 
        last_name="Price", 
        school= school1, 
        period= period1, 
        comments= "", 
        cell_phone= "5-(188)725-5712", 
        email= "tlittle18@unblog.fr"
        )

    student1 = Student.objects.create(
        first_name= "Carolyn", 
        last_name= "Jones", 
        emergency_contact_phone="6-(621)832-5904", 
        emergency_contact_name="Julie Willis", 
        parent= parent1, 
        gender= "F", 
        school= school1, 
        birthdate= "2004-06-30", 
        period= period1, 
        allergies= "", 
        comments= "", 
        home_phone= "7-(272)438-7908", 
        address= "06738 Sauthoff Junction", 
        email= "sashaseifollahi@gmail.com"
    )

    student2 = Student.objects.create(
        first_name= "Barbara", 
        last_name= "Fisher", 
        emergency_contact_phone= "2-(029)230-6211", 
        emergency_contact_name= "Louise Williamson", 
        parent= parent1, 
        gender= "F", 
        school= school1, 
        birthdate= "2010-07-16", 
        period= period1, 
        allergies= "", 
        comments= "", 
        home_phone= "9-(592)782-4565", 
        address= "70 Buell Circle", 
        email= "sashaseifollahi@gmail.com"
    )

    student3 = Student.objects.create(
        first_name= "Frank", 
        last_name= "Gibson", 
        emergency_contact_phone= "9-(920)573-8300", 
        emergency_contact_name= "Chris Kelly", 
        parent= parent1, 
        gender= "M", 
        school= school1, 
        birthdate= "2004-05-29", 
        period= period1, 
        allergies= "Hydrocortisone", 
        comments= "", 
        home_phone= "4-(836)709-7552", 
        address= "85 Columbus Drive", 
        email= "sashaseifollahi@gmail.com"
    )

    student4 = Student.objects.create(
        first_name= "Bob", 
        last_name= "Miller", 
        emergency_contact_phone="6-(621)832-5904", 
        emergency_contact_name="Julie Willis", 
        parent= parent1, 
        gender= "F", 
        school= school2, 
        birthdate= "2004-06-30", 
        period= period2, 
        allergies= "", 
        comments= "", 
        home_phone= "7-(272)438-7908", 
        address= "06738 Sauthoff Junction", 
        email= "sashaseifollahi@gmail.com"
    )

    student5 = Student.objects.create(
        first_name= "Trevor", 
        last_name= "Brown", 
        emergency_contact_phone= "2-(029)230-6211", 
        emergency_contact_name= "Louise Williamson", 
        parent= parent1, 
        gender= "F", 
        school= school2, 
        birthdate= "2010-07-16", 
        period= period2, 
        allergies= "", 
        comments= "", 
        home_phone= "9-(592)782-4565", 
        address= "70 Buell Circle", 
        email= "sashaseifollahi@gmail.com"
    )

    student6 = Student.objects.create(
        first_name= "Gibson", 
        last_name= "Frank", 
        emergency_contact_phone= "9-(920)573-8300", 
        emergency_contact_name= "Chris Kelly", 
        parent= parent1, 
        gender= "M", 
        school= school2, 
        birthdate= "2004-05-29", 
        period= period2, 
        allergies= "Hydrocortisone", 
        comments= "", 
        home_phone= "4-(836)709-7552", 
        address= "85 Columbus Drive", 
        email= "sashaseifollahi@gmail.com"
    )

    class_registration1 = ClassRegistration.objects.create(reg_class=class1, student=student1, registration_status=True, school=school1, period=period1)
    class_registration2 = ClassRegistration.objects.create(reg_class=class1, student=student2, registration_status=True, school=school1, period=period1)
    class_registration3 = ClassRegistration.objects.create(reg_class=class1, student=student3, registration_status=True, school=school1, period=period1)

    class_registration1 = ClassRegistration.objects.create(reg_class=class2, student=student4, registration_status=True, school=school2, period=period2)
    class_registration2 = ClassRegistration.objects.create(reg_class=class2, student=student5, registration_status=True, school=school2, period=period2)
    class_registration3 = ClassRegistration.objects.create(reg_class=class2, student=student6, registration_status=True, school=school2, period=period2)

if __name__ == '__main__':

    print ('Starting population script..')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplus.settings')

    from dashboard.models import *
    from accounts.models import *
    from school_components.models import *

    populate()

    print ('.. Done!')
