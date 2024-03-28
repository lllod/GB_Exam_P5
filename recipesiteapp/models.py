from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Recipe(models.Model):
    DIF_CHOICE = (
        ('1', 'Легко'),
        ('2', 'Средне'),
        ('3', 'Сложно'),
        ('4', 'Эксперт'),
        ('5', 'Ивлев'),
    )

    name = models.CharField(max_length=48)
    description = models.TextField()
    cooking_steps = models.TextField()
    cooking_time = models.IntegerField(default=0)
    img = models.ImageField(upload_to='recipe_images')
    difficulty = models.CharField(max_length=8, choices=DIF_CHOICE, default='1')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    addition_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.id})


class Category(models.Model):
    name = models.CharField(max_length=24)
    recipes = models.ManyToManyField(Recipe, through='RecipesCategories')

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class RecipesCategories(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Рецепты по категориям'

    def __str__(self):
        return self.category.name
