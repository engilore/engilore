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

    def _generate_unique_slug(self):
        original_slug = slugify(self.name)
        slug = original_slug
        count = 1

        while Category.objects.filter(slug=slug).exists():
            slug = f'{original_slug}-{count}'
            count += 1

        return slug

    def _set_slug(self):
        if not self.slug or self._is_name_changed():
            self.slug = self._generate_unique_slug()

    def _is_name_changed(self):
        if self.pk:
            existing_name = Category.objects.filter(pk=self.pk).values_list('name', flat=True).first()
            return existing_name != self.name
        return False

    def _is_description_changed(self):
        if self.pk:
            existing_description = Category.objects.filter(pk=self.pk).values_list('description', flat=True).first()
            return existing_description != self.description
        return False

    def _set_meta_title(self):
        if not self.meta_title or self._is_name_changed():
            self.meta_title = self.name

    def _set_meta_description(self):
        if not self.meta_description or self._is_description_changed():
            description_source = self.description or self.name
            self.meta_description = description_source[:155] + '...' if len(description_source) > 155 else description_source

    def save(self, *args, **kwargs):
        self._set_slug()
        self._set_meta_title()
        self._set_meta_description()
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

    def _is_name_changed(self):
        if self.pk:
            existing_name = Topic.objects.filter(pk=self.pk).values_list('name', flat=True).first()
            return existing_name != self.name
        return False

    def _is_description_changed(self):
        if self.pk:
            existing_description = Topic.objects.filter(pk=self.pk).values_list('description', flat=True).first()
            return existing_description != self.description
        return False

    def _generate_meta_title(self):
        if not self.meta_title or self._is_name_changed():
            self.meta_title = self.name

    def _generate_meta_description(self):
        if not self.meta_description or self._is_description_changed():
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
