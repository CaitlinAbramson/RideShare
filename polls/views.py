from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Suggestion
from django.urls import reverse
from django.views import generic
from django.utils import timezone

class SuggestionView(generic.DetailView):
    model = Question
    template_name = 'polls/suggestions.html'

def suggestResults(request, pk):
    question = get_object_or_404(Question, pk=pk)
    try:
        name = request.POST.get("suggestion_name", "")
        text = request.POST.get("suggestion_text", "")
    except (KeyError, Suggestion.DoesNotExist):
        return render(request, 'polls/suggestions.html', {
            'question': question,
            'error_message': "You didn't submit a suggestion.",
        })
    else:
        question.suggestion_set.create(suggestion_name=name, suggestion_text=text)
        return HttpResponseRedirect(reverse('polls:suggestionsList', args=(question.id,)))

class SuggestionListView(generic.DetailView):
    model = Question
    template_name = 'polls/suggestionsList.html'

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

