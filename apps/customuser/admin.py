from django.contrib import admin
from apps.customuser.models import User
from apps.country.models import Country
from apps.media.models import Media
from apps.news.models import News


admin.site.register(User)
admin.site.register(Country)
admin.site.register(Media)
admin.site.register(News)

# admin.site.register(UserAdmin)
