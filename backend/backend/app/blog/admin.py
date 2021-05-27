from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from .models import Post
from .forms import PostForm

@admin.display(
    description='Информация о пользователе', empty_value='unknown', 
    ordering="-timestamp"
    # ordering=Concat('user__username', Value(' '), 'user__email')
)
def upper_case_data(obj):
    '''Кастомизировать вывод колонки'''
    return ("%s %s" % (obj.user.username, obj.user.email))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Удобный фильтр по датам
    date_hierarchy = 'timestamp'
    # Нулевые значения заменные чем-либо
    empty_value_display = '-empty-'
    # Отображать в списке объектов
    list_display = ("__str__", "user", "id", "timestamp", "draft")
    # Что будет являться ссылками на объект
    list_display_links = ("__str__", "user", "id")
    # По чему мозжно фильтровать
    list_filter = ("draft",  ('text', admin.EmptyFieldListFilter))
    # select_related примененный к чему-либо
    list_select_related = ('user',)

    # fields = ("user", ("title", "text"), "picture")
    fieldsets = (
        ("Common options", {
            "fields": (("user", "draft"), ("title", "text"), "picture"),
            "description": "You can change those"
        }),
        ("Advanced options", {
            "classes": ("collapse",),
            "fields": ("id",),
            # "fields": tuple(),
            "description": "Think Before changing"
        }),
    )

    # Можно задать форму
    form = PostForm