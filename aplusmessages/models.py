from django.core.urlresolvers import reverse
from django.db import models


class SentMessage(models.Model):
    STATUS_SENT   = 'SENT'
    STATUS_FAILED = 'FAILED'
    STATUS_QUEUED = 'QUEUED'

    STATUS_CHOICES = [(STATUS_SENT, 'sent'), (STATUS_FAILED, 'failed'), (STATUS_QUEUED, 'queued')]

    SEND_IND      = "INDIVIDUAL"
    SEND_EVERYONE = "ALL"
    SEND_STUDENTS = "STUDENTS"
    SEND_TEACHERS = "TEACHERS"
    SEND_ADMINS   = "ADMINS"
    SEND_CLASS    = "CLASS"

    SEND_CHOICES = (
        (SEND_IND, ''),
        (SEND_EVERYONE, 'Everyone'),
        (SEND_STUDENTS, 'Students'),
        (SEND_TEACHERS, 'Teachers'),
        (SEND_ADMINS, 'Admins'),
    )

    sender = models.CharField(max_length = 12, null=True, blank=True)
    from_email = models.CharField(max_length=512)

    recipient_type = models.CharField(max_length = 12, choices = SEND_CHOICES)
    to_list = models.TextField(blank=True, null=True)
    cc_list = models.TextField(blank=True, null=True)
    bcc_list = models.TextField(blank=True, null=True)

    subject = models.CharField(max_length = 255, blank=True, null=True)
    body = models.TextField(blank=True)
    html_body = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, blank=True, null=True, max_length=16)
    status_message = models.CharField(max_length=1024, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)

    def get_formatted_to_list(self):
        names = []
        emails = self.to_list.split(",")
        for email in emails:
            names.append(email.split("@")[0])

        return ','.join(map(str, names))

    def get_formatted_to_list_detail(self):
        names = []
        emails = self.to_list.split(",")
        for email in emails:
            names.append((email.split("@")[0]) + " <" + email + ">")

        return ','.join(map(str, names))

#previous:

class Email(models.Model):
    #email = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse()

