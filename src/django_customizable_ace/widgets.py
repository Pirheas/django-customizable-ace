from django import forms
from django.conf import settings
from django.template import Template, Context
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text


DEFAULT_CONFIG = {'theme': 'monokai',
                  'lang': 'python',
                  'readonly': False,
                  'width': '700px',
                  'height': '400px'}


class AceWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        self._readonly = bool(self._get_config('readonly', kwargs))
        self._theme = self._get_config('theme', kwargs)
        self._langage = self._get_config('lang', kwargs)
        self._width = self._get_config('width', kwargs)
        self._height = self._get_config('height', kwargs)
        super(AceWidget, self).__init__(*args, **kwargs)


    @staticmethod
    def _get_config(label, kwargs):
        llabel = str(label).lower()
        ulabel = 'ACE_{0}'.format(str(label).upper())
        if llabel in kwargs:
            return kwargs.pop(llabel)
        if hasattr(settings, ulabel):
            return getattr(settings, ulabel)
        return DEFAULT_CONFIG[llabel]

    @staticmethod
    def _required_js():
        return ('django_customizable_ace/ace/ace.js',
                'django_customizable_ace/js/ace_widget.js',)

    @staticmethod
    def _required_css():
        return {'screen': ['django_customizable_ace/css/ace_widget.css']}

    @property
    def media(self):
        css = self._required_css()
        js = self._required_js()
        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None):
        ctx = {'class_name': 'ace-editor',
               'code': value or '',
               'id': name,
               'width': self._width,
               'height': self._height,
               'default_theme': self._theme,
               'default_lang': self._langage,
               'read_only': self._readonly}
               
        template = Template(self._get_template_content())
        context = Context(ctx)
        return mark_safe(template.render(context))

    @staticmethod
    def _get_template_content():
        import os
        filedir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(filedir, 'templates', 'ace_widget.html')
        with open(template_path, 'r') as f:
            return f.read()

