def test_prescription_api(test_app):
    response = test_app.get("/prescription")
    assert response.status_code == 200
    assert response.json() == []