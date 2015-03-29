from school_components.models import School, Period
from accounts.utils import *
# The context processor function
def school_period(request):

        request = process_user_info(request)
        
	if request.user.is_authenticated():
		user_school = request.user_school
	else:
		user_school = None

	schoollist = School.objects.all().order_by('title') #exclude did not work here always so to fiz bug added "if not current on user" on html
	periodlist = Period.objects.filter(school=user_school).order_by('-id').reverse()

	return {
        'school_list': schoollist, 'period_list': periodlist,
        'user_role': request.user_role,
        'user_school': request.user_school,
        'user_period':request.user_period
    }

