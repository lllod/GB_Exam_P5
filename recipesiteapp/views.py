from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Recipe
from .forms import RecipeAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


def about(request):
    return render(request, 'recipesiteapp/about.html')


class RecipeView(DetailView):
    model = Recipe


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipesiteapp/index.html'
    context_object_name = 'recipes'
    ordering = ['-addition_date']

    def get_queryset(self):
        return super().get_queryset().order_by('?')[:6]


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeAddForm
    template_name = 'recipesiteapp/recipe_form.html'
    success_url = reverse_lazy('recipe', kwargs={'pk': model.objects.last().pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Recipe
    fields = ['name', 'description', 'cooking_steps', 'cooking_time', 'img', 'difficulty']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class RecipeDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


class AuthorRecipeListView(ListView):
    model = Recipe
    template_name = 'recipesiteapp/user_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        return Recipe.objects.filter(author=author).order_by('-addition_date')
