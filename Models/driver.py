from app import db

class Driver(db.Model):
    __tablename__ = 'drivers'

    ID = db.Column(db.Integer, primary_key=True)
    AreaID = db.Column(db.Integer, nullable=False)
    DriverCarID = db.Column(db.Integer, db.ForeignKey('cars.ID'), nullable=False)
    Name = db.Column(db.String, nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)

    DriverCar = db.relationship('Car', back_populates='Driver')

    def to_dict(self):
        result = {k:v for k,v in self.__dict__.items() if k != '_sa_instance_state'}
        result['DriverCar'] = self.DriverCar.to_dict()
        return result