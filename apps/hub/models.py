from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
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
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def generate_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        else:
            old_instance = Project.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.name != self.name:
                self.slug = self.generate_slug()
        super().save(*args, **kwargs)


class Resource(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name=_('Project'),
        on_delete=models.CASCADE,
        related_name='resources'
    )
    name = models.CharField(
        verbose_name=_('Resource Name'),
        max_length=100,
        null=False,
        blank=False
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=100,
        unique=True,
        null=False,
        blank=True
    )
    url = models.URLField(
        verbose_name=_('Resource URL'),
        null=False,
        blank=False
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated At'),
        auto_now=True,
    )

    class Meta:
        verbose_name = _('Resource')
        verbose_name_plural = _('Resources')
        unique_together = ('project', 'name')
        ordering = ['created_at'] 

    def __str__(self):
        return f"{self.name} for {self.project.name}"

    def generate_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        num = 1
        while Resource.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        else:
            old_instance = Resource.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.name != self.name:
                self.slug = self.generate_slug()
        super().save(*args, **kwargs)