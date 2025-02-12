from app import db

class BundleItem(db.Model):
    __tablename__ = 'bundles'

    ID = db.Column(db.Integer, primary_key=True)
    BundleID = db.Column(db.Integer, nullable=False)
    OrderID = db.Column(db.Integer, db.ForeignKey('orders.ID'), nullable=False)
    Delivery = db.Column(db.Integer, nullable=False)
    DriverStatus = db.Column(db.Integer, nullable=False)
    Priority = db.Column(db.Integer, nullable=False)



    def to_dict(self):
        return {k:v for k,v in self.__dict__.items() if k != '_sa_instance_state'}