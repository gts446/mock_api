from app import db
import pytz

class Order(db.Model):
    __tablename__ = 'orders'

    ID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.Integer, nullable=False)
    OrderStatus = db.Column(db.Integer, nullable=False)
    CustomerPickup = db.Column(db.Integer, nullable=False)
    DeliveryType = db.Column(db.Integer, nullable=False)
    DeliveryStatus = db.Column(db.Integer, nullable=False)
    PickupDate = db.Column(db.DateTime(timezone=True), nullable=False)
    DeliveryDate = db.Column(db.DateTime(timezone=True), nullable=False)
    SenderLatitude = db.Column(db.Float, nullable=False)
    SenderLongitude = db.Column(db.Float, nullable=False)
    RecipientLatitude = db.Column(db.Float, nullable=False)
    RecipientLongitude = db.Column(db.Float, nullable=False)
    DriverUserID = db.Column(db.Integer, nullable=False)
    BundleID = db.Column(db.Integer, nullable=False)
    DriverStatus = db.Column(db.Integer, nullable=False)
    SenderName = db.Column(db.String)
    RecipientName = db.Column(db.String)
    UserOrderCount = db.Column(db.Integer)
    SenderAddress = db.Column(db.String)
    TakeoutType = db.Column(db.Integer)
    RecipientAddress = db.Column(db.String)
    PaymentType = db.Column(db.Integer)
    Distance = db.Column(db.Float)
    TotalFinal = db.Column(db.Float)
    

    def to_dict(self):
        result = {k:v for k,v in self.__dict__.items() if k != '_sa_instance_state'}
        local_tz = pytz.timezone("Europe/Vilnius")
        result['PickupDate'] = local_tz.localize(self.PickupDate)
        result['DeliveryDate'] = local_tz.localize(self.DeliveryDate)
        return result