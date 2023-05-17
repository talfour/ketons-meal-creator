from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import (DeleteView,
                                  UpdateView,
                                  ListView,
                                  DetailView,
                                  CreateView)
from .models import Food
from .forms import FoodModelForm


class FoodListView(ListView):

    """Show all default ingredients and users ingredients which can be used to prepare a recipe."""

    model = Food
    template_name = 'food/main.html'
    context_object_name = 'food'
    paginate_by = 80

    def get_queryset(self):
        """Filtered foods by default foods and user custom foods"""
        self.author = self.request.user
        return Food.objects.filter(Q(user=self.author.profile) | Q(user=1))


class FoodCreateView(CreateView):

    """Create food which can be used to prepare recipes."""

    model = Food
    form_class = FoodModelForm
    template_name = 'food/create.html'
    context_object_name = 'food'


class FoodDetailView(DetailView):

    """Show information details about food"""

    model = Food
    template_name = 'food/details.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        food = Food.objects.get(slug=slug)
        return food

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Food.objects.get(slug=self.kwargs.get('slug'))
        context["nutri_values"] = obj.get_info()
        return context
