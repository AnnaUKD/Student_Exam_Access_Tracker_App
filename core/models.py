from django.db import models

# Create your models here.
class GroupJournal(models.Model):
    group_name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    journal_url = models.URLField(null=False, blank=False)
    group_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
         # return "%s object (%s)" % (self.__class__.__name__, self.pk)
        return "%s %s %s" % (self.group_name, self.journal_url, self.group_amount)