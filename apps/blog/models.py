from django.db import models
from django.utils.text import slugify

from account.models import User
from category.models import Category, Topic
from blog.constants import POST_STATUS, POST_TYPE


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
        )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
        )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False
        )
    summary = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        )
    content = models.TextField(
        null=False,
        blank=False
        )
    featured_image = models.ImageField(
        upload_to='featured_img/',
        null=True,
        blank=True,
        )
    category = models.ManyToManyField(
        Category,
        related_name='posts',
        blank=False
        )
    topics = models.ManyToManyField(
        Topic,
        related_name='posts',
        blank=False
        )
    status = models.CharField(
        max_length=10,
        choices=POST_STATUS,
        default='draft'
        )
    type = models.CharField(
        max_length=10,
        choices=POST_TYPE,
        default='journal'
        )
    meta_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    meta_description = models.CharField(
        max_length=300,
        null=False,
        blank=True,
    )
    is_featured = models.BooleanField(
        default=False,
        null=False,
        blank=True
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
        )
    
    def _generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)

    def _generate_meta_title(self):
        if not self.meta_title:
            self.meta_title = self.title

    def _generate_meta_description(self):
        if not self.meta_description:
            description_source = self.summary or self.content
            self.meta_description = description_source[:155] + '...' if len(description_source) > 155 else description_source

    def save(self, *args, **kwargs):
        self._generate_slug()
        self._generate_meta_title()
        self._generate_meta_description()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['published_at']),
        ]
