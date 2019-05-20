import time, re
import easygui
import requests
import pyperclip
import xlsxwriter
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetimerange import DateTimeRange

class_regrex = re.compile(r'^class="[\d\w\D\W\s]"')

three_to_four = {'Bootstrap 3x': 'Bootstrap 4',
                 'col-\d-offset-\d': 'col offset-\d',
                 'col-\d-push-\d': 'col order-\d',
                 'col-\d-pull-\d': 'col order-\d',
                 'panel': 'card',
                 'panel-heading': 'card-header',
                 'panel-title': 'card-title',
                 'panel-body': 'card-body',
                 'panel-footer': 'card-footer',
                 'panel-primary': 'card bg-primarytext-white',
                 'panel-success': 'card bg-successtext-white',
                 'panel-info': 'cardtext-whitebg-info',
                 'panel-warning': 'card bg-warning',
                 'panel-danger': 'card bg-danger text-white',
                 'well': 'cardcard-body',
                 'thumbnail': 'cardcard-body',
                 'navbar-right': 'ml-auto',
                 'navbar-btn': 'nav-item',
                 'navbar-fixed-top': 'fixed-top',
                 'nav-stacked': 'flex-column',
                 'btn-default': 'btn-secondary',
                 'img-responsive': 'img-fluid',
                 'img-circle': 'rounded-circle',
                 'img-rounded': 'rounded',
                 'form-horizontal': '(removed)',
                 'radio': 'form-check',
                 'checkbox': 'form-check',
                 'input-lg': 'form-control-lg',
                 'input-sm': 'form-control-sm',
                 'control-label': 'col-form-label',
                 'table-condensed': 'table-sm',
                 'item': 'carousel-item',
                 'help-block': 'form-text',
                 'pull-right': 'float-right',
                 'pull-left': 'float-left',
                 'center-block': 'mx-auto d-block',
                 'hidden-xs': 'd-none',
                 'hidden-sm': 'd-sm-none',
                 'hidden-md': 'd-md-none',
                 'hidden-lg': 'd-lg-none',
                 'visible-xs': 'd-block d-sm-none',
                 'visible-sm': 'd-none d-sm-blockd-md-none',
                 'visible-md': 'd-none d-md-blockd-lg-none',
                 'visible-lg': 'd-none d-lg-blockd-xl-none',
                 'label': 'badge',
                 'badge': 'badge badge-pill'
                 }
"""
???
'list-inline > li': 'list-inline-item',
'dropdown-menu > li': 'dropdown-item',
'nav navbar > li': 'nav-item',
'nav navbar > li > a': 'nav-link',
'pagination > li': 'page-item',
'pagination > li > a': 'page-link',
"""

def sanitize_HTML(all_text):
    all_text = all_text.replace('<b>', '<strong>')
    all_text = all_text.replace('</b>', '</strong>')
    all_text = all_text.replace('<i>', '<em>')
    all_text = all_text.replace('</i>', '</em>')
    all_text = all_text.replace('<b></b>', '')
    all_text = all_text.replace('<span></span>', '')
    all_text = all_text.replace('<div></div>', '')
    all_text = all_text.replace('<ul></ul>', '')
    all_text = all_text.replace('<li></li>', '')
    all_text = BeautifulSoup(all_text, 'html.parser')
    all_text = all_text.prettify()
    pyperclip.copy(all_text)
    return all_text


def iter_dict(a):
    aa = changing_html
    for item in three_to_four:
        if re.match(re.compile(item), a):
            aa = changing_html.replace(a, three_to_four.get(item))
    return aa


changing_html = pyperclip.paste()
print('dirty ', changing_html)
regexpHandler = re.findall('class="(.*?)"', changing_html)
for class_to_change in regexpHandler:
    changing_html = iter_dict(class_to_change)
sanitize_HTML(changing_html)
