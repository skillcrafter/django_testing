from http import HTTPStatus
import pytest

from django.urls import reverse

from pytest_django.asserts import assertRedirects


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
            ('news:home', None),
            ('news:detail', pytest.lazy_fixture('news_id_for_args')),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


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


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    )
)
@pytest.mark.parametrize(
    'name, args',
    (
            ('news:edit', pytest.lazy_fixture('comment_id_for_args')),
            ('news:delete', pytest.lazy_fixture('comment_id_for_args')),
    )
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, name, args, expected_status):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
