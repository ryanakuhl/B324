import re, requests, pyperclip
from bs4 import BeautifulSoup

three_to_four =  {'Bootstrap 3.x': 'Bootstrap 4',
                  'badge': 'badge badge-pill',
                  'btn-default': 'btn-secondary',
                  'center-block': 'mx-auto d-block',
                  'checkbox': 'form-check',
                  'col-\d-offset-\d': 'col offset-\d',
                  'col-\d-pull-\d': 'col order-\d',
                  'col-\d-push-\d': 'col order-\d',
                  'control-label': 'col-form-label',
                  'form-horizontal': '(removed)',
                  'help-block': 'form-text',
                  'hidden-desktop': 'd-lg-none',
                  'hidden-lg': 'd-lg-none',
                  'hidden-md': 'd-md-none',
                  'hidden-phone': 'd-sm-none',
                  'hidden-sm': 'd-sm-none',
                  'hidden-tablet': 'd-md-none',
                  'hidden-xs': 'd-none',
                  'img-circle': 'rounded-circle',
                  'img-responsive': 'img-fluid',
                  'img-rounded': 'rounded',
                  'input-lg': 'form-control-lg',
                  'input-sm': 'form-control-sm',
                  'item': 'carousel-item',
                  'label': 'badge',
                  'navbar-btn': 'nav-item',
                  'navbar-fixed-top': 'fixed-top',
                  'navbar-right': 'ml-auto',
                  'nav-stacked': 'flex-column',
                  'panel': 'card',
                  'panel-body': 'card-body',
                  'panel-danger': 'card bg-danger text-white',
                  'panel-footer': 'card-footer',
                  'panel-heading': 'card-header',
                  'panel-info': 'card text-white bg-info',
                  'panel-primary': 'card bg-primary text-white',
                  'panel-success': 'card bg-success text-white',
                  'panel-title': 'card-title',
                  'panel-warning': 'card bg-warning',
                  'pull-left': 'float-left',
                  'pull-right': 'float-right',
                  'radio': 'form-check',
                  'table-condensed': 'table-sm',
                  'thumbnail': 'card card-body',
                  'visible-desktop': 'd-none d-lg-block d-xl-none',
                  'visible-lg': 'd-none d-lg-block d-xl-none',
                  'visible-md': 'd-none d-md-block d-lg-none',
                  'visible-phone': 'd-none d-sm-block d-md-none',
                  'visible-sm': 'd-none d-sm-block d-md-none',
                  'visible-tablet': 'd-none d-md-block d-lg-none',
                  'visible-xs': 'd-block d-sm-none',
                  'well': 'card card-body'}

three_to_four_list = {
                      'list-inline': 'list-inline-item',
                      'dropdown-menu': 'dropdown-item',
                      'navbar': 'nav-item',
                      'pagination': 'page-item',
                      }

tag_dict = {'applet': 'object',
            'b': 'strong',
            'i': 'em',
            'dir': 'ul',
            'menu': 'ul',
            'center': 'div',
            'isindex': 'form'
            }


def sanitize_html(all_text):
    all_text = BeautifulSoup(all_text, 'html.parser')
    for tag in all_text.find_all():
      if tag.name in tag_dict:
        tag.name = tag_dict.get(tag.name)
    empty_tags = all_text.findAll(lambda tag: not tag.contents)
    [empty_tag.extract() for empty_tag in empty_tags]
    pyperclip.copy(all_text.prettify())


def iter_dict(a):
    local_changing_html = changing_html
    for item in three_to_four:
      if re.match(re.compile(item), a):
        local_changing_html = changing_html.replace(a, three_to_four.get(item))
    return local_changing_html


def list_items(a):
    soup = BeautifulSoup(changing_html, 'html.parser')
    for kid in soup.find(class_=a).children:
        if kid.name == 'li':
          if kid.has_attr('class'):
            kid['class'] = kid['class'] + ' ' + three_to_four_list.get(a)
          else:
            kid['class'] = three_to_four_list.get(a)
        if a == 'pagination ' or 'navbar':
            for nested_link in kid.find_all('a'):
                if nested_link.has_attr('class'):
                    nested_link['class'] = kid['class'] + ' ' + three_to_four_list.get(a).replace('item', 'link')
                else:
                    nested_link['class'] = three_to_four_list.get(a).replace('item', 'link')
    soup.find(class_=a)['class'] = ''
    return str(soup).replace(' class=""', '')


changing_html = pyperclip.paste()
regexpHandler = re.findall('class="(.*?)"', changing_html)
class_list = []
for r in regexpHandler:
    class_list += [a for a in r.split(' ') if a not in class_list]
for class_to_change in class_list:
    if class_to_change in three_to_four_list:
        changing_html = list_items(class_to_change)
    elif class_to_change in three_to_four:
        changing_html = iter_dict(class_to_change)
sanitize_html(changing_html)
