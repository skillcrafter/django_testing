from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestAvailability(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.author,
        )

    def test_pages_availability_for_everyone(self):
        urls = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_users(self):
        for name, args, client, status in (
                ('notes:edit', (self.note.slug,),
                 self.author, HTTPStatus.OK
                 ),
                ('notes:delete', (self.note.slug,),
                 self.author, HTTPStatus.OK
                 ),
                ('notes:detail', (self.note.slug,),
                 self.author, HTTPStatus.OK
                 ),
                ('notes:edit', (self.note.slug,),
                 self.reader, HTTPStatus.NOT_FOUND
                 ),
                ('notes:delete', (self.note.slug,),
                 self.reader, HTTPStatus.NOT_FOUND
                 ),
                ('notes:detail', (self.note.slug,),
                 self.reader, HTTPStatus.NOT_FOUND
                 ),
                ('notes:add', None,
                 self.reader, HTTPStatus.OK
                 ),
                ('notes:success', None,
                 self.reader, HTTPStatus.OK
                 ),
                ('notes:list', None,
                 self.reader, HTTPStatus.OK
                 ),
        ):
            self.client.force_login(client)
            with self.subTest(user=client, name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name, args in (
                ('notes:list', None),
                ('notes:success', None),
                ('notes:delete', (self.note.slug,)),
                ('notes:add', None),
                ('notes:edit', (self.note.slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
