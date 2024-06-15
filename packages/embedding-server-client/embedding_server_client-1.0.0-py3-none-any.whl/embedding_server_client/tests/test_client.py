import uuid
from datetime import datetime

import pytest
from unittest.mock import patch
from embedding_server_client.client import EmbeddingClient
from embedding_server_client.error import EmbeddingClientError
from embedding_server_client.schema.document import DocumentInsertionResponse, DocumentInsertionStatus, \
    DocumentInsertionRequest
from embedding_server_client.schema.embedding import (
    Embedding,
    EmbeddingUsage)
from embedding_server_client.schema.zmq_message_header import ZmqMessageType, ZmqMessageStatus, ZmqMessageHeader


@pytest.fixture
def mock_zmq_context():
    with patch('zmq.Context') as mock:
        yield mock


@pytest.fixture
def bert_client(mock_zmq_context):
    return EmbeddingClient('tcp://localhost:5555')


def test_initialization(bert_client, mock_zmq_context):
    assert mock_zmq_context.called
    assert bert_client.host == 'tcp://localhost:5555'


def test_destructor(bert_client, mock_zmq_context):
    bert_client.__del__()
    assert mock_zmq_context.return_value.term.called
    assert mock_zmq_context.return_value.socket.return_value.close.called


def test_send_request_valid(bert_client, mock_zmq_context):
    mock_socket = mock_zmq_context.return_value.socket.return_value

    embedding_data = [Embedding(object='embedding', index=0, embedding=[0.1, 0.2, 0.3])]
    embedding_usage = EmbeddingUsage(prompt_tokens=5, total_tokens=10)
    embedding = DocumentInsertionResponse(status=DocumentInsertionStatus.SUCCESS, embeddings=embedding_data, usage=embedding_usage)

    valid_msgpack_encoded_embedding = embedding.msgpack_pack()

    response_header = ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=ZmqMessageType.DOCUMENT_INSERTION,
        status=ZmqMessageStatus.SUCCESS,
        request_ts=datetime.now(),
        response_ts=datetime.now()
    )
    valid_msgpack_encoded_header = response_header.msgpack_pack()

    mock_socket.recv_multipart.return_value = [valid_msgpack_encoded_header, valid_msgpack_encoded_embedding]

    request = DocumentInsertionRequest(input='test', model='test-model')
    response = bert_client.send_document_insertion_request(request)

    assert isinstance(response, DocumentInsertionResponse)
    assert len(response.embeddings) == 1
    assert response.embeddings[0].embedding == [0.1, 0.2, 0.3]


def test_send_request_invalid_request(bert_client):
    with pytest.raises(ValueError):
        bert_client.send_document_insertion_request('invalid_request')


def test_send_request_exception_handling(bert_client, mock_zmq_context):
    mock_socket = mock_zmq_context.return_value.socket.return_value

    mock_socket.send_multipart.side_effect = Exception("Network error")
    mock_socket.recv_multipart.return_value = [b'error', b'details']

    request = DocumentInsertionRequest(input='test', model="test-model")

    with pytest.raises(Exception) as exc_info:
        bert_client.send_document_insertion_request(request)

    assert "Network error" in str(exc_info.value)


def test_send_request_error_response(bert_client, mock_zmq_context):
    mock_socket = mock_zmq_context.return_value.socket.return_value

    error_header = ZmqMessageHeader(
        zmq_message_id=uuid.uuid4(),
        message_type=ZmqMessageType.DOCUMENT_INSERTION,
        status=ZmqMessageStatus.ERROR,
        error_code=500,
        error_message="Internal Server Error",
        request_ts=datetime.now(),
        response_ts=datetime.now()
    )
    valid_msgpack_encoded_header = error_header.msgpack_pack()

    mock_socket.recv_multipart.return_value = [valid_msgpack_encoded_header]

    request = DocumentInsertionRequest(input='test', model='test-model')
    with pytest.raises(EmbeddingClientError) as exc_info:
        bert_client.send_document_insertion_request(request)

    assert 'Internal Server Error' in str(exc_info.value)
    assert exc_info.value.error_code == 500


def test_send_request_invalid_response_length(bert_client, mock_zmq_context):
    mock_socket = mock_zmq_context.return_value.socket.return_value

    mock_socket.recv_multipart.return_value = [b'some data', b'some more data', b'even more data']

    request = DocumentInsertionRequest(input='test', model='test-model')
    with pytest.raises(ValueError) as exc_info:
        bert_client.send_document_insertion_request(request)

    assert 'Invalid response length' in str(exc_info.value)
