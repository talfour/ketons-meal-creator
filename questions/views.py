import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView
from actions.utils import create_action
from .forms import AnswerModelForm, QuestionModelForm
# , CategoryModelForm
from .models import Category, Question, Answer, VoteSystem
from profiles.models import Profile



class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'questions/categories.html'
    context_object_name = 'categories'
    ordering = ['name']


# class CategoryCreateView(LoginRequiredMixin, CreateView):
#     template_name = 'questions/create_category.html'
#     form_class = CategoryModelForm

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             return self.form_valid(form)

#     def form_valid(self, form):
#         obj, created = Category.objects.get_or_create(
#             name=form.cleaned_data['name'])
#         return HttpResponseRedirect(reverse('questions:question-categories'))

#     def form_invalid(self, form):
#         return self.render_to_response(
#             self.get_context_data(form=form)
#         )


class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    ordering = ['-votes', '-created']

    def get_queryset(self):
        qs = super(QuestionListView, self).get_queryset()
        return qs.filter(category__name=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get('slug')
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Question
    template_name = 'questions/question_detail.html'
    form_class = AnswerModelForm

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        question = Question.objects.get(slug=slug)
        return question

    def get_success_url(self):
        return reverse('questions:question-detail-view', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = Answer.objects.filter(question=self.object, parent=None)
        is_answered = False
        for answer in answers:
            if answer.best_answer:
                is_answered = True

        print(self.object.vote_question.get(user=self.request.user.profile))
        
        context['voted'] = self.object.vote_question.get(user=self.request.user.profile).value
        context['is_answered'] = is_answered
        context['form'] = AnswerModelForm()
        context['answers'] = answers
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        reply_id = self.request.POST.get('answer_id')
        answer_qs = None
        answer = form.save(commit=False)
        if reply_id:
            answer_qs = Answer.objects.get(id=reply_id)
            answer.parent = answer_qs
        answer.question = self.object
        answer.author = self.request.user.profile
        answer.save()
        create_action(
            self.request.user, f"Dodał komentarz do {self.get_object()}", self.get_object())
        return super(QuestionDetailView, self).form_valid(form)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'questions/create.html'
    form_class = QuestionModelForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user.profile
        self.object.created = datetime.now()
        self.object.save()
        form.save_m2m()
        create_action(self.request.user, 'Zadał/a nowe pytanie', self.object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

@login_required
def mark_as_best_answer(request):
    answer_id = json.loads(request.body.decode("UTF-8"))
    answer_id = answer_id['answer_id']
    answer_obj = Answer.objects.get(id=answer_id)
    if request.method == "GET":
        is_answered = Answer.objects.filter(question=answer_obj.question.id)
        print(is_answered)
        context = {'is_answered': is_answered}
        return render(request, 'questions:question_detail.html', context)
    if request.method == "POST":
        answer_obj.best_answer = True
        answer_obj.save()
        # use it if question should be closed when best answer is choosen
        answer_q = answer_obj.question
        question = Question.objects.get(id=answer_q.id)
        question.is_open = False
        question.save()
        return JsonResponse({'message': 'Oznaczyłeś/aś najlepszą odpowiedź na to pytanie. Wątek został zamknięty.'})

@login_required
def check_if_exists(request):
    question = json.loads(request.body.decode("UTF-8"))
    question_duplicate = question['question']
    question_obj = Question.objects.filter(title__icontains=question_duplicate)
    q_dict = {}
    for q in question_obj:
        q_dict[q.title] = q.get_absolute_url()
    return JsonResponse({'question':q_dict})


@login_required
def like_unlike_question(request):
    question_id = json.loads(request.body.decode("UTF-8"))
    question_value = question_id['value']
    question_id = question_id['question_id']
    question_obj = Question.objects.get(id=question_id)
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        try:
            exists = VoteSystem.objects.get(question=question_obj, user=profile)
            exists.value = question_value
            exists.save()
            return JsonResponse({'message':'Twój głos został dodany.'})
        except VoteSystem.DoesNotExist:
            vote = VoteSystem.objects.create(user=profile, question=question_obj, value=question_value)
            return JsonResponse({'message':'Twój głos został dodany.'})