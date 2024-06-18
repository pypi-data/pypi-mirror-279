import json
import os
from unittest.mock import MagicMock, patch

import pytest
from tenacity import RetryError, wait_none

from ts_sdk.task.__util_adapters.communication_format import (
    COMMUNICATION_FORMAT_ENV_KEY,
    CommunicationFormat,
)
from ts_sdk.task.__util_fileinfo import (
    add_labels,
    get_labels,
    delete_labels,
    get_file_pointer,
    pipeline_history_from_input_file_meta,
    __RETRY_COUNT,
)

org_slug = "org_slug"
pipeline_id_0 = "pipeline_id_0"
pipeline_id_1 = "pipeline_id_1"
file_id = "file_id"

dummy_context_data = {
    "type": "s3",
    "bucket": "bucket",
    "fileKey": "some/fileKey",
    "fileId": "11111111-eeee-4444-bbbb-222222222222",
    "orgSlug": org_slug,
    "pipelineId": pipeline_id_1,
    "inputFile": {"meta": {"pipelineHistory": pipeline_id_0}},
}

add_label_args = [
    dummy_context_data,
    file_id,
    [{"name": "label1", "value": "label-value-1"}],
]
get_label_args = [dummy_context_data, file_id]
delete_label_empty_args = [dummy_context_data, file_id, []]
delete_label_args = [dummy_context_data, file_id, ["label_id"]]


@pytest.fixture(scope="session", autouse=True)
def before_all(request):
    for function in [add_labels, get_labels, delete_labels, get_file_pointer]:
        function.retry.wait = wait_none()


def test_format_unsupported():
    os.environ.update({COMMUNICATION_FORMAT_ENV_KEY: "unknown"})

    with pytest.raises(NotImplementedError):
        add_labels(*add_label_args)

    with pytest.raises(NotImplementedError):
        get_labels(*get_label_args)

    with pytest.raises(NotImplementedError):
        delete_labels(*delete_label_empty_args)

    with pytest.raises(NotImplementedError):
        delete_labels(*delete_label_args)

    with pytest.raises(NotImplementedError):
        get_file_pointer(dummy_context_data, "11111111-eeee-4444-bbbb-222222222222")


def __test_file_info_adapter(
    request_mock,
    endpoint,
    endpoint_env_key,
    path,
    communication_format,
    callback,
):
    os.environ.update(
        {
            endpoint_env_key: endpoint,
            COMMUNICATION_FORMAT_ENV_KEY: communication_format.value,
        }
    )

    request_response_mock = MagicMock()
    request_response_mock.status_code = 200
    request_response_mock.text = "{}"
    request_mock.return_value = request_response_mock

    callback()

    args, kwargs = request_mock.call_args
    url: str = args[0]
    assert url.startswith(endpoint + path)

    request_mock.reset_mock()
    request_response_mock.status_code = 404
    request_mock.return_value = request_response_mock

    with pytest.raises(RetryError):
        callback()
    assert request_mock.call_count == __RETRY_COUNT


@patch("requests.post")
def test_add_labels_v0(post_mocker):
    return __test_file_info_adapter(
        post_mocker,
        "http://fileinfo.local",
        "FILEINFO_ENDPOINT",
        f"/internal/{org_slug}/files/{file_id}/labels",
        CommunicationFormat.V0,
        lambda: add_labels(*add_label_args),
    )


@patch("requests.post")
def test_add_labels_v1(post_mocker):
    return __test_file_info_adapter(
        post_mocker,
        "https://localhost:443",
        "KERNEL_ENDPOINT",
        f"/api/v1/fileinfo/files/{file_id}/labels",
        CommunicationFormat.V1,
        lambda: add_labels(*add_label_args),
    )


@patch("requests.get")
def test_get_labels_v0(get_mocker):
    return __test_file_info_adapter(
        get_mocker,
        "http://fileinfo.local",
        "FILEINFO_ENDPOINT",
        f"/internal/{org_slug}/files/{file_id}/labels",
        CommunicationFormat.V0,
        lambda: get_labels(*get_label_args),
    )


@patch("requests.get")
def test_get_labels_v1(get_mocker):
    return __test_file_info_adapter(
        get_mocker,
        "https://localhost:443",
        "KERNEL_ENDPOINT",
        f"/api/v1/fileinfo/files/{file_id}/labels",
        CommunicationFormat.V1,
        lambda: get_labels(*get_label_args),
    )


@patch("requests.delete")
def test_delete_empty_labels_v0(delete_mocker):
    return __test_file_info_adapter(
        delete_mocker,
        "http://fileinfo.local",
        "FILEINFO_ENDPOINT",
        f"/internal/{org_slug}/files/{file_id}/labels",
        CommunicationFormat.V0,
        lambda: delete_labels(*delete_label_empty_args),
    )


@patch("requests.delete")
def test_delete_empty_labels_v1(delete_mocker):
    return __test_file_info_adapter(
        delete_mocker,
        "https://localhost:443",
        "KERNEL_ENDPOINT",
        f"/api/v1/fileinfo/files/{file_id}/labels",
        CommunicationFormat.V1,
        lambda: delete_labels(*delete_label_empty_args),
    )


@patch("requests.delete")
def test_delete_labels_v0(delete_mocker):
    return __test_file_info_adapter(
        delete_mocker,
        "http://fileinfo.local",
        "FILEINFO_ENDPOINT",
        f"/internal/{org_slug}/files/{file_id}/labels",
        CommunicationFormat.V0,
        lambda: delete_labels(*delete_label_args),
    )


@patch("requests.delete")
def test_delete_labels_v1(delete_mocker):
    return __test_file_info_adapter(
        delete_mocker,
        "https://localhost:443",
        "KERNEL_ENDPOINT",
        f"/api/v1/fileinfo/files/{file_id}/labels",
        CommunicationFormat.V1,
        lambda: delete_labels(*delete_label_args),
    )


def test_get_file_pointer_v0():
    os.environ.update(
        {
            COMMUNICATION_FORMAT_ENV_KEY: CommunicationFormat.V0.value,
        }
    )
    with pytest.raises(NotImplementedError):
        get_file_pointer(dummy_context_data, "11111111-eeee-4444-bbbb-333333333333")


@patch("ts_sdk.task.__util_ts_api.get")
def test_get_file_pointer_v1(get_mock):
    get_response_mock = MagicMock()
    get_response_mock.status_code = 200
    get_response_mock.text = json.dumps(
        {
            "file": {"bucket": "a-bucket", "path": "a-path", "version": "a-version"},
            "meta": {},
        }
    )
    get_mock.return_value = get_response_mock

    result = get_file_pointer(
        dummy_context_data, "11111111-eeee-4444-bbbb-333333333333"
    )

    args, kwargs = get_mock.call_args
    path: str = args[0]
    assert path == "/v1/fileinfo/file/11111111-eeee-4444-bbbb-333333333333"

    assert result == {
        "type": "s3file",
        "fileId": "11111111-eeee-4444-bbbb-333333333333",
        "bucket": "a-bucket",
        "fileKey": "a-path",
        "version": "a-version",
    }

    get_mock.reset_mock()
    get_response_mock.status_code = 404
    get_mock.return_value = get_response_mock

    with pytest.raises(RetryError):
        get_file_pointer(dummy_context_data, "11111111-eeee-4444-bbbb-333333333333")
    assert get_mock.call_count == __RETRY_COUNT

    get_mock.reset_mock()
    get_response_mock.status_code = 500
    get_mock.return_value = get_response_mock

    with pytest.raises(Exception):
        get_file_pointer(dummy_context_data, "11111111-eeee-4444-bbbb-333333333333")
    assert get_mock.call_count == 1


def test_pipeline_history_from_input_file_meta():
    history = pipeline_history_from_input_file_meta(dummy_context_data, pipeline_id_1)
    assert history == pipeline_id_0 + "," + pipeline_id_1
