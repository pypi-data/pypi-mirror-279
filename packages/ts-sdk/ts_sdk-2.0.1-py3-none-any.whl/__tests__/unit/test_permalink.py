import pytest

from ts_sdk.task.__util_permalink import (
    remove_trailing_slash,
    ensure_object_type,
    ObjectType,
    select_short_name,
    get_permalink,
)


TEST_UUID = "b7b24a5b-16eb-483f-86cc-93777f016c34"


def test_remove_trailing_slash():
    assert (
        remove_trailing_slash("http://api.test.tetrascience.com")
        == "http://api.test.tetrascience.com"
    )
    assert (
        remove_trailing_slash("http://api.test.tetrascience.com/")
        == "http://api.test.tetrascience.com"
    )
    assert (
        remove_trailing_slash("http://api.test.tetrascience.com//")
        == "http://api.test.tetrascience.com"
    )


def test_object_type_to_object_type():
    assert ensure_object_type(ObjectType.FILE) == ObjectType.FILE
    assert ensure_object_type(ObjectType._DEBUG) == ObjectType._DEBUG


def test_string_to_object_type_success():
    assert ensure_object_type("file") == ObjectType.FILE
    assert ensure_object_type("_debug") == ObjectType._DEBUG


def test_number_to_object_type():
    with pytest.raises(ValueError):
        ensure_object_type(10)


def test_string_to_object_type_failure():
    with pytest.raises(ValueError):
        ensure_object_type("not file")


def test_select_short_name_success():
    assert select_short_name(ObjectType.FILE) == "fi"


def test_get_permalink_uuid_is_string():
    with pytest.raises(ValueError):
        get_permalink("http://api.test.tetrascience.com", ObjectType.FILE, 10)


def test_get_permalink_platform_url_is_string():
    with pytest.raises(ValueError):
        get_permalink(10, ObjectType.FILE, TEST_UUID)


def test_get_permalink_object_type_must_be_valid():
    with pytest.raises(NotImplementedError):
        get_permalink("http://api.test.tetrascience.com", "_debug", TEST_UUID)
    with pytest.raises(ValueError):
        get_permalink("http://api.test.tetrascience.com", "something else", TEST_UUID)


def test_get_permalink_success_with_object_type():
    result = get_permalink(
        "http://api.test.tetrascience.com", ObjectType.FILE, TEST_UUID
    )
    assert result == f"http://api.test.tetrascience.com/o/fi/{TEST_UUID}"


def test_get_permalink_success_with_string():
    result = get_permalink(
        "http://api.test.tetrascience.com/",
        "file",
        TEST_UUID,
    )
    assert result == f"http://api.test.tetrascience.com/o/fi/{TEST_UUID}"


def test_select_short_name_failure():
    with pytest.raises(NotImplementedError):
        select_short_name(ObjectType._DEBUG)
