import json
from flask import jsonify, Request


class APIRequest:
    def __init__(self, function: str, data: dict[str, any]):
        self.function = function
        self.data = data

    @classmethod
    def form_request(cls, req: Request) -> tuple["APIRequest | None", "str | None"]:
        """
        Returns APIRequest object, error message
        """
        json_str = req.form.get("jsonrequest") or req.data.decode("utf-8")
        if not json_str:
            return None, "Missing 'jsonrequest' parameter"
        try:
            data_dict = json.loads(json_str)
        except json.JSONDecodeError:
            return None, "Invalid JSON format inside 'jsonrequest'"
        if "Function" not in data_dict or "Data" not in data_dict:
            return None, "Missing 'Function' or 'Data' parameter inside 'jsonrequest'"
        
        return cls(data_dict["Function"], data_dict["Data"]), None

class APIResponse:
    def __init__(self, success: bool, data: dict[str, any] = None, message: str = ""):
        self.success = success
        self.data = data or {}
        self.message = message

    def to_json(self):
        return jsonify({"success": self.success, "Data": self.data, "message": self.message})

class APIHandler:
    def __init__(self,request = APIRequest):
        self.request = request

    def result(self,db) -> tuple[bool, any, str]:

        """
        Returns  tuple(bool,data,message[str])
        """
        func = FUNCTION_MAP.get(self.request.function)
        if not func:
            return False, None, f'Function {self.request.function} not found'
        return func(db, self.request.data)
    

    @staticmethod
    def get_driver_car_list(db, data=None)-> tuple[bool, any, str]:
        from cruds import get_cars
        return True, {"Items": [car.to_dict() for car in get_cars(db)]}, ''
    
    @staticmethod
    def get_dispatch_info(db, data=None)-> tuple[bool, any, str]:
        from cruds import get_drivers, get_orders
        return True, {"Drivers": [driver.to_dict() for driver in get_drivers(db)], "Orders": [order.to_dict() for order in get_orders(db)]}, ''
    
    @staticmethod
    def get_order_bundles(db, data=None)-> tuple[bool, any, str]:
        from cruds import get_bundles
        bundles_items_list = [bundle.to_dict() for bundle in get_bundles(db)]
        bundles = {}
        for bundle_item in bundles_items_list:
            bundle_item['ID'] = bundle_item['BundleID']
            if bundle_item['ID'] not in bundles:
                bundles[bundle_item['ID']] = [bundle_item]
            else:
                bundles[bundle_item['ID']].append(bundle_item)
        result = [{'ID':id, 'Items':items} for id, items in bundles.items()]
        return True, {"OrderBundles": result}, ''
    
    @staticmethod
    def create_new_bundle(db, data=None) -> tuple[bool, any, str]:
        if 'Orders' not in data:
            return False, '', '[Orders] not found'
        
        from cruds import create_bundle
        
        success, result = create_bundle(db, data['Orders'])
        if success:
            return True, {'ID': result},''
        else:
            return False, '', result
        
    @staticmethod
    def update_bundle(db, data) -> tuple[bool, any, str]:
        if 'ID' not in data:
            return False, '', '[ID] not found'
        
        if 'Items' not in data:
            return False, '', '[Items] not found'
        
        for item in data['Items']:
            if 'OrderID' not in item or 'Delivery' not in item:
                return False, '', '[Items] must be list[dict[str("OrderID"):int, str("Delivery"):bool]]'

        from cruds import update_bundle_sequence
        
        status, msg = update_bundle_sequence(db, data['ID'], data['Items'])

        if status:
            return True, '', ''
        else:
            return False, '', msg
    
    @staticmethod
    def delete_order_from_bundle(db, data) -> tuple[bool, any, str]:
        if 'ID' not in data:
            return False, '', '[ID] not found'
        from cruds import delete_order_from_bundle
        status, msg = delete_order_from_bundle(db, data['ID'])

        if status:
            return True,'',''
        else:
            return False, '', msg
        
    @staticmethod
    def delete_bundle(db, data) -> tuple[bool, any, str]:
        if 'ID' not in data:
            return False, '', '[ID] not found'
        from cruds import delete_bundle
        delete_bundle(db, data['ID'])

       
        return True,'',''
        
    
    @staticmethod
    def assign_driver(db, data=None):
        if 'OrderID' not in data:
            return False, '', '[OrderID] not found'
        if 'DriverUserID' not in data:
            return False, '', '[DriverUserID] not found'

        from cruds import assign_driver_to_order

        update_status, msg = assign_driver_to_order(db, data['OrderID'], data['DriverUserID'])

        if update_status:
            return True, '',''
        
        else:
            return False, '', msg
   
    
    @staticmethod
    def generate_data(db, data=None) -> None:
        from fake_data import generate_sample_data
        generate_sample_data(db)
    
FUNCTION_MAP = {
    "GetDriverCarList": APIHandler.get_driver_car_list,
    "GetDispatchInfo": APIHandler.get_dispatch_info,
    "GetOrderBundles": APIHandler.get_order_bundles,
    'GenerateSampleData': APIHandler.generate_data,
    'CreateOrderBundle' :  APIHandler.create_new_bundle,
    'AssignDriverUserToOrder' : APIHandler.assign_driver,
    'CreateOrderBundleSequence' : APIHandler.update_bundle,
    'DeleteOrderFromBundle' : APIHandler.delete_order_from_bundle,
    'DeleteOrderBundle' : APIHandler.delete_bundle
}