import concurrent
import uuid
from concurrent.futures import ThreadPoolExecutor
import pytest

from embedding_server_client.client import EmbeddingClient
from embedding_server_client.schema import (
    DocumentInsertionRequest,
    DocumentInsertionResponse,
    DocumentQueryRequest,
    DocumentQueryResponse)
from embedding_server_client.schema.health_check import HealthCheck


@pytest.fixture
def bert_client():
    host = "tcp://localhost:5555"
    client = EmbeddingClient(host)
    yield client
    client.close()


def test_request_to_bert_server(bert_client):
    request = DocumentInsertionRequest(
        input=['I like icecream', 'geopolitical policy', 'what is this thing here', 'no thats wrong'],
        model="test_model", user=uuid.uuid4())
    response = bert_client.send_document_insertion_request(request)

    assert response is not None
    assert isinstance(response, DocumentInsertionResponse)
    print(response.to_json_str(indent=4))


def test_request_to_bert_server_with_doc_url(bert_client):
    request = DocumentInsertionRequest(
        input=['Thank you for sharing the link. Good to know that it was a question 8 days ago on Reddit, '
               'but it links to the same issue on GitHub I recommended to follow. I don’t know if it is a coincidence '
               'that you share it minutes after I change the topic title to similar to the one on Reddit. '],
        model="test_model",
        user=uuid.uuid4(),
        doc_urls=["GithubTest2.docx"],
        verbose=True)
    response = bert_client.send_document_insertion_request(request)

    assert response is not None
    assert isinstance(response, DocumentInsertionResponse)
    print(response.to_json_str(indent=4))


def test_query_request_to_embedding_server(bert_client):
    request = DocumentQueryRequest(
        input="Programming",
        model="test_model", user=uuid.uuid4(),
        top_k=10)
    response = bert_client.send_query_request(request)

    assert response is not None
    assert isinstance(response, DocumentQueryResponse)
    print(response.to_json_str(indent=4))


def test_load_test_embedding_server(num_requests: int = 1000):
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        clients = [EmbeddingClient("tcp://localhost:5555") for _ in range(num_requests)]
        future_to_request = {executor.submit(test_request_to_bert_server, client): i for i, client in
                             enumerate(clients)}
        for future in concurrent.futures.as_completed(future_to_request):
            request_id = future_to_request[future]
            try:
                data = future.result()
                print(f"Request {request_id} completed: {data}")
            except Exception as exc:
                print(f"Request {request_id} generated an exception: {exc}")

        for client in clients:
            client.close()


def test_health_check(bert_client):
    response = bert_client.send_health_check_request()

    assert response is not None
    assert isinstance(response, HealthCheck)
    print(response.to_json_str(indent=4))
