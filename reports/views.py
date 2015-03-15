from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports
from school_components.models.students_model import Student
from school_components.models.courses_model import Course
from school_components.models.classes_model import Class
from accounts.models import TeacherUser, UserProfile


def view_reports(request):
    return render(request, "reports/view_reports.html")


def export_pdf(request):
    c.drawString(100, 100, "Hello World")
    c = canvas.Canvas("student.pdf")
    student_pdf(c)
    c.showPage()
    c.save()

def export_csv(request):
    context_dictionary = {}

    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="report-title.csv"'

        reports = Report.objects.all()
        # need to change depending on the user choice
        for report in reports:
        writer = csv.writer(response)
         writer.writerow(['depend on the filter'])
         # need to change regarding to the row headers of the data that user selects

        return response

    else:

        return render_to_response('reports/view_reports.html',
			context_dictionary,
			RequestContext(request))
        
