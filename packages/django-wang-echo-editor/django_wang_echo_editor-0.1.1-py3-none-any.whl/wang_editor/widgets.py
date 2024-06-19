from copy import deepcopy

from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.safestring import mark_safe
from django.conf import settings
from js_asset import JS


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super().default(obj)


json_encode = LazyEncoder().encode


class WangEditorWidget(forms.Textarea):
    class Media:
        custom_css = settings.WANG_EDITOR_CONFIG.get('custom_css', [])  # 获取配置文件中的自定义css
        custom_js = settings.WANG_EDITOR_CONFIG.get('custom_js', [])  # 获取配置文件中的自定义js
        origin_js = settings.WANG_EDITOR_CONFIG.get('origin_js', None)  # 获取配置文件中的wangEditor的js文件
        flatatt_js = []
        for i in range(len(custom_js)):
            flatatt_js.append(JS(custom_js[i], {
                'id': 'wang_edit_custom' + str(i),
            }))
        css = {
            'all': (
                '/static/wang_editor/css/wangeditor5.min.css',
                'wang_editor/css/editor.css',
                *custom_css
            )
        }
        js = (
            origin_js or '/static/wang_editor/js/wangeditor5.min.js',
            JS('wang_editor/js/editor_init.js', {
                'id': 'wang_editor_init',
            }),
            *flatatt_js
        )

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.wang_editor_config = deepcopy(settings.WANG_EDITOR_CONFIG or {})

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        print(final_attrs)
        return mark_safe(
            renderer.render('widget.html', {
                'id': attrs.get('id'),
                'value': value or '',
                'final_attrs': flatatt(final_attrs),
                'toolbar_config': json_encode(self.wang_editor_config.get('toolbar_config', {})),
                'editor_config': json_encode(self.wang_editor_config.get('editor_config', {})),
            })
        )

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        This is combination of the same method from Django<=1.10 and Django1.11+
        """
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs
