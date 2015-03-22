from school_components.models import School, Period
# The context processor function
def school_period(request):
	user_school = request.user.userprofile.school
	schoollist = School.objects.all().order_by('title') #exclude did not work here always so to fiz bug added "if not current on user" on html
	periodlist = Period.objects.filter(school=user_school).order_by('-id').reverse()

	return {
        'school_list': schoollist, 'period_list': periodlist,
    }