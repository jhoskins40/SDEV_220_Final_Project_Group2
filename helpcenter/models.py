'''Module Doctstring Goes Here.'''
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

class Ticket(models.Model):
    '''Defines the data fields and parameters of our tickets.'''

    # The "id" field-- a unique, randomly generated, value.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,serialize=True, editable=False)
    # The "author" field-- the username of whomever created the ticket.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    # The "title" field-- a brief summary of the subject to follow.
    title = models.CharField(max_length=200)
    # The "subject" field-- a detailed description of the above-mentioned title.
    subject = models.TextField()
    # The "submitted_date" field-- a timestamp of the ticket creation date.
    submitted_date = models.DateTimeField(blank=True, null=True, editable=False)
    # The "status" field-- tracks the support status of the ticket. (not implemented)
    class Status(models.IntegerChoices):
        '''Enum setup for the status field.'''
        PENDING = 0
        ACTIVE  = 1
        CLOSED  = 2

    status = models.IntegerField(default=0,choices=Status.choices)

    def publish(self):
        '''This is called whenever the user hits the "save" button in the webapp.'''
        self.submitted_date = timezone.now()
        self.save()

    def __str__(self):
        '''Generic function doc-string'''
        # pylint: disable=invalid-str-returned

        return self.title
    