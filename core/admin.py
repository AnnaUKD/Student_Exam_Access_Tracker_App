from django.contrib import admin

from core.models import GroupJournal
# Register your models here.

@admin.register(GroupJournal)
class GroupJournalAdmin(admin.ModelAdmin):
    pass
    # list_display = ('group_name', 'journal_url', 'group_amount')
    # search_fields = ('group_name',)
    # list_filter = ('group_amount',)