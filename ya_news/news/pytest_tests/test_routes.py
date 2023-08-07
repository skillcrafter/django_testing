import pytest

from django.urls import reverse
from http import HTTPStatus

from pytest_django.asserts import assertRedirects


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.mark.parametrize(
    'parametrized_client, expected_status, name, args',
    (
        (pytest.lazy_fixture('client'), HTTPStatus.OK,
         'news:home', ''),
        (pytest.lazy_fixture('client'), HTTPStatus.OK,
         'news:detail', pytest.lazy_fixture('news_id_for_args')),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK,
         'news:edit', pytest.lazy_fixture('comment_id_for_args')),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK,
         'news:delete', pytest.lazy_fixture('comment_id_for_args')),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND,
         'news:edit', pytest.lazy_fixture('comment_id_for_args')),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND,
         'news:delete', pytest.lazy_fixture('comment_id_for_args')),
        (pytest.lazy_fixture('client'), HTTPStatus.OK,
         'users:login', ''),
        (pytest.lazy_fixture('client'), HTTPStatus.OK,
         'users:logout', ''),
        (pytest.lazy_fixture('client'), HTTPStatus.OK,
         'users:signup', '')
    ),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, news, expected_status, args):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
        ('news:delete', pytest.lazy_fixture('comment_id_for_args')),
    )
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
