from django.db import models


class Category(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Topic(models.Model):
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'topic'
        verbose_name_plural = 'topics'