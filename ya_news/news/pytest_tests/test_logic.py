from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_noname_user_cant_create_comment(
        client, form_data, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_comment_creation(author_client, author, form_data, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    add_comment = Comment.objects.get()
    assert add_comment.text == form_data['text']
    assert add_comment.author == author


def test_user_cant_use_bad_words(author_client, form_data, news_id_for_args):
    form_data['text'] = f'Текст, {BAD_WORDS[0]}, текст, вторая часть'
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'text', WARNING)
    assert Comment.objects.count() == 0


def test_the_author_granded_to_edit_comment(
        author_client, form_data,
        comment, news_id_for_args,
        comment_id_for_args):
    news_url = reverse('news:detail', args=news_id_for_args)
    url_to_comments = news_url + '#comments'
    edit_url = reverse('news:edit', args=comment_id_for_args)
    response = author_client.post(edit_url, form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_noname_user_cant_edit_comment(admin_client,
                                       form_data,
                                       comment,
                                       comment_id_for_args):
    edit_url = reverse('news:edit', args=comment_id_for_args)
    response = admin_client.post(edit_url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(
        author_client, news_id_for_args, comment_id_for_args):
    news_url = reverse('news:detail', args=news_id_for_args)
    url_to_comments = news_url + '#comments'
    delete_url = reverse('news:delete', args=comment_id_for_args)
    response = author_client.delete(delete_url)
    # print(response)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
        admin_client, comment_id_for_args):
    url = reverse('news:delete', args=comment_id_for_args)
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
