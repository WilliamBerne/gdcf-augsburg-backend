def test_list_documents_for_member_is_not_shadowed_by_document_id_route(client):
    response = client.get("/documents/member/123")

    assert response.status_code == 200
    assert response.json() == []
