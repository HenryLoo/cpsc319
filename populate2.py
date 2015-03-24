import os

def populate():

    notification_attendance = NotificationType.objects.create(notification_type='Attendance', condition=3, content='Student missed 3 classes in row')
    notification_performance = NotificationType.objects.create(notification_type='Performance', condition=50, content='Student performance is lowest than 50%')
    notification_assignment = NotificationType.objects.create(notification_type='Assignment', condition=3, content='Student did not deliver 3 assignments')

    # system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    # system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=None, school=None)
    school1 =  School.objects.create(title='Surrey, BC', phone='604-930-2122', address='8820 168 St, Surrey, BC V4N 6G7', comments="Gobind Sarvar School was established in 2005 as a learning institute under the premise Today's Learner...Tomorrow's Guide.")
    period1 = Period.objects.create(description='Summer 2015', start_date='2015-03-25', end_date='2015-03-31', comments='First school year of the system', school= school1)

    system_admin_user = User.objects.create_user(username='admin@email.com', email='admin@email.com', password='admin', first_name='Admin First Name', last_name='Admin Last Name')
    system_admin_user.password = 'admin'
    system_admin_user.save()
    system_admin_userprofile = UserProfile.objects.create(user= system_admin_user, phone='778-666-000', role='SYSTEM_ADMIN', period=period1, school=school1)

    department1 = Department.objects.create(school=school1, name='Language', description='description here')

    course1 = Course.objects.create(school=school1, period=period1, department=department1, name='Language 1', age_requirement=4, description='description here')

    teaching1 = TeachingAvailability.objects.create(monday=False);

    teacher_user = User.objects.create_user(username='teacher1@email.com', email='teacher1@email.com', password='teacher', first_name='John', last_name='Doe')
    teacher_userprofile = UserProfile.objects.create(user= teacher_user, phone='778-666-000', role='TEACHER', period=period1, school=school1)
    teacher1 = TeacherUser.objects.create(user=teacher_userprofile, teaching_availability= teaching1, comments='comments here')
   
    class1 = Class.objects.create(course=course1,school=school1, period=period1, section='1', description='description here', class_size=20, waiting_list_size=10, room='X')

    class_teacher = ClassTeacher.objects.create(teacher=teacher1, taught_class=class1)

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
        email= "jwillis0@photobucket.com"
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
        email= "lwilliamson1i@godaddy.com"
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
        email= "ckelly1j@shinystat.com"
    )

    class_registration1 = ClassRegistration.objects.create(reg_class=class1, student=student1, registration_status=True, school=school1, period=period1)
    class_registration2 = ClassRegistration.objects.create(reg_class=class1, student=student2, registration_status=True, school=school1, period=period1)
    class_registration3 = ClassRegistration.objects.create(reg_class=class1, student=student3, registration_status=True, school=school1, period=period1)

    grading1= Grading.objects.create(reg_class=class1, student=student1, grade=10, assignment='Assignment 1', date='2015-03-25', comments='')
    grading2= Grading.objects.create(reg_class=class1, student=student1, grade=5, assignment='Assignment 2', date='2015-03-26', comments='')
    grading3= Grading.objects.create(reg_class=class1, student=student1, grade=8, assignment='Assignment 3', date='2015-03-27', comments='')

if __name__ == '__main__':

    print ('Starting population script..')
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplus.settings')

    from dashboard.models import *
    from accounts.models import *
    from school_components.models import *

    populate()

    print ('.. Done!')
