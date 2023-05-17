from itertools import chain
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import NewUserForm
from actions.models import Action
from food.models import Food
from profiles.models import Profile
from recipes.models import Recipe
from questions.models import Question

UserModel = get_user_model()

def home_view(request):
    user = request.user
    actions = None
    following_ids = None
    if request.user.is_authenticated:
        profile = request.user.profile
        actions = Action.objects.exclude(
            user=request.user).exclude(verb="liked")
        following_ids = profile.following.values_list(
            'following_user_id', flat=True)

        if following_ids:
            actions = actions.filter(user_id__in=following_ids)

        # show latest 20 actions
        actions = actions.select_related(
            'user', 'user__profile').prefetch_related('target')[:12]
        # show from latest 20 actions only actions where user created new recipe.
        # actions_new_meal = []
        # for action in actions:
        #     if action.verb == 'Added new recipe.':
        #         actions_new_meal.append(action)
    context = {
        'user': user,
        'actions': actions
    }
    return render(request, "main/home.html", context)


class SearchResultView(ListView, LoginRequiredMixin):
    template_name = "main/search.html"
    model = Recipe

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get('q')
        context["question_query"] = self.request.GET.get('question')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        question = self.request.GET.get('question')
        if question is not None:
            questions = Question.objects.filter(
                Q(title__icontains=question) | Q(content__icontains=question))
            self.count = len(questions)
            return questions

        if query is not None:
            recipe_results = Recipe.objects.filter(title__icontains=query)
            users = Profile.objects.filter(Q(first_name__icontains=query) | Q(
                last_name__icontains=query) | Q(user__username__icontains=query))
            food = Food.objects.filter(name__icontains=query)

            queryset_chain = chain(recipe_results, users, food)

            qs = sorted(queryset_chain,
                        key=lambda instance: instance.slug, reverse=True)
            self.count = len(qs)

            return qs
        return Recipe.objects.none


def register(request):
    if request.method == "POST":
        user_form = NewUserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta'
            message = render_to_string('registration/register_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('register_confirm')
        else:
            if User.objects.filter(username=request.POST.get('username')):
                messages.error(request, 'Nazwa użytkownika jest już zajęta.')
            elif User.objects.filter(email=request.POST.get('email')):
                messages.error(request, 'Podany adres email jest zajęty.')
            else:
                messages.error(request, 'Nazwa użytkownika lub hasło jest niepoprawne.')
    user_form = NewUserForm()
    return render(request, 'registration/register.html', context={'user_form': user_form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Link aktywacyjny jest niepoprawny!')

def register_confirm(request):
    return render(request, 'registration/register_confirm.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)


    