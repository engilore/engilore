from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from account.models import User
from category.models import Category, Topic
from blog.constants import STATUS_CHOICES, TYPE_CHOICES


class Volume(models.Model):
    number = models.PositiveIntegerField(
        verbose_name=_('Volume Number'),
        unique=True
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        unique=True
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Volume')
        verbose_name_plural = _('Volumes')
        ordering = ['-number']

    def __str__(self):
        return f"Volume {self.number}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"volume-{self.number}-{self.title}")
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        unique=False,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
        null=False,
        blank=True
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name='blog_posts'
    )
    topics = models.ManyToManyField(
        Topic,
        verbose_name=_('Topics'),
        related_name='blog_posts',
        blank=True
    )
    post_type = models.CharField(
        verbose_name=_('Post Type'),
        max_length=20,
        choices=TYPE_CHOICES,
        default='journal',
        null=False,
        blank=False
    )
    content = models.TextField(
        verbose_name=_('Content'),
        null=False,
        blank=False
    )
    thumbnail = models.ImageField(
        verbose_name=_('Thumbnail'),
        upload_to='blog_thumbnail/',
        null=True,
        blank=True,
    )
    volume = models.ForeignKey(
        Volume,
        verbose_name=_('Volume'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts'
    )
    meta_title = models.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        null=True,
        blank=True,
    )
    meta_description = models.TextField(
        verbose_name=_('Meta Description'),
        max_length=160,
        null=True,
        blank=True,
    )
    meta_keywords = models.CharField(
        verbose_name=_('Meta Keywords'),
        max_length=255,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        null=False,
        blank=False
    )
    is_featured = models.BooleanField(
        verbose_name=_('Is Featured'),
        default=False,
        null=False,
        blank=False
    )
    is_spotlighted = models.BooleanField(
        verbose_name=_('Is Spotlighted'),
        default=False,
        null=False,
        blank=False
    )
    published_at = models.DateTimeField(
        verbose_name=_('Published At'),
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True
    )

    def __str__(self):
        return self.title

    def generate_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def generate_meta_title(self):
        return self.title

    def generate_meta_description(self):
        if len(self.content) > 157:
            return self.content[:157] + '...'
        return self.content

    def generate_meta_keywords(self):
        keywords = self.title.split() + self.content.split()[:10]
        return ', '.join(keywords)

    def save(self, *args, **kwargs):
        old_instance = None
        if self.pk:
            old_instance = BlogPost.objects.filter(pk=self.pk).first()

        if not self.slug or (old_instance and old_instance.title != self.title):
            self.slug = self.generate_slug()

        if not self.meta_title or (old_instance and old_instance.title != self.title):
            self.meta_title = self.generate_meta_title()

        if not self.meta_description or (old_instance and old_instance.content != self.content):
            self.meta_description = self.generate_meta_description()

        if not self.meta_keywords or (
            old_instance and (old_instance.title != self.title or old_instance.content != self.content)
        ):
            self.meta_keywords = self.generate_meta_keywords()

        if self.is_spotlighted:
            BlogPost.objects.filter(is_spotlighted=True).update(is_spotlighted=False)

        if self.status == 'published' and self.published_at is None:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')
        ordering = ['-published_at']
