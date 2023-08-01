from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.other = User.objects.create(username='Noname')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст',
            slug='slug', author=cls.author, )

    def test_is_page_availible_for_owner(self):
        urls = ('notes:list', 'notes:success', 'notes:add',)
        users_statuses = ((self.author, HTTPStatus.OK),)

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, )
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_is_detail_page_availible_for_editing_deleting(self):
        urls = ('notes:detail', 'notes:edit', 'notes:delete',)
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.other, HTTPStatus.NOT_FOUND),)

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_is_page_redirected_for_noname_user(self):
        urls = ('notes:list', 'notes:success', 'notes:add',)
        urls_slug = ('notes:detail', 'notes:edit', 'notes:delete',)
        login_link = reverse('users:login')

        for name in urls:
            with self.subTest(name=name):
                url = reverse(name, )
                redirect_url = f'{login_link}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
        for name in urls_slug:
            with self.subTest(name=name):
                url = reverse(name, args=(self.note.slug,))
                redirect_url = f'{login_link}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_is_page_availible_for_noname_user(self):
        urls = (('users:login', None),
                ('users:logout', None),
                ('users:signup', None),
                ('notes:home', None),)

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
