from django.contrib import admin
from django.forms import ModelForm
from editor.models import Article, Comment


# Register your models here.

class ArticleForm(ModelForm):
    # list_display = ('title', 'created_time', 'last_updated_time')
    # ordering = ('-created_time',)

    class Media:
        css = {
            'all': (
                'https://unpkg.com/@wangeditor/editor@latest/dist/css/style.css',
                '/static/css/editor.css',
            )
        }
        js = (
            'https://unpkg.com/@wangeditor/editor@latest/dist/index.js',
            '/static/js/editor.js',
        )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm
    list_display = ('title', 'created_time', 'last_updated_time')
    ordering = ('-created_time',)

    # class Media:
    #     css = {
    #         'all': (
    #             'https://unpkg.com/@wangeditor/editor@latest/dist/css/style.css',
    #             '/static/css/editor.css',
    #         )
    #     }
    #     js = (
    #         'https://unpkg.com/@wangeditor/editor@latest/dist/index.js',
    #         '/static/js/editor.js',
    #     )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'created_time')
    ordering = ('-created_time',)
