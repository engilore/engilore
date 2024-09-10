from django.db import models
from django.utils.text import slugify

from account.models import User


class Category(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_categories',
        )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False
        )
    description = models.TextField(
        null=True,
        blank=True
        )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
        )
    meta_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        )
    meta_description = models.CharField(
        max_length=300,
        null=True,
        blank=True,
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
            original_slug = slugify(self.name)
            slug = original_slug
            count = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f'{original_slug}-{count}'
                count += 1

            self.slug = slug

    def _generate_meta_title(self):
        if not self.meta_title:
            self.meta_title = self.name

    def _generate_meta_description(self):
        if not self.meta_description:
            description_source = self.description or self.name
            self.meta_description = description_source[:155] + '...' if len(description_source) > 155 else description_source

    def save(self, *args, **kwargs):
        self._generate_slug()
        self._generate_meta_title()
        self._generate_meta_description()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
        ]



class Topic(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_topics',
        )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False
        )
    description = models.TextField(
        null=True,
        blank=True
        )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        null=False,
        blank=True
        )
    category = models.ForeignKey(
        Category,
        related_name='topics',
        on_delete=models.CASCADE
        )
    meta_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        )
    meta_description = models.CharField(
        max_length=300,
        null=True,
        blank=True,
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
            original_slug = slugify(self.name)
            slug = original_slug
            count = 1

            while Topic.objects.filter(slug=slug).exists():
                slug = f'{original_slug}-{count}'
                count += 1

            self.slug = slug

    def _generate_meta_title(self):
        if not self.meta_title:
            self.meta_title = self.name

    def _generate_meta_description(self):
        if not self.meta_description:
            description_source = self.description or self.name
            self.meta_description = description_source[:155] + '...' if len(description_source) > 155 else description_source

    def save(self, *args, **kwargs):
        self._generate_slug()
        self._generate_meta_title()
        self._generate_meta_description()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
            models.Index(fields=['category_id']),
        ]
