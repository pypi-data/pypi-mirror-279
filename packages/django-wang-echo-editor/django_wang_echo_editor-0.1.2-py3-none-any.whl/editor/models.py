from django.db import models
from wang_editor.fields import WangEditorField


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_time',)
        verbose_name = '文章'
        verbose_name_plural = '文章'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='所属文章')
    content = WangEditorField(verbose_name='内容')
    desc = WangEditorField(verbose_name='简介', default='')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.article.title + ' 的评论'

    class Meta:
        ordering = ('-created_time',)
        verbose_name = '评论'
        verbose_name_plural = '评论'
