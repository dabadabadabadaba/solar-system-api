from app import db

class Planet (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    num_of_moons= db.Column(db.Integer)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "num_of_moons":self.num_of_moons
            }

    @classmethod
    def from_dict(cls, planet_dict):
        return cls(
            name=planet_dict['name'],
            description=planet_dict['description'],
            num_of_moons= planet_dict['num_of_moons']
        )

