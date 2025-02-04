import requests


def test_task2_car1():
    expected = {"id": 6, "name": "BMW X1", "year": "2013"}
    response = requests.get("http://localhost:8000/cars/6")
    assert response.json() == expected


def test_task2_car2():
    expected = {"id": 89, "name": "Aston Martin DB11", "year": "2011"}
    response = requests.get("http://localhost:8000/cars/89")
    assert response.json() == expected


def test_task2_car_not_found():
    response = requests.get("http://localhost:8000/cars/666666")
    assert response.text == "Not found"
    assert response.status_code == 404