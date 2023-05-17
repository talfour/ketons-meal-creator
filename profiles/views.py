import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .forms import AddNewMealForm, ProfileModelForm
from .models import Profile
from .models import UserFollows
from actions.utils import create_action
from recipes.models import Recipe, RecipeEvent, RecipeIngredients
from recipes.utils import sum_values_from_dictionary


class ProfileListView(ListView, LoginRequiredMixin):
    model = Profile
    template_name = 'profiles/profile-list.html'
    context_object_name = 'profiles'
    paginate_by = 30
    ordering = ('followers')


class ProfileDetailView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'profiles/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(slug=self.kwargs.get('slug'))
        followers = profile.following.all()
        is_following = followers.filter(
            following_user_id=self.request.user.profile).exists()
        profile_recipes = Recipe.objects.filter(author=profile)
        context = {'total_followers': followers.count(),
                   'is_following': is_following,
                   'profile': profile,
                   'profile_recipes': profile_recipes, }
        return context


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None,
                            request.FILES or None, instance=profile)

    confirm = False
    if request.method == "POST" and 'update_profile' in request.POST:
        if form.is_valid():
            form.save()
            confirm = True

    total_followers = profile.followers.all()
    total_following = profile.following.all()
    context = {
        'profile': profile,
        'total_followers': total_followers,
        'total_following': total_following,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/myprofile.html', context)


@login_required
def following_users_list(request):
    user = request.user
    followed_people = user.profile.following.all()
    followed_profiles = [f.following_user_id for f in followed_people]
    meals = Recipe.objects.filter(
        author__in=followed_profiles, published=True).order_by('-created')
    paginator = Paginator(meals, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_paginated = True if paginator.num_pages > 1 else False
    try:
        meal = paginator.page(page_number)
    except PageNotAnInteger:
        meal = paginator.page(1)
    except EmptyPage:
        meal = paginator.page(paginator.num_pages)
    context = {
        'user': user,
        'followed_users_meals': meal,
        'page_obj':page_obj,
        'is_paginated': is_paginated
    }
    return render(request, "profiles/following.html", context)


@login_required
def user_calendar(request):
    return render(request, "profiles/calendar.html")


@login_required
def calendar_day_details(request, date):
    date_year = date.strftime('%Y-%m-%d')
    day_meals = RecipeEvent.objects.filter(
        user=request.user.profile).filter(date=date_year).select_related('recipe').annotate(count=Count('recipe'))
    request.session['day'] = date.strftime('%Y-%m-%d')
    # to zwraca wartości dla danego meala i ingredient dla meala włącznie z ilością
    meal_info = []
    ingredients = []
    for meal in day_meals:
        meal_info.append(meal.recipe.get_nutrition_info_with_portions(
            meal.portions, meal.recipe.portions))
        recipe = {'meal':meal.recipe.title}
        
        recipe['total_nutrition'] = meal.recipe.get_nutrition_info_with_portions(
            meal.portions, meal.recipe.portions)
        recipe['portions'] = meal.portions
        recipe['id'] = meal.id
        recipe['user_choosen_name'] = meal.description
        recipe['image'] = meal.recipe.images.url
        recipe['slug'] = meal.recipe.slug
        recipe['time'] = meal.time
        ingredients.append(recipe)
        for i in meal.recipe.recipeingredients_set.all():
            recipe[i.ingredient.name] = i.get_nutrition_info_based_by_portions(meal.recipe.portions, meal.portions)

    total_nutrition = sum_values_from_dictionary(meal_info)
    context = {
        'date': date_year,
        'day_meals':day_meals,
        'meal_info':meal_info,
        'ingredients':ingredients,
        'total_nutrition':total_nutrition,
    }

    return render(request, "profiles/calendar-detail.html", context )


@login_required
def add_new_meal_to_day(request):
    day = request.session['day']
    user = request.user.profile
    if request.method == "POST":
        form = AddNewMealForm(user, request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.date = day
            post.save()
            day_fixed = day.replace("-", "")
            return HttpResponseRedirect(reverse('profiles:calendar-detail', kwargs={'date': day_fixed}))
    else:
        form = AddNewMealForm(user)
    return render(request, 'profiles/calendar-detail-new-meal.html', {'form': form})


@login_required
def delete_meal_from_day(request, pk):
    try:
        instance = RecipeEvent.objects.get(id=pk)
    except RecipeEvent.DoesNotExist:
        instance = None
    if request.user.profile != instance.user:
        raise PermissionDenied
    else:
        day = request.session['day']
        day_fixed = day.replace("-", "")
        instance.delete()
    return HttpResponseRedirect(reverse('profiles:calendar-detail', kwargs={'date': day_fixed}))


@login_required
def user_follow(request):
    user = Profile.objects.get(id=request.user.id)
    following_user = json.loads(request.body.decode("UTF-8"))
    following_user_id = following_user['following_user']
    follow = Profile.objects.get(id=following_user_id)
    is_following = UserFollows.objects.filter(
        user_id=follow, following_user_id=user)
    if request.method == "POST":
        if is_following.exists():
            is_following.delete()
            return JsonResponse({'message': 'Już nie obserwujesz tej osoby.'}, status=201)
        else:
            UserFollows.objects.create(user_id=follow, following_user_id=user)
            create_action(request.user, "Obserwuje", follow)
            return JsonResponse({'message': 'Obserwujesz tą osobę.'}, status=201)
    return JsonResponse({'message': 'Obserwujesz tą osobę.'})
