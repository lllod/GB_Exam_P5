from django import forms
from .models import Recipe, Category, RecipesCategories


class RecipeAddForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.SelectMultiple(
        attrs={'class': 'form-control', 'multiple': 'multiple'}), label='Категории')

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_steps', 'cooking_time', 'img', 'difficulty', 'categories']
        labels = {
            'name': 'Название',
            'description': 'Краткое описание',
            'cooking_steps': 'Этапы приготовления',
            'cooking_time': 'Время приготовления (мин.)',
            'img': 'Изображение готового блюда',
            'difficulty': 'Сложность',
            'categories': 'Категории',
        }
        widgets = {
            'author': forms.HiddenInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
            for category in self.cleaned_data['categories']:
                RecipesCategories.objects.create(recipe=instance, category=category)
        return instance
