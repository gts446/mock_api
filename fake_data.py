from faker import Faker
from faker.providers import DynamicProvider
from Models import Car, Driver, Order
from flask_sqlalchemy import SQLAlchemy
from random import randint, uniform
from datetime import datetime, timedelta
from cruds import *

car_models = [
    "Toyota Corolla", "Toyota Camry", "Toyota RAV4",
    "Honda Civic", "Honda Accord", "Honda CR-V",
    "Ford Focus", "Ford Mustang", "Ford Explorer",
    "Chevrolet Malibu", "Chevrolet Impala", "Chevrolet Tahoe",
    "BMW 3 Series", "BMW X5", "BMW M4",
    "Audi A4", "Audi Q5", "Audi A6",
    "Mercedes C-Class", "Mercedes E-Class", "Mercedes GLE",
    "Nissan Altima", "Nissan Rogue", "Nissan Sentra",
    "Hyundai Elantra", "Hyundai Santa Fe", "Hyundai Tucson",
    "Volkswagen Jetta", "Volkswagen Passat", "Volkswagen Tiguan",
    "Subaru Outback", "Subaru Forester", "Subaru Impreza",
    "Mazda CX-5", "Mazda Mazda3", "Mazda Mazda6",
    "Tesla Model 3", "Tesla Model S", "Tesla Model X",
    "Lexus RX", "Lexus ES", "Lexus GX",
    "Kia Sorento", "Kia Optima", "Kia Sportage",
    "Jeep Wrangler", "Jeep Grand Cherokee", "Jeep Cherokee",
    "Porsche 911", "Porsche Cayenne"
    ]
car = DynamicProvider(
     provider_name="car",
     elements=car_models
)

fake = Faker()

fake.add_provider(car)

MIN_LAT, MIN_LON = 54.6427375057442, 25.2001887058088
MAX_LAT, MAX_LON = 54.7302899425111, 25.3312570459098


def generate_sample_data(db: SQLAlchemy) -> None:
    db.session.query(Car).delete()
    db.session.query(Driver).delete()
    db.session.query(Order).delete()
    db.session.query(BundleItem).delete()
    db.session.commit()
    _generate_sample_cars(db)
    _generate_sample_drivers(db)
    _generate_sample_orders(db)

def _generate_sample_cars(db: SQLAlchemy) -> None:
    new_cars = []
    for _ in range(5):
        random_car = fake.car()
        new_cars.append(Car(Name=random_car, Model=random_car, Size=randint(0,3)))
    db.session.add_all(new_cars)
    db.session.commit()

def _generate_sample_drivers(db: SQLAlchemy) -> None:
    cars = get_cars(db)
    new_drivers = []
    for i in range(5):
        lat = uniform(MIN_LAT, MAX_LAT)
        lon = uniform(MIN_LON, MAX_LON)
        new_drivers.append(Driver(AreaID=1, DriverCarID=cars[i].ID, Name=fake.name(), Latitude=lat, Longitude=lon))
    db.session.add_all(new_drivers)
    db.session.commit()

def _generate_sample_orders(db: SQLAlchemy) -> None:
    # from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    # geolocator = Nominatim(user_agent="geoapi")

    new_orders = []
    for i in range(10):
        lat1, lon1 = uniform(MIN_LAT, MAX_LAT), uniform(MIN_LON, MAX_LON)
        lat2, lon2 = uniform(MIN_LAT, MAX_LAT), uniform(MIN_LON, MAX_LON)

        # location1 = geolocator.reverse((lat1, lon1), exactly_one=True)
        # location2 = geolocator.reverse((lat2, lon2), exactly_one=True)


        pickupdate = datetime.now() + timedelta(minutes=randint(1,120)) 
        new_orders.append(Order(
            Type = 1,
            OrderStatus = 3,
            CustomerPickup = 0,
            DeliveryType = 2,
            DeliveryStatus = 0,
            PickupDate = pickupdate,
            DeliveryDate = pickupdate + timedelta(minutes=30),
            SenderLatitude = lat1,
            SenderLongitude = lon1,
            RecipientLatitude = lat2,
            RecipientLongitude = lon2,
            DriverUserID = 0,
            BundleID = 0,
            DriverStatus = 0,
            SenderName = fake.name(),
            RecipientName = fake.name(),
            UserOrderCount = randint(0,10),
            SenderAddress = f'Random street {randint(1,100)}',
            TakeoutType = 2,
            RecipientAddress = f'Random street {randint(1,100)}',
            PaymentType = 4,
            Distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers,
            TotalFinal = randint(100,10000)/100
            ))
    db.session.add_all(new_orders)
    db.session.commit()


# def _format_address(address):
#     if address:
#         addr = address.raw.get("address", {})
        
#         filtered_address = f"{addr.get('road', '')} {addr.get('house_number','')}, {addr.get('city', '')}, {addr.get('country', '')}"
        
#         return filtered_address.strip(", ")
#     else:
#         return ''




