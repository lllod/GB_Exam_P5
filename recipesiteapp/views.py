from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Recipe, Category
from .forms import RecipeAddForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


def about(request):
    return render(request, 'recipesiteapp/about.html')


class RecipeView(DetailView):
    model = Recipe
    template_name = 'recipesiteapp/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cooking_steps = self.object.cooking_steps.split('\n')
        context['categories'] = Category.objects.filter(recipescategories__recipe=self.object)
        context['cooking_steps'] = cooking_steps
        return context


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipesiteapp/index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return super().get_queryset().order_by('?')[:6]


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeAddForm
    template_name = 'recipesiteapp/recipe_form.html'
    success_url = reverse_lazy('recipe')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe', kwargs={'pk': self.object.pk}) if self.object else reverse_lazy('recipe')


class RecipeUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Recipe
    template_name = 'recipesiteapp/recipe_form_upd.html'
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


class LastRecipeListView(ListView):
    model = Recipe
    template_name = 'recipesiteapp/last-recipes.html'
    context_object_name = 'recipes'
    paginate_by = 6
    ordering = ['-addition_date']


class CategoryRecipeListView(ListView):
    model = Recipe
    template_name = 'recipesiteapp/category_list.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return category.recipes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, id=self.kwargs['category_id'])
        context['category'] = category
        return context
