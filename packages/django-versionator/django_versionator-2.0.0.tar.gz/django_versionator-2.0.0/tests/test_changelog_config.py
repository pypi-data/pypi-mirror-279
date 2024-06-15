from unittest.mock import Mock, patch

import pytest
from data_fetcher.global_request_context import GlobalRequest
from freezegun import freeze_time
from pytest_django.asserts import assertInHTML

from sample_app.data_factories import AuthorFactory, BookFactory
from sample_app.fetchers import BookNameFetcher
from sample_app.models import Author, Book, Tag
from versionator.changelog.changelog import (
    Changelog,
    ChangelogConfig,
    SingleRecordChangelogConfig,
)


def modify_record(record, **kwargs):
    record.reset_version_attrs()
    for k, v in kwargs.items():
        setattr(record, k, v)
    record.save()
    record.reset_version_attrs()


def create_data():
    with freeze_time("2000-01-01"):
        a1 = AuthorFactory()
        a2 = AuthorFactory()

        b1 = BookFactory(author=a1)
        b2 = BookFactory(author=a2)

    with freeze_time("2001-01-01"):
        modify_record(a1, first_name="a1v2")
        modify_record(a2, first_name="a2v2")
        modify_record(b1, title="b1v2")
        modify_record(b2, title="b1v2")

    with freeze_time("2002-01-01"):
        modify_record(a1, last_name="a1v3")
        modify_record(a2, last_name="a2v3")
        modify_record(b1, title="b1v3")
        modify_record(b2, title="b2v3")

    # each record should have 3 entries,  v1 (create), v2, v3

    return a1, a2, b1, b2


def test_model_filter():
    a1, a2, *_ = create_data()
    config = ChangelogConfig(
        models=[Author],
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 6
    entries = changelog.get_entries(1)

    assert entries[0].eternal == a1
    assert entries[1].eternal == a2
    assert entries[2].eternal == a1
    assert entries[3].eternal == a2


def test_auhorproperty_on_authorless_model():
    create_data()
    config = ChangelogConfig(
        models=[Author],
        page_size=2,
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 6
    entries = changelog.get_entries(1)
    assert entries[0].author is None


def test_page_size():
    create_data()
    config = ChangelogConfig(
        models=[Author, Book],
        page_size=2,
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 12
    entries = changelog.get_entries(1)
    assert len(entries) == 2
    assert changelog.get_page_count() == 6


def test_start_date():
    create_data()
    config = ChangelogConfig(
        models=[Author, Book],
        start_date="2000-12-01",
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 8
    entries = changelog.get_entries(1)

    for entry in entries:
        assert entry.right_version.timestamp.date().isoformat() >= "2001-01-01"


def test_end_date():
    create_data()
    config = ChangelogConfig(
        models=[Author, Book],
        end_date="2000-12-01",
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 4
    entries = changelog.get_entries(1)

    for entry in entries:
        assert entry.right_version.timestamp.date().isoformat() == "2000-01-01"


def test_start_and_end_date():
    create_data()
    config = ChangelogConfig(
        models=[Author, Book],
        start_date="2000-12-01",
        end_date="2001-12-01",
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 4
    entries = changelog.get_entries(1)

    for entry in entries:
        assert entry.right_version.timestamp.date().isoformat() >= "2001-01-01"


def test_with_specified_fields():
    create_data()
    config = ChangelogConfig(
        models=[Author, Book],
        fields_by_model={
            Author: ["first_name"],
        },
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 2
    entries = changelog.get_entries(1)

    for entry in entries:
        assert len(entry.diffs) == 1
        assert entry.diffs[0].field.name == "first_name"


def test_with_diffable_fields():
    create_data()

    class CustomChangelogConfig(ChangelogConfig):
        def get_diffable_fields_for_model(self, model):
            diffable = super().get_diffable_fields_for_model(model)
            return [field for field in diffable if field.name != "first_name"]

    config = CustomChangelogConfig(
        models=[Author, Book],
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 12
    entries = changelog.get_entries(1)

    for entry in entries:
        for diff in entry.diffs:
            if diff.field:
                assert diff.field.name != "first_name"


def test_with_filtering():
    a1, _a2, b1, _b2 = create_data()
    create_data()

    class AuthorScopedChangelog(ChangelogConfig):
        def get_base_version_queryset_for_single_model(self, live_model):
            if live_model is Author:
                return live_model._history_class.objects.filter(eternal=a1)

            elif live_model is Book:
                return live_model._history_class.objects.filter(author=a1)

    config = AuthorScopedChangelog(
        models=[Author, Book],
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 6
    entries = changelog.get_entries(1)
    for entry in entries:
        assert entry.eternal in (a1, b1)


def single_record_changelog():
    a1, *_ = create_data()
    create_data()

    config = SingleRecordChangelogConfig(
        record=a1,
    )
    changelog = Changelog(config)
    assert changelog.get_entry_count() == 3

    entries = changelog.get_entries(1)
    assert len(entries) == 3
    for entry in entries:
        assert entry.eternal == a1


def test_creates_only():
    create_data()

    config = ChangelogConfig(
        create_mode=ChangelogConfig.ONLY_CREATES,
        models=[Author, Book],
    )
    changelog = Changelog(config)

    assert changelog.get_entry_count() == 4
    entries = changelog.get_entries(1)
    for entry in entries:
        assert entry.diffs[0].__class__.__name__ == "CreateDiff"


def test_exclude_creates():
    create_data()

    config = ChangelogConfig(
        create_mode=ChangelogConfig.EXCLUDE_CREATES,
        models=[Author, Book],
    )
    changelog = Changelog(config)

    assert changelog.get_entry_count() == 8
    entries = changelog.get_entries(1)
    for entry in entries:
        for diff in entry.diffs:
            assert diff.field is not None
