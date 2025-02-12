from sqlalchemy import select
from Models import Car, Driver, Order, BundleItem
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func



def get_cars(db:SQLAlchemy) -> list[Car]:
    cars = select(Car)
    return db.session.execute(cars).scalars().all()

def get_drivers(db:SQLAlchemy) -> list[Driver]:
    drivers = select(Driver)
    return db.session.execute(drivers).scalars().all()

def get_orders(db:SQLAlchemy) -> list[Order]:
    orders = select(Order)
    return db.session.execute(orders).scalars().all()

def get_bundles(db: SQLAlchemy) -> list[BundleItem]:
    bundles = select(BundleItem)
    return db.session.execute(bundles).scalars().all()

def create_bundle(db: SQLAlchemy, order_ids:list[str]) -> tuple[bool, any]:
    """
    Returns tuple(True, str(new bundle id)
    or tuple (False, str(error msg))
    """
    last_bundle_id = db.session.query(func.max(BundleItem.ID)).scalar()
    if not last_bundle_id:
        new_bundle_id = 1
    else:
        new_bundle_id = last_bundle_id+1
    bundle_items = []

    for order_id in order_ids:
        if not isinstance(order_id, (int,str)):
            return False, f"Expected string, but got {type(order_id).__name__}: {order_id}"

        bundle_items.append(
            BundleItem(BundleID=new_bundle_id, OrderID=order_id, Delivery=0, DriverStatus=0, Priority=0)
        )
        bundle_items.append(
            BundleItem(BundleID=new_bundle_id, OrderID=order_id, Delivery=0, DriverStatus=0, Priority=0)
        )
        update_order(db, order_id, {'BundleID':new_bundle_id})
    db.session.add_all(bundle_items)
    db.session.commit()
    return True, new_bundle_id

def update_bundle_sequence(db: SQLAlchemy, bundle_id:int, data:list[dict]) -> tuple[bool, str]:
    priority = 1
    if not data:
        return False, f"Empty data - {data}"
    
    qry = select(BundleItem).where(BundleItem.BundleID == bundle_id)
    bundle_items = db.session.execute(qry).scalars().all()

    # Set priorities to 0 in case existing bundle is being updated
    for bundle_item in bundle_items:
        bundle_item.Priority = 0



    for sequence_item in data:
        obj = next((item for item in bundle_items if item.OrderID == int(sequence_item['OrderID']) and item.Priority == 0), None)
        if obj:
            obj.Delivery = sequence_item['Delivery']
            obj.Priority = priority
            priority += 1
        else:
            return False, f"Bundle item {sequence_item['OrderID']} not found"

    db.session.commit()

    return True, "success"

def delete_order_from_bundle(db: SQLAlchemy, order_id:int) -> tuple[bool, str]:
    qry = select(Order).where(Order.ID == order_id)
    order = db.session.execute(qry).scalars().first()
    if not order:
        return False, f"Order {order_id} not found"
    if order.BundleID == 0:
        return False, f"Order {order_id} not in a bundle"
    
    order.BundleID = 0

    db.session.query(BundleItem).filter(BundleItem.OrderID == order_id).delete()
    db.session.commit()

    return True, "success"

def delete_bundle(db: SQLAlchemy, bundle_id:int) -> None:
    qry = select(Order).where(Order.BundleID == bundle_id)
    orders = db.session.execute(qry).scalars().all()
    
    for order in orders:
        order.BundleID = 0

    db.session.query(BundleItem).filter(BundleItem.BundleID == bundle_id).delete()
    db.session.commit()

def update_order(db: SQLAlchemy, order_id, field_data:dict):
    order = db.session.query(Order).filter_by(ID=order_id).first()
    
    if not order:
        return False, f"Order [{order_id}] not found"

    for field, value in field_data.items():
        if hasattr(order, field):
            setattr(order, field, value)
        else:
            print(f"Warning: {field} is not a valid column")

    db.session.commit()
    return True, "success"

def assign_driver_to_order(db: SQLAlchemy, order_id:int, driver_id:int):
    qry = select(Order).where(Order.ID == order_id)
    order = db.session.execute(qry).scalars().first()

    if not order:
        return False, f"Order [{order_id}] not found"

    if order.BundleID != 0:
        qry = select(Order).where(Order.BundleID == order.BundleID)
        orders = db.session.execute(qry).scalars().all()

        qry = select(BundleItem).where(BundleItem.BundleID == order.BundleID)
        bundle_items = db.session.execute(qry).scalars().all()

        for item in bundle_items:
            item.DriverStatus = 10

        for order in orders:
            order.DriverUserID = driver_id
            order.DriverStatus = 10
    else:
        order.DriverUserID = driver_id
        order.DriverStatus = 10

    db.session.commit()

    return True, "success"
