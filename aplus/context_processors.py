from school_components.models import School, Period
# The context processor function
def school_period(request):
    school = School.objects.all().order_by('title')
    period = Period.objects.all().order_by('-id').reverse()

    return {
        'school_list': school, 'period_list': period,
    }