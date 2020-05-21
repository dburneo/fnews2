from django.db import models
from django.urls import reverse, reverse_lazy
from autoslug import AutoSlugField

import uuid

class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    url = models.URLField()
    languages = models.ManyToManyField("country.Language", blank=True)
    country = models.ForeignKey("country.Country", related_name='medias', on_delete=models.CASCADE)
    # city = models.ForeignKey("country.City", null=True, blank=True, related_name='medias')
    slug = AutoSlugField(populate_from='name', unique=True)
    visible = models.BooleanField('¿Tiene vista previa?', default=True)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medias"

    def __str__(self):
        return self.name

    def get_news_url(self):
        return reverse_lazy("news", kwargs={"slug": self.slug})


class DefaultMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
