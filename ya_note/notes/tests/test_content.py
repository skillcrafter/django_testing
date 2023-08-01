from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='testUser')
        cls.other = User.objects.create(username='otherUser')
        cls.note_owner = Note.objects.create(
            title='Заголовок1', text='Текст1',
            slug='slug1', author=cls.author,)
        cls.note_noname_user = Note.objects.create(
            title='Заголовок2', text='Текст2',
            slug='slug2', author=cls.other,)

    def test_list_context(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note_owner, object_list)

    def test_different_list(self):
        users_notes = (
            (self.author, self.note_noname_user),
            (self.other, self.note_owner),)

        for user, note in users_notes:
            self.client.force_login(user)
            response = self.client.get(self.NOTES_URL)
            object_list = response.context['object_list']
            self.assertNotIn(note, object_list)

    def test_form_context(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note_owner.slug,)),)
        self.client.force_login(self.author)

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
            self.assertIn('form', response.context)
