import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import JsonResponse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.decorators.http import require_POST
from django.views.generic import (DeleteView,
                                  UpdateView,
                                  ListView,
                                  DetailView,
                                  CreateView)
from django.views.generic.edit import FormMixin
from taggit.models import Tag
from actions.utils import create_action
from comments.forms import CommentForm
from comments.models import Comment
from food.models import FoodWeight
from profiles.models import Profile
from .forms import RecipeModelForm, IngredientFormSet
from .models import Recipe, RecipeIngredients
from .utils import calculation_based_by_quantity, sum_values_from_dictionary


class UserRecipeBookListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/user_recipes.html'
    context_object_name = 'user_recipes'
    paginate_by = 14

    def get_queryset(self, *args, **kwargs):
        queryset = Recipe.objects.filter(Q(author=self.request.user.profile)
                                        |Q(saved=self.request.user.profile))
        query = self.request.GET.get('q')
        if query:
            return Recipe.objects.filter(Q(title__icontains=query) & Q(author=self.request.user.profile) | Q(saved=self.request.user.profile))
        else:
            return Recipe.objects.filter(Q(author=self.request.user.profile)
                                        |Q(saved=self.request.user.profile))
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(UserRecipeBookListView,
    #                     self).get_context_data(**kwargs)
    #     context['recipes'] = Recipe.objects.filter(Q(author=self.request.user.profile) 
    #                                               |Q(saved=self.request.user.profile))
    #     print(context)
    #     return context


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/main.html'
    context_object_name = 'recipes'
    paginate_by = 14

    def get_queryset(self, *args, **kwargs):
        queryset = Recipe.objects.filter(published=True)
        sorting_query = self.request.GET.get('sort')
        if 'tag' in self.request.GET:
            obj = get_object_or_404(Tag, slug=self.request.GET['tag'])
            return queryset.filter(tags__in=[obj])

        if sorting_query:
            if 'likes-asc' in sorting_query and sorting_query is not None:
                return queryset.order_by('liked')
            if 'likes-desc' in sorting_query and sorting_query is not None:
                return queryset.order_by('-liked')

            if 'date-asc' in sorting_query and sorting_query is not None:
                return queryset.order_by('created')
            if 'date-desc' in sorting_query and sorting_query is not None:
                return queryset.order_by('-created')       

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('sort') 
        return context
    

class RecipeDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Recipe
    template_name = 'recipes/detail.html'
    form_class = CommentForm

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        recipe = Recipe.objects.get(slug=slug)
        return recipe

    def get_success_url(self):
        return reverse('recipes:recipe-detail-view', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        recipe = self.get_object()
        recipes_tags_ids = recipe.tags.values_list('id', flat=True)
        similar_recipes = Recipe.objects.filter(
            tags__in=recipes_tags_ids).filter(published=True).exclude(id=recipe.id)
        similar_recipes = similar_recipes.annotate(
            same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]

        total = recipe.get_nutrition_info()
        per_portion = recipe.get_nutrition_info_with_portions(1, recipe.portions)
        context['current_user'] = current_user
        context['total'] = total.items()
        context['per_portion'] = per_portion.items()
        context['similar_recipes'] = similar_recipes
        context['comments'] = recipe.comments

        context['form'] = CommentForm(initial={'recipe': self.object,
                                               'content_type': recipe.get_content_type,
                                               'object_id': recipe.id})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            parent_obj = None
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()
                    new_comment.parent = parent_obj
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        create_action(
            self.request.user, f"Dodał/a komentarz do {self.get_object}", self.get_object())
        return super(RecipeDetailView, self).form_valid(form)


class RecipeCreateView(LoginRequiredMixin, CreateView):

    template_name = 'recipes/create.html'
    form_class = RecipeModelForm
    queryset = Recipe.objects.all()
    success_url = reverse_lazy('recipes:main-recipe-view')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        ingredient_form = IngredientFormSet()
        ingredient_form.can_delete = False
        for n in ingredient_form:
            n.fields['unit'].queryset = FoodWeight.objects.none()
        return self.render_to_response(self.get_context_data(form=form,
                                                             ingredient_form=ingredient_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = IngredientFormSet(self.request.POST)
        if form.is_valid() and ingredient_form.is_valid():
            return self.form_valid(form, ingredient_form)
        else:
            return self.form_invalid(form, ingredient_form)

    def form_valid(self, form, ingredient_form):
        if ingredient_form.cleaned_data == [{}]:
            messages.warning(
                self.request, 'Musisz wybrać jakieś składniki.')
            return self.form_invalid(form, ingredient_form)
        else:

            self.object = form.save(commit=False)
            self.object.author = self.request.user.profile

            self.object.save()
            form.save_m2m()
            if self.object.published:
                create_action(self.request.user, 'Dodał/a nowy przepis.', self.object)
            ingredient_form.instance = self.object
            ingredient_form.save()
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form)
        )


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipes/confirm_delete.html'
    success_url = reverse_lazy("recipes:main-recipe-view")

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Recipe.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(
                self.request, 'Musisz być autorem tego przepisu aby go usunąć.')
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user.profile:
            raise Http404("Nie jesteś autorem, nie możesz edytować :)")
        return super(RecipeDeleteView, self).dispatch(request, *args, **kwargs)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeModelForm
    template_name = 'recipes/update.html'
    success_url = reverse_lazy('recipes:main-recipe-view')
    object = None

    def get_success_url(self):
        slug = self.object.slug
        return reverse('recipes:recipe-detail-view', kwargs={'slug': slug})

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = RecipeModelForm(
                self.request.POST, instance=self.object)
            context['formset'] = IngredientFormSet(
                self.request.POST, instance=self.object)
        else:
            context['form'] = RecipeModelForm(instance=self.object)
            ingredient_form_set = IngredientFormSet(instance=self.object)
            ingredient_form_set.extra = 0
            ingredient_form_set.min_num = 1
            ingredient_form_set.validate_min = True

            context['formset'] = ingredient_form_set
            for m in ingredient_form_set:
                m.fields['unit'].queryset = FoodWeight.objects.none()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = IngredientFormSet(self.request.POST, instance=self.object)
        formset.min_num = 1
        formset.validate_min = True
        error_list = ['<ul class="errorlist"><li>Proszę wysłać 1 lub więcej formularzy.</li></ul>']
        if(form.is_valid() and formset.is_valid()):
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        if self.object.published:
            create_action(self.request.user,
                          'Zaktualizował/a przepis.', self.object)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


@login_required
def load_weight(request):
    food_id = json.loads(request.body.decode("UTF-8"))
    weights = FoodWeight.objects.filter(
        food_id=food_id['ingredient']).order_by('measure_description')
    return render(request, 'recipes/weight_dropdown_list_options.html', {'weights': weights})


@login_required
def get_recipe(request):
    recipe_id = json.loads(request.body.decode("UTF-8"))
    recipe = Recipe.objects.get(id=recipe_id['recipe'])
    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
    ingredients_dict = {}
    ingredients_id = [i.ingredient.id for i in ingredients]
    ingredients_units_ids = [i.unit.id for i in ingredients]
    ingredients_units = [i.unit.measure_description for i in ingredients]
    for i in range(len(ingredients_id)):
        ingredients_dict[ingredients_id[i]
                         ] = ingredients_units[i], ingredients_units_ids[i]

    return JsonResponse({'ingredients': ingredients_dict, 'portions': recipe.portions})


@login_required
@require_POST
def like_unlike_recipe(request):
    recipe_id = json.loads(request.body.decode("UTF-8"))
    recipe_id = recipe_id['recipe_id']
    recipe_obj = Recipe.objects.get(id=recipe_id)
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if profile in recipe_obj.liked.all():
            recipe_obj.liked.remove(profile)
            return JsonResponse({'message': "Nie lubisz tego przepisu."}, status=201)
        else:
            recipe_obj.liked.add(profile)

        recipe_obj.save()

        create_action(request.user, 'polubił/a twój przepis', recipe_obj)
    return JsonResponse({'message': "Lubisz ten przepis."}, status=201)


@login_required
@require_POST
def add_recipe_to_book(request):
    recipe_id = json.loads(request.body.decode("UTF-8"))
    recipe_id = recipe_id['recipe_id']
    recipe_obj = Recipe.objects.get(id=recipe_id)
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if profile in recipe_obj.saved.all():
            recipe_obj.saved.remove(profile)
            return JsonResponse({'message': 'Przepis został usunięty z twojej książki.'})
        else:
            recipe_obj.saved.add(profile)
        recipe_obj.save()
    return JsonResponse({'message': 'Przepis został dodany do twojej książki.'})


@login_required
def check_recipe(request):
    recipe_id = json.loads(request.body.decode("UTF-8"))
    portions = recipe_id['portions']
    recipe_id = recipe_id['recipe_id']
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_ingredients = recipe.recipeingredients_set.all()
    meal_info = recipe.get_nutrition_info_with_portions(
        float(portions),float(recipe.portions))
    ingredients = [i.get_nutrition_info_based_by_portions(
        float(recipe.portions), float(portions)) for i in recipe_ingredients]
    return JsonResponse({'meal_info': meal_info, 'ingredients': ingredients})
