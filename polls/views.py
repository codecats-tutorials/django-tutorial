from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from polls.models import Poll, Choice
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'
    
    def get_queryset(self):
        return Poll.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Poll
    def get_queryset(self):
        return Poll.objects.filter(
            pub_date__lte = timezone.now()
        )
    
class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Poll

def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk = poll_id)
    try:
        selected_choice = poll.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        
        return render(request, 'polls/detail.html', {
            'poll' : poll,
            'error_message' : "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls:results', args = (poll.id,) ))