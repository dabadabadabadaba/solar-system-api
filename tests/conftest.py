import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra): # if the request is finished, we're not using the database anymore, **extra means any extra variables that might be passed in 
        db.session.remove
    
    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context(): 
        db.drop_all()

@pytest.fixture
def client(app): # the app that's passed in is referring the fixture above
    return app.test_client()

@pytest.fixture
def two_planets(app):
    planet1 = Planet(name="Blargh", description="The Brown Planet", num_of_moons=6)
    planet2 = Planet(name="Cupcake", description="The Sweet Planet", num_of_moons=5)

    db.session.add(planet1)
    db.session.add(planet2)
    db.session.commit()