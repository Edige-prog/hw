import requests


def test_task1():
    expected = [
        {"id": 24, "name": "Rolls-Royce Wraith", "year": "2001"},
        {"id": 9, "name": "Ford Focus ST", "year": "2011"},
        {"id": 12, "name": "Kia Sedona", "year": "2003"},
        {"id": 8, "name": "Lexus RX", "year": "2005"},
        {"id": 49, "name": "Chevrolet Silverado 3500 HD Regular Cab", "year": "2019"},
        {"id": 14, "name": "Ford Explorer", "year": "2000"},
        {"id": 2, "name": "Chevrolet Express 2500 Cargo", "year": "2005"},
        {"id": 92, "name": "Chevrolet Express 1500 Cargo", "year": "2019"},
        {"id": 95, "name": "Ford Taurus", "year": "2019"},
        {"id": 55, "name": "McLaren 570S", "year": "2015"},
    ]

    response = requests.get("http://localhost:8000/cars")
    assert response.json() == expected


def test_task1_part1():
    expected = [{"id": 12, "name": "Kia Sedona", "year": "2003"}]
    response = requests.get("http://localhost:8000/cars?page=3&limit=1")
    assert response.json() == expected


def test_task1_part2():
    expected = [
        {"id": 45, "name": "Ford C-MAX Energi", "year": "2008"},
        {"id": 15, "name": "MINI Hardtop", "year": "2004"},
    ]
    response = requests.get("http://localhost:8000/cars?page=20&limit=2")
    assert response.json() == expected