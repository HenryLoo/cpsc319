from school_components.models import School, Period
from accounts.utils import *
# The context processor function
def school_period(request):

        if not request.user.is_anonymous():
                request = process_user_info(request)
        
        if request.user.is_authenticated():
                user_school = request.user_school
        else:
                user_school = None

        schoollist = School.objects.all().order_by('title') #exclude did not work here always so to fiz bug added "if not current on user" on html
        periodlist = Period.objects.filter(school=user_school).order_by('-id').reverse()

        cd = {
                'school_list': schoollist, 'period_list': periodlist,
        }

        if not request.user.is_anonymous():
                cd['user_school'] = request.user_school
                cd['user_period'] = request.user_period
                cd['user_role'] = request.user_role

        
        return cd
