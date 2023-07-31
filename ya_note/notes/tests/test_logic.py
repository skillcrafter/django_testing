from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify
from django.contrib.auth import get_user_model

from django.test import Client, TestCase

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class CheckData(TestCase):
    def check_data(self, field_data):
        """Сравнение данных заметки в БД с данными отправленными в форме."""
        note = Note.objects.get()
        db_data = (note.title, note.text, note.slug, note.author)
        for name, sent_value, db_value in zip(
            FIELD_NAMES, field_data, db_data
        ):
            with self.subTest(sent_value=sent_value, db_value=db_value):
                self.assertEqual(
                    sent_value,
                    db_value,
                    msg=(
                        f'В базу данных, в поле {name} было записано: '
                        f'{db_value}. Убедитесь что передаете верные данные '
                        f'- {sent_value}.'
                    ),
                )

    def equal(self, expected_count):
        """Сравнение кол-ва заметок в БД."""
        notes_count = Note.objects.count()
        self.assertEqual(
            expected_count,
            notes_count,
            msg=(
                f'Кол-во заметок в БД {notes_count} не соответствует '
                f'ожидаемому {expected_count}.'
            ),
        )

class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        #cls.note = Note.objects.create(title='Заголовок', text='Текст заметки', slug='new-slug', author=cls.author)
        # Адрес страницы с новостью.

        # Создаём пользователя и клиент, логинимся в клиенте.
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(title='Заголовок', text='Текст заметки', slug='new-slug', author=cls.author)
        cls.url = reverse('notes:add', args=())
        # Данные для POST-запроса при создании комментария.
        cls.form_data = {'text': cls.TEXT}

        @classmethod
        def setUpTestData(cls):
            cls.author = USER_MODEL.objects.create(username=AUTHOR)
            cls.author_client = Client()
            cls.author_client.force_login(cls.author)
            cls.form_data = dict(zip(FIELD_NAMES, FIELD_DATA))
            cls.field_data = (*FIELD_DATA, cls.author)

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        note_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(note_count, 0)

        url = reverse('notes:add')
        # Через анонимный клиент пытаемся создать заметку:
        response = client.post(url, data=form_data)
        login_url = reverse('users:login')
        expected_url = f'{login_url}?next={url}'
        # Проверяем, что произошла переадресация на страницу логина:
        assertRedirects(response, expected_url)
