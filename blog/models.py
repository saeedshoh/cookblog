from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(verbose_name="Название", max_length=100)
    slug = models.SlugField(verbose_name="Слаг", max_length=100)
    parent = TreeForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children'
        )
    
    class MPTTMeta:
        order_insertion_by = ['name']

class Tag(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    slug = models.SlugField(verbose_name="Слаг", max_length=100)

class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Загаловка", max_length=200)
    image = models.ImageField(upload_to="articles/")
    text = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(
        Category, 
        related_name='post', 
        on_delete=models.SET_NULL, 
        null=True)
    tags = models.ManyToManyField(Tag, related_name='post')
    created_at = models.DateTimeField(auto_now_add=True)

class Recipe(models.Model):
    name = models.CharField(verbose_name="Название", max_length=100)
    serves = models.CharField(max_length=50)
    prep_time = models.PositiveIntegerField(default=0)
    cook_time = models.PositiveIntegerField(default=0)
    indegrens = models.TextField()
    directions = models.TextField()
    post = models.ForeignKey(
        Post, 
        related_name='recipe'
        on_delete=models.SET_NULL,
        null=True
        )
    
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)