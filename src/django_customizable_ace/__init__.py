
__author__ = 'Pirheas'
__version__ = '0.1.0'


def ace_staticfiles_path():
    import os
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'static')
