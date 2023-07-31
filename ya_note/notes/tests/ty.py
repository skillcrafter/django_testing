# p._fields            # view the field names
# ('x', 'y')
#
# Color = namedtuple('Color', 'red green blue')
# Pixel = namedtuple('Pixel', Point._fields + Color._fields)
# Pixel(11, 22, 128, 255, 0)
# Pixel(x=11, y=22, red=128, green=255, blue=0)
from collections import namedtuple
from django.urls import reverse

SLUG = 'note-slug'

URL_NAME = namedtuple(
    'NAME',
    [
        'home',
        'add',
        'list',
        'detail',
        'edit',
        'delete',
        'success',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('notes:home'),
    reverse('notes:add'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
    reverse('notes:success'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)

print(URL.home)