from accounts.models import *
from accounts.forms import *
from django.contrib.auth.models import User

NUM_FIELDS = 16

def create_teacher(school_id, period_id, email, password, first_name, last_name,
                   phone, comments, monday, monday_times, tuesday, tuesday_times,
                   wednesday, wednesday_times, thursday, thursday_times, friday, friday_times):

    #add the school and period to the userprofile
    monday = to_bool(monday)
    tuesday = to_bool(tuesday)
    wednesday = to_bool(wednesday)
    thursday = to_bool(thursday)
    friday = to_bool(friday)
    
    user = User(username=email.lower(), email=email.lower(), first_name=first_name, last_name=last_name)
    user.set_password(password)
    
    user.full_clean()
    
    
    profile = UserProfile(user=user, phone=phone, role='TEACHER')
    profile.full_clean()
   
    avail = TeachingAvailability(monday=monday, monday_times=monday_times, tuesday=tuesday, tuesday_times=tuesday_times, wednesday=wednesday,
                                 wednesday_times=wednesday_times, thursday=thursday, thursday_times=thursday_times, friday=friday, friday_times=friday_times)
    avail.full_clean()
   

    teacher = TeacherUser(user=profile, teaching_availability=avail, comments=comments)
    teacher.full_clean()

    ##not saving here anymore, saving only if there are no errors
    
    #only save if all of them have been verified
    #user.save()
    #profile.user = user
    #profile.save()
    #teacher.user = profile
    #avail.save()
    #teacher.teaching_availability = avail
    #teacher.save()

    return (user, profile, avail, teacher)
    
    
    
    


#fields should be (a.school, b.period), 1.email, 2.password, 3.first name, 4.last name, 5.phone, 6.comments, 7.monday, 8.monday comments, ... friday comments
#NOTE: just assign them to the current school/period, since they are only gonna use this for their first batch

#john@john.com, password, John, He, 604-112-1212, He is john, mon=yes,,tues=yes,,wed=yes,,thurs=yes,,fri=no,I'm a Sauder student

def to_bool(string):
    if 'unknown' in string.lower():
        return None
    if 'yes' in string.lower():
        return True
    if 'no' in string.lower():
        return False

    raise ValidationError("You must specify either yes, no, or unknown for each of Monday to Friday.")


                        
def validate_teachers_csv(file):

    errors = []
    teacher_list = []
    
    for i, line in enumerate(file):
        teacher = map(lambda field: field.strip(), line.split(',')) #!!! how will the datatypes be handled? will python convert them all properly?
        
        try:
            if len(teacher) != NUM_FIELDS:
                    raise ValidationError("Line: '{0}'. The number of fields '{1}' is incorrect for a teacher.".format(line,len(teacher)))
                
                #create a teacher
            school_id = 1 #!!!get the current one
            period_id = 1 #!!!get the current one
                    
            teach_tuple = create_teacher(school_id, period_id, *teacher) 
            teacher_list.append(teach_tuple) #assume the exception doesn't come on this line

        except Exception as e:

            errors.append(str(e))

        if len(errors) > 1:
            return teacher_list, errors

    return teacher_list, errors
            
        

        
