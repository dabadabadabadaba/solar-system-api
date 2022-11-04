def test_get_all_planets_with_empty_db_returns_empty_list(client): #taking in our client fixture in conftest.py
    response = client.get("/planets") #will run a GET request
    response_body = response.get_json()

    assert response.status_code == 200 # attribute that let's us get the status from the response
    assert response_body == []

def test_get_one_planet_with_empty_db_returns_404(client): # with every new test we write with client, an entirely new database is created and then removed
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "message" in response_body

def test_get_one_planet_with_populated_db_returns_planet_json(client, two_planets):
    response = client.get("/planets/1")
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Blargh", 
        "description": "The Brown Planet", 
        "num_of_moons" : 6
    }

def test_post_one_planet_creates_planet_in_db(client, two_planets):
    response = client.post("/planets", json={
        "name": "Dog",
        "description": "A dog planet",
        "num_of_moons": 3
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "msg" in response_body
    assert response_body["msg"] == "Successfully created the planet Dog"