from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        verbose_name=_('Category Name'),
        max_length=255,
        unique=True,
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
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True
    )
    meta_title = models.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        blank=True,
        null=True,
    )
    meta_description = models.TextField(
        verbose_name=_('Meta Description'),
        max_length=160,
        blank=True,
        null=True,
    )
    meta_keywords = models.CharField(
        verbose_name=_('Meta Keywords'),
        max_length=255,
        blank=True,
        null=True,
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
        return self.name

    def generate_slug(self):
        return slugify(self.name)

    def generate_meta_title(self):
        return self.name

    def generate_meta_description(self):
        if self.description:
            return self.description[:157] + '...' if len(self.description) > 157 else self.description
        return f"All posts in the {self.name} category."

    def generate_meta_keywords(self):
        keywords = self.name.split()
        if self.description:
            keywords += self.description.split()[:10]
        return ', '.join(keywords)

    def save(self, *args, **kwargs):
        old_instance = None
        if self.pk:
            old_instance = Category.objects.filter(pk=self.pk).first()

        if not self.slug or (old_instance and old_instance.name != self.name):
            self.slug = self.generate_slug()

        if not self.meta_title or (old_instance and old_instance.name != self.name):
            self.meta_title = self.generate_meta_title()

        if not self.meta_description or (old_instance and old_instance.description != self.description):
            self.meta_description = self.generate_meta_description()

        if not self.meta_keywords or (
            old_instance and (old_instance.name != self.name or old_instance.description != self.description)
        ):
            self.meta_keywords = self.generate_meta_keywords()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']


class Topic(models.Model):
    name = models.CharField(
        verbose_name=_('Topic Name'),
        max_length=255,
        null=False,
        blank=True
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        related_name='topics'
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True
    )
    meta_title = models.CharField(
        verbose_name=_('Meta Title'),
        max_length=255,
        blank=True,
        null=True,
    )
    meta_description = models.TextField(
        verbose_name=_('Meta Description'),
        max_length=160,
        blank=True,
        null=True,
    )
    meta_keywords = models.CharField(
        verbose_name=_('Meta Keywords'),
        max_length=255,
        blank=True,
        null=True,
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
        return self.name

    def generate_slug(self):
        return slugify(self.name)

    def generate_meta_title(self):
        return self.name

    def generate_meta_description(self):
        if self.description:
            return self.description[:157] + '...' if len(self.description) > 157 else self.description
        return f"Explore posts related to {self.name}."

    def generate_meta_keywords(self):
        keywords = self.name.split()
        if self.description:
            keywords += self.description.split()[:10]
        return ', '.join(keywords)

    def save(self, *args, **kwargs):
        old_instance = None
        if self.pk:
            old_instance = Topic.objects.filter(pk=self.pk).first()

        if not self.slug or (old_instance and old_instance.name != self.name):
            self.slug = self.generate_slug()

        if not self.meta_title or (old_instance and old_instance.name != self.name):
            self.meta_title = self.generate_meta_title()

        if not self.meta_description or (old_instance and old_instance.description != self.description):
            self.meta_description = self.generate_meta_description()

        if not self.meta_keywords or (
            old_instance and (old_instance.name != self.name or old_instance.description != self.description)
        ):
            self.meta_keywords = self.generate_meta_keywords()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['name']
