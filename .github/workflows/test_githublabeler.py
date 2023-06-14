import githublabeler
import pytest
from datetime import datetime, timezone

FAKE_ID = 'fakeID'

activeDiscussionPosts = [{'id': FAKE_ID,
                          'createdAt': '2022-06-01T22:42:26Z',
                          'lastEditedAt': '3023-06-01T22:42:26Z',
                          'comments': {'nodes': [{'createdAt': '2022-06-01T22:42:26Z',
                                                  'updatedAt': '2022-06-01T22:42:26Z',
                                                  'replies': {'nodes': [{'createdAt': '2022-06-01T22:42:26Z',
                                                                         'updatedAt': '2022-06-01T22:42:26Z'}]}}]}}]

quietDiscussionPosts = [{'id': FAKE_ID,
                         'createdAt': '2022-06-01T22:42:26Z',
                         'lastEditedAt': '2022-06-01T22:42:26Z',
                         'comments': {'nodes': [{'createdAt': '2022-06-01T22:42:26Z',
                                                 'updatedAt': '2022-06-01T22:42:26Z',
                                                 'replies': {'nodes': [{'createdAt': '2022-06-01T22:42:26Z',
                                                                        'updatedAt': '2022-06-01T22:42:26Z'}]}}]}}]

newDiscussionPosts = [{'id': FAKE_ID,
                       'createdAt': '3022-06-01T22:42:26Z',
                       'lastEditedAt': '2022-06-01T22:42:26Z',
                       'comments': {'nodes': [{'createdAt': '2022-06-01T22:42:26Z',
                                               'updatedAt': '2022-06-01T22:42:26Z',
                                               'replies': {'nodes': [{'createdAt': '2022-06-01T22:42:26Z',
                                                                      'updatedAt': '2022-06-01T22:42:26Z'}]}}]}}]


def test_isActive():
    now = datetime.now(timezone.utc)
    for d in activeDiscussionPosts:
        assert githublabeler.isActive(d, now)

    for d in quietDiscussionPosts:
        assert githublabeler.isActive(d, now) == False


def test_getUpdates():
    now = datetime.now(timezone.utc)
    assert githublabeler.getUpdates(quietDiscussionPosts, now) == [{
        'id': FAKE_ID,
        'add': [
            githublabeler.QUIET_LABEL], 'remove': [
            githublabeler.NEW_LABEL, githublabeler.ACTIVE_LABEL]}]
    assert githublabeler.getUpdates(activeDiscussionPosts, now) == [{
        'id': FAKE_ID,
        'add': [
            githublabeler.ACTIVE_LABEL], 'remove': [
            githublabeler.NEW_LABEL, githublabeler.QUIET_LABEL]}]
    assert githublabeler.getUpdates(newDiscussionPosts, now) == [{
        'id': FAKE_ID,
        'add': [
            githublabeler.NEW_LABEL, githublabeler.ACTIVE_LABEL], 'remove': [
            githublabeler.QUIET_LABEL]}]
