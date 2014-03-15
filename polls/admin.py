from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
              (None,    {'fields' : ['question']}),
              ('info',  {'fields' : ['pub_date'], 'classes' : ['collapse']})
    ]
    inlines = [ChoiceInLine]
    list_display = ('question', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question']
    

admin.site.register(Poll, PollAdmin)
