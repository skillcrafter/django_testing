import pytest

from django.urls import reverse
from http import HTTPStatus
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
class TestNews:
    URL_HOMEPAGE = reverse('news:home')

    def test_news_count(self, client, news_objects):
        response = client.get(self.URL_HOMEPAGE)
        object_list = response.context['object_list']
        news_count = len(object_list)
        assert news_count == NEWS_COUNT_ON_HOME_PAGE

    def test_news_order(self, client, news_objects):
        response = client.get(self.URL_HOMEPAGE)
        object_list = response.context['object_list']
        all_dates = [news.date for news in object_list]
        sorted_dates = sorted(all_dates, reverse=True)
        assert all_dates == sorted_dates


@pytest.mark.usefixtures('news')
@pytest.mark.django_db
class TestCommentsContent:
    DETAIL_PAGE_URL = 'news:detail'

    def test_comment_order(self, client, comments, news_pk):
        url = reverse(self.DETAIL_PAGE_URL, args=news_pk)
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        comments = list(response.context['object'].comment_set.all())
        sorted_comments = sorted(comments, key=lambda x: x.created)
        assert comments == sorted_comments


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_on_page',
    (
            (pytest.lazy_fixture('author_client'), True),
            (pytest.lazy_fixture('client'), False),
    )
)
def test_pages_data_for_different_users(
        parametrized_client, form_on_page, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    response = parametrized_client.get(url)
    form_in_context = 'form' in response.context
    assert form_in_context is form_on_page
    assert response.status_code == HTTPStatus.OK
