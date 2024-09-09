from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from account.models import User
from category.models import Category, Topic
from blog.validators import capitalize_words
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
    volume = models.CharField(
        max_length=10,
        null=True,
        blank=True,
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
        default='journal',
        null=False,
        blank=False
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
            original_slug = slugify(self.title)
            if self.volume:
                original_slug = f'{original_slug}-volume-{self.volume}'
            
            slug = original_slug
            count = 1

            while Post.objects.filter(slug=slug).exists():
                slug = f'{original_slug}-{count}'
                count += 1

            self.slug = slug

    def _generate_meta_title(self):
        if not self.meta_title:
            self.meta_title = self.title
            if self.volume:
                self.meta_title = f'{self.meta_title} | Volume {self.volume}'

    def _generate_meta_description(self):
        if not self.meta_description:
            description_source = self.summary or self.content
            self.meta_description = description_source[:155] + '...' if len(description_source) > 155 else description_source
        
    def save(self, *args, **kwargs):
        self.title = capitalize_words(self.title)
        self._generate_slug()
        self._generate_meta_title()
        self._generate_meta_description()

        if self.status == 'published' and self.published_at is None:
            self.published_at = timezone.now()

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
