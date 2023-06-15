from django.db import models


class Tags(models.Model):

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        unique=True,
    )
    color = models.CharField(
        max_length=150,
        verbose_name='Цветовой HEX-код',
        unique=True
    )
    slug = models.CharField(
        max_length=150,
        verbose_name='Slug',
        unique=True
    )

    def __str__(self):
        return self.name
