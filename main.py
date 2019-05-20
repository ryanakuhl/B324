import re, requests, pyperclip
from bs4 import BeautifulSoup

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

three_to_four_list = {
                      'list-inline': 'list-inline-item',
                      'dropdown-menu': 'dropdown-item',
                      'navbar': 'nav-item',
                      'pagination': 'page-item',
                      }


def sanitize_html(all_text_in):
  all_text = all_text_in.replace('<b>', '<strong>').replace('</b>', '</strong>')
  all_text = all_text.replace('<i>', '<em>').replace('</i>', '</em>')
  all_text = BeautifulSoup(all_text, 'html.parser')
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
      for nested_link in kid.find_all('a'):
        if nested_link.has_attr('class'):
          nested_link['class'] = kid['class'] + ' ' + three_to_four_list.get(a).replace('item', 'link')
        else:
          nested_link['class'] = three_to_four_list.get(a).replace('item', 'link')
  soup.find(class_=a)['class'] = ''
  return str(soup).replace(' class=""', '')


changing_html = pyperclip.paste()
regexpHandler = re.findall('class="(.*?)"', changing_html)
list = []
for r in regexpHandler:
  for a in r.split(' '):
    if a not in list:
      list.append(a)
for class_to_change in list:
  if class_to_change in three_to_four_list:
    changing_html = list_items(class_to_change)
  elif class_to_change in three_to_four:
    changing_html = iter_dict(class_to_change)
sanitize_html(changing_html)
