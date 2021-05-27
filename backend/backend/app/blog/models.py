from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """Пост на стенку"""
    user = models.ForeignKey(
        User, verbose_name="Пользователь", db_index=True,
        related_name="posts", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField("Заголовок", max_length=100, null=True)
    text = models.TextField("Текст поста", max_length=500, null=True)
    picture = models.ImageField(upload_to="pics/%Y/%m/%d", null=True)
    draft = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user}'s post"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Comment(models.Model):
    """Комментарий к посту"""
    post = models.ForeignKey(
        Post, verbose_name="Пост", db_index=True,
        related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", 
        on_delete=models.CASCADE
    )
    content = models.TextField("Содержимое", max_length=200)
    
    def __str__(self):
        return f"comment to a {self.post}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

class Like(models.Model):
    """Лайк"""
    post = models.ForeignKey(
        Post, verbose_name="Пост", 
        related_name="likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", 
        related_name="liked", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} likes {self.post}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ("user", "post")