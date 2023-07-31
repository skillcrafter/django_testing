from django.conf import settings
from django.test import TestCase

from django.urls import reverse

from notes.models import Note


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        Note.objects.bulk_create(
            Note(title=f'Новость {index}', text='Просто текст.')
            for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
        )

        class TestNotes(TestCase):
            @classmethod
            def setUpTestData(cls):
                cls.add_url = reverse('notes:add', args=(cls.note.slug,))
                cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
                cls.author = User.objects.create(username='Автор')
                cls.note = Note.objects.create(
                    title='Заголовок',
                    text='Текст заметки',
                    slug=SlUG,
                    author=cls.author,
                )
            def test_notes_list_for_different_users(self):
                """Проверка списка заметок."""
                clients = (
                    (self.author_client, True),
                    (self.user_client, False),
                )
                for client, value in clients:
                    with self.subTest(client=client):
                        object_list = client.get(URL.list).context[
                            'object_list']
                        self.assertTrue(
                            (self.note in object_list) is value,
                            msg=(
                                f'{client} не должен видеть заметки других '
                                f'пользователей в своем списке заметок.'
                            ),
                        )

            # def test_pages_contains_form(self):
            #     """Проверка формы."""
            #     for url in (URL.add, URL.edit):
            #         with self.subTest(url=url):
            #             self.assertIsInstance(
            #                 self.author_client.get(url).context['form'],
            #                 NoteForm,
            #                 msg=(
            #                     f'Проверьте, что форма редактирования передается на '
            #                     f'страницу {url}.'
            #                 ),
            #             )

            def test_authorized_client_has_form(self):
                for url in (self.add_url, self.edit_url):
                    with self.subTest(url=url):
                        self.client.force_login(self.author)
                        response = self.client.get(url)
                        self.assertIn('form', response.context['object_list'])