from app import db

class Car(db.Model):
    __tablename__ = 'cars'

    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    Model = db.Column(db.String, nullable=False)
    Size = db.Column(db.Integer, nullable=False)

    Driver = db.relationship('Driver', back_populates='DriverCar')

    def to_dict(self):
        return {k:v for k,v in self.__dict__.items() if k != '_sa_instance_state'}
