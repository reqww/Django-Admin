from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import ngettext
from django.contrib import messages

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


@admin.display(description='Лайки')
def count_likes(obj):
    return obj.likes.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    @admin.action(description='Make published', permissions=['change'])
    def make_published(self, request, queryset):
        updated = queryset.update(draft=False)
        self.message_user(request, ngettext(
            '%d post was successfully marked as published.',
            '%d posts were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)

    # Удобный фильтр по датам
    date_hierarchy = 'timestamp'
    # Нулевые значения замененные чем-либо
    empty_value_display = '-empty-'
    # Отображать в списке объектов
    list_display = ("__str__", count_likes,  "user", "id", "timestamp", "draft")
    # Что будет являться ссылками на объект
    list_display_links = ("__str__", "user", "id")
    # По чему мозжно фильтровать
    list_filter = ("draft",  ('text', admin.EmptyFieldListFilter), ("likes", admin.EmptyFieldListFilter))
    # select_related примененный к чему-либо
    list_select_related = ('user',)
    # Поля для айди
    raw_id_fields = ("user",)
    # Только для чтения
    readonly_fields = ("timestamp",)
    # Сохранять как новый
    save_as = True
    # Кнопки вверху и внизу
    # save_on_top = True
    # Искать по след. полям
    search_fields = ['user__email']
    # Пользовательские действия
    actions = [make_published]


    # fields = ("user", ("title", "text"), "picture")
    fieldsets = (
        ("Common options", {
            "fields": (("user", "timestamp", "draft"), ("title", "text"), "picture"),
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