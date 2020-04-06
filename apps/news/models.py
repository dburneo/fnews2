from django.db import models
from django.utils.encoding import smart_str
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from . import managers

from ..media import models as ModelsMedia

import uuid, random, time, requests, datetime

def order_random():
    random.seed(time.time())
    return random.randint(1, 10000)


class News(models.Model):
    # TODO: Define fields here
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.URLField()
    title = models.TextField()
    short_desc = models.TextField(null=True)
    # tags = models.ManyToManyField("Tag", blank=True)
    media = models.ForeignKey("media.Media", on_delete=models.CASCADE)
    language = models.ForeignKey("country.Language", null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(null=True, max_length=380)
    order = models.IntegerField(default=order_random)
    long_desc = models.TextField(null=True)

    def get_next(self):
        next = News.objects.filter(id__gt=self.id)
        if next:
            return next.first()
        return False

    def get_prev(self):
        prev = News.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first()
        return False

    class Meta:
        verbose_name = "New"
        verbose_name_plural = "News"
        unique_together = ("link", "title")


# class Tag(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.TextField()

#     class Meta:
#         verbose_name = "Tag"
#         verbose_name_plural = "Tags"


class ReadLater(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey("News", related_name='%(app_label)s_%(class)s_news', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_news', on_delete=models.CASCADE)
    readed = models.BooleanField(default=False)
    marked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ReadLater"
        verbose_name_plural = "ReadLaters"

    def __str__(self):
        return self.news


class NewsWithRead(models.Model):
    # TODO: Define fields here
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.URLField()
    title = models.TextField()
    short_desc = models.TextField(null=True)
    # tags = models.ManyToManyField("Tag", blank=True)
    media = models.ForeignKey("media.Media", on_delete=models.CASCADE)
    language = models.ForeignKey("country.Language", null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(null=True)
    order = models.IntegerField(default=order_random)
    readlater = models.BooleanField(default=False)

    objects = managers.NewsManager()

    class Meta:
        db_table = 'news_news'
        managed = False


class FollowNew(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey("News", related_name='%(app_label)s_%(class)s_news', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_news', on_delete=models.CASCADE)
    readed = models.BooleanField(default=False)
    marked = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    until = models.DateTimeField(null=True)


    def save(self, *args, **kwargs):
        new = self.news
        out = new.short_desc
        out = out.replace(u'\u2018', u"'")
        out = out.replace(u'\u2019', u"'")
        out = out.replace(u'\u201c', u'"')
        description = out.replace(u'\u201d', u'"')

        from datetime import timedelta, datetime
        from ..news.views import busqueda
        duration = timedelta(days=60)
        ahora = datetime.now()
        hasta = ahora + duration

        if self.marked == True:
            e = Verbs.objects.filter(news=new.pk)
            if e.exists():
                e = e.get()
                self.content = e.content
                self.until = hasta
            else:
                url = 'https://language.googleapis.com/v1/documents:analyzeEntities?fields=entities%2Fname&key=' + settings.API_KEY
                headers = {
                    'content-type': "application/json",
                    'cache-control': "no-cache",
                }
                payload = "{\r\n \"document\": {\r\n  \"content\": \""+str(description)+"\",\r\n  \"type\": \"PLAIN_TEXT\"\r\n },\r\n \"encodingType\": \"UTF8\"\r\n}"
                response = requests.request("POST", url, data=payload, headers=headers)
                json = response.json()
                respuesta = json
                print(response.text)
                keys = ''
                list=[]
                for each in respuesta['entities']:
                    list.append(each['name'])
                e1 = Verbs(news=new, content=list)
                e1.save()
                self.content = e1.content
                self.until = hasta

                busqueda(new, list)

            super(FollowNew, self).save(*args, **kwargs)
        else:
            super(FollowNew, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "FullNewsText"
        verbose_name_plural = "FullNewsTexts"

    def __str__(self):
        return self.news


class MediaInterest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media = models.ForeignKey(ModelsMedia.Media, verbose_name='Medio de Prensa', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_news', on_delete=models.CASCADE)
    marked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Medios de interes"
        verbose_name_plural = "Medios de Interes"

    def __str__(self):
        return self.media


class Verbs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey("News", related_name='%(app_label)s_%(class)s_news', on_delete=models.CASCADE)
    content = models.TextField(default='algo')


class Meta:
    verbose_name = "Verbs"
    verbose_name_plural = "Verbs"


def __str__(self):
    return self.news
