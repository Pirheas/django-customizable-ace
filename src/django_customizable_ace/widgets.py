from django import forms
from django.conf import settings
from django.template import Template, Context
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text


DEFAULT_CONFIG = {'theme': 'monokai',
                  'lang': 'python',
                  'readonly': False,
                  'width': '700px',
                  'height': '400px',
                  'soft_tabs': True,
                  'show_invisibles': False,
                  'fontsize': '14px',
                  'tabsize': 4,
                  'print_margin': True,
                  'highlight_active': True}

DEFAULT_ALLOWED_CONFIGURATION = {'enabled': True,
                                 'lang': [('python','Python',)],
                                 'theme': [('eclipse', 'Eclipse',),
                                           ('github', 'GitHub',),
                                           ('monokai', 'Monokai',),
                                           ('xcode', 'XCode',)],
                                 'fontsize': [('12px', 'Small',),
                                              ('14px', 'Medium',),
                                              ('16px', 'Large',)]}

class AceWidget(forms.Textarea):
    def __init__(self, config=None, customizable=None, *args, **kwargs):
        # Config when loading page
        config = config or {}
        self._readonly = bool(self._get_config('readonly', config))
        self._theme = self._get_config('theme', config)
        self._langage = self._get_config('lang', config)
        self._width = self._get_config('width', config)
        self._height = self._get_config('height', config)
        self._soft_tabs = bool(self._get_config('soft_tabs', config))
        self._show_invisibles = bool(self._get_config('show_invisibles', config))
        self._fontsize = str(self._get_config('fontsize', config))
        self._tabsize = int(self._get_config('tabsize', config))
        self._print_margin = bool(self._get_config('print_margin', config))
        self._highlight_active = bool(self._get_config('highlight_active', config))
        # What's allowed to be changed dynamically
        customizable = customizable or {}
        self._allow_modif = bool(self._get_allowed('enabled', customizable))
        if self._allow_modif is True:
            at_least_one = False
            # Lang
            self._allowed_lang = self._get_allowed('lang', customizable)
            at_least_one = at_least_one or len(self._allowed_lang) > 1
            # Theme
            self._allowed_theme = self._get_allowed('theme', customizable)
            at_least_one = at_least_one or len(self._allowed_theme) > 1
            # Font Size
            self._allowed_fontsize = self._get_allowed('fontsize', customizable)
            at_least_one = at_least_one or len(self._allowed_fontsize) > 1
            # If nothing to configure, disable allow_modif
            if at_least_one is False:
                self._allow_modif = False
        super(AceWidget, self).__init__(*args, **kwargs)

    @staticmethod
    def _get_config(label, local_config):
        llabel = str(label).lower()
        ulabel = 'ACE_{0}'.format(str(label).upper())
        if llabel in local_config:
            return local_config.pop(llabel)
        if hasattr(settings, ulabel):
            return getattr(settings, ulabel)
        return DEFAULT_CONFIG[llabel]

    @staticmethod
    def _get_allowed(label, local_config):
        llabel = str(label).lower()
        ulabel = 'ACE_MODIF_{0}'.format(str(label).upper())
        if llabel in local_config:
            return local_config.pop(llabel)
        if hasattr(settings, ulabel):
            return getattr(settings, ulabel)
        return DEFAULT_ALLOWED_CONFIGURATION[llabel]

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
               'code': force_text(value or ''),
               'width': self._width,
               'height': self._height,
               'default_theme': self._theme.lower(),
               'default_lang': self._langage.lower(),
               'read_only': self._bool_to_str(self._readonly),
               'soft_tabs': self._bool_to_str(self._soft_tabs),
               'show_invisibles': self._bool_to_str(self._show_invisibles),
               'fontsize': self._fontsize,
               'tabsize': self._tabsize,
               'print_margin': self._bool_to_str(self._print_margin),
               'highlight_active': self._bool_to_str(self._highlight_active),
               'allow_modif': self._allow_modif}
        if self._allow_modif is True:
            ctx['allowed_lang'] = self._allowed_lang
            print('ALLOWED:' , ctx['allowed_lang'])
            ctx['allowed_theme'] = self._allowed_theme
            ctx['allowed_fontsize'] = self._allowed_fontsize
               
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

    @staticmethod
    def _bool_to_str(value):
        return 'yes' if value else 'no' 
