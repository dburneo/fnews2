from django.db import models
from django.db import connection

def get_len(query):
    def __len__(self):
        return self.count
    return __len__


class NewsManager(models.Manager):
    def set_len(self, queryset, user=None, media=None):
        params = []
        params.append(user.id)
        where = ""
        if media:
            params.append(media.id)
            where = "where news.media_id = %s::uuid"
        cursor = connection.cursor()
        query = """
            SELECT
               COUNT(news.id)
            FROM
              public.news_news as news
              left join public.news_readlater as rl on (news.id = rl.news_id and rl.user_id = %s)
              {}""".format(where)
        cursor.execute(query, params)
        row = cursor.fetchone()
        queryset.count = row[0]
        setattr(type(queryset), '__len__', get_len(queryset))
        return queryset

    def with_user(self, user, media=None):
        params = []
        params.append(user.id)
        where = ""
        if media:
            params.append(media.id)
            where = "where news.media_id = %s::uuid"
        queryset = self.raw(
            """
            SELECT
               rl.marked as readlater,
               news.id,
               news.link,
               news.title,
               news.short_desc,
               news.language_id,
               news.media_id,
               news."timestamp",
               news.photo,
               news."order"
            FROM
              public.news_news as news
              left join public.news_readlater as rl on (news.id = rl.news_id  and rl.user_id = %s)
              {}""".format(where), params
        )
        return self.set_len(queryset, user=user, media=media)
