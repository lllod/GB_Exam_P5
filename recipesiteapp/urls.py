from django.urls import path
from . import views
from .views import RecipeView, RecipeCreateView, RecipeUpdateView, RecipeDeleteView, RecipeListView, \
    AuthorRecipeListView, LastRecipeListView, CategoryRecipeListView

urlpatterns = [
    path('', RecipeListView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('recipe/<int:pk>/', RecipeView.as_view(), name='recipe'),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/upd/', RecipeUpdateView.as_view(), name='recipe-upd'),
    path('recipe/<int:pk>/del/', RecipeDeleteView.as_view(), name='recipe-del'),
    path('author/<str:username>/', AuthorRecipeListView.as_view(), name='author-posts'),
    path('recipe/last/', LastRecipeListView.as_view(), name='last-recipes'),
    path('category/<int:category_id>/', CategoryRecipeListView.as_view(), name='category-list'),
]
