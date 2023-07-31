# Импортируем класс HTTPStatus.
from http import HTTPStatus

# Импортируем функцию для определения модели пользователя.
from django.contrib.auth import get_user_model

from django.test import Client, TestCase
# Импортируем функцию reverse().
from django.urls import reverse

# Импортируем класс модели новостей.
# Импортируем класс комментария.
# from notes.models import Note
from notes.models import Note

# Получаем модель пользователя.
User = get_user_model()

SlUG = 'note-slug'

URL_HOME = reverse('notes:home', args=())
URL_LOGIN = reverse('users:login', args=())
URL_SIGNUP = reverse('users:signup', args=())
URL_LOGOUT = reverse('users:logout', args=())
URL_DETAIL = reverse('notes:detail', args=(SlUG,))
URL_EDIT = reverse('notes:edit', args=(SlUG,))
URL_DELETE = reverse('notes:delete', args=(SlUG,))
URL_ADD = reverse('notes:add', args=())
URL_LIST = reverse('notes:list', args=())
URL_SUCSESS = reverse('notes:success', args=())
URL_LIST = reverse('notes:list', args=())


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = User.objects.create(username='Пользователь')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=SlUG,
            author=cls.author,
        )

    def test_pages_availability(self):
        # Создаём набор тестовых данных - кортеж кортежей.
        # Каждый вложенный кортеж содержит два элемента:
        # имя пути и позиционные аргументы для функции reverse().
        urls = (
            (URL_HOME, self.client, HTTPStatus.OK),
            (URL_LOGIN, self.client, HTTPStatus.OK),
            (URL_LOGOUT, self.client, HTTPStatus.OK),
            (URL_SIGNUP, self.client, HTTPStatus.OK),
            (URL_DETAIL, self.author_client, HTTPStatus.OK),
            (URL_EDIT, self.author_client, HTTPStatus.OK),
            (URL_DELETE, self.author_client, HTTPStatus.OK),
            (URL_ADD, self.user_client, HTTPStatus.OK),
            (URL_LIST, self.user_client, HTTPStatus.OK),
            (URL_SUCSESS, self.user_client, HTTPStatus.OK),
            (URL_DETAIL, self.user_client, HTTPStatus.NOT_FOUND),
            (URL_EDIT, self.user_client, HTTPStatus.NOT_FOUND),
            (URL_DELETE, self.user_client, HTTPStatus.NOT_FOUND)
        )
        # Итерируемся по внешнему кортежу
        # и распаковываем содержимое вложенных кортежей:
        for url, client, expected_status in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    response.status_code,
                    expected_status)

    # def test_redirects(self):
    #     """Проверка редиректа для неавторизованного пользователя."""
    #     urls = (
    #         URL.list,
    #         URL.add,
    #         URL.success,
    #         URL.detail,
    #         URL.edit,
    #         URL.delete,
    #     )
    #     for url in urls:
    #         with self.subTest(url=url):
    #             redirect_url = f'{URL.login}?next={url}'
    #             self.assertRedirects(
    #                 self.client.get(url),
    #                 redirect_url,
    #                 msg_prefix=(
    #                     f'Убедитесь, что у неавторизованного '
    #                     f'пользователя нет доступа к странице {url}.'
    #                 ),
    #             )

    def test_redirect_for_anonymous_client(self):
        # Сохраняем адрес страницы логина:
        login_url = reverse('users:login')
        # В цикле перебираем имена страниц, с которых ожидаем редирект:
        for url in (URL_EDIT, URL_DELETE, URL_ADD, URL_SUCSESS, URL_DETAIL, URL_LIST):
            with self.subTest(url=url):
                # Получаем адрес страницы редактирования или удаления комментария:
                # url = reverse(name, args=(self.note.slug,))
                # Получаем ожидаемый адрес страницы логина,
                # на который будет перенаправлен пользователь.
                # Учитываем, что в адресе будет параметр next, в котором передаётся
                # адрес страницы, с которой пользователь был переадресован.
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                # Проверяем, что редирект приведёт именно на указанную ссылку.
                self.assertRedirects(response, redirect_url)
