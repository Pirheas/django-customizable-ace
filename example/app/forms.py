from django import forms
from django_customizable_ace.widgets import AceWidget

class MyCodeForm(forms.Form):

    @staticmethod
    def get_config():
        # Local default config for this type of form
        return {'readonly': False}

    @staticmethod
    def get_customizable():
        # Local customization for this type of form
        return {'lang': [('python', 'Python',), ('java', 'Java')]}

    code = forms.CharField(widget=AceWidget(config=get_config.__func__(),
                                            customizable=get_customizable.__func__()))
