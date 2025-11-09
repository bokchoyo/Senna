from database.cars import Cars
from database.users import Users
from helpers.config import Config
from helpers.logger import Logger
from motor.motor_asyncio import AsyncIOMotorClient

config = Config()
logger = Logger('garages.log')

class Garages:
    def __init__(self):
        self.client = AsyncIOMotorClient(config.get_mongodb_uri())
        self.garages = self.client['private']['garages']
        self.users = Users()
        self.cars = Cars()

    async def add_garage(self, user_id):
        garage = {
            '_id': user_id,
            'cars': {}
        }
        try:
            await self.garages.insert_one(garage)
            await logger.log_info('add_garage()', f'Added garage {user_id}')
        except Exception as e:
            await logger.log_error('add_garage()', f'Error adding garage {user_id}: {e}')

    async def add_car(self, user_id, make, model, trim, year):
        car = await self.cars.get_car(make, model, trim, year)
        if not car:
            await logger.log_error('add_car()', f'Car not found: {make}, {model}, {trim}, {year}')
            return 0
        try:
            car_id = await self.users.increment_last_car_id(user_id)
            if car_id < 1: return car_id
            result = await self.garages.update_one(
                {'_id': user_id},
                {'$set': {f'cars.{car_id}': car}}
            )
            if result.modified_count > 0:
                await logger.log_info('add_car()', f'{make}, {model}, {trim}, {year} added to garage {user_id}')
            else:
                await logger.log_warning('add_car()', f'Garage not found: {user_id}')
                return 0
        except Exception as e:
            await logger.log_error('add_car()', f'Error adding {make}, {model}, {trim}, {year} to garage {user_id}: {e}')
            return -1

    async def get_car(self, user_id, car_id):
        try:
            garage = await self.garages.find_one({'_id': user_id})
            if not garage:
                await logger.log_warning('get_car()', f'Garage not found: {user_id}')
                return 0
            car = garage.get('cars', {}).get(str(car_id))
            if car:
                await logger.log_info('get_car()', f'Car {car_id} retrieved from garage {user_id}')
                return car
            else:
                await logger.log_warning('get_car()', f'Car {car_id} not found in garage {user_id}')
                return 0
        except Exception as e:
            await logger.log_error('get_car()', f'Error retrieving car {car_id} from garage {user_id}: {e}')
            return -1

    async def get_name_and_specs_imperial(self, user_id, car_id):
        try:
            car = await self.get_car(user_id, car_id)
            if car == 0:
                await logger.log_warning('get_name_and_specs_imperial()', f'Car {car_id} not found in garage {user_id}')
                return 0
            specs = {
                "name": car.get("name"),
                "url": car.get("url"),
                "nation": car.get("nation"),
                "class": car.get("class"),
                "rating": car.get("rating"),
                "value": car.get("value"),
                "mph": car.get("mph"),
                "0-60": car.get("0-60"),
                "mpg": car.get("mpg"),
                "G": car.get("G"),
                "hp/lb": car.get("hp/lb"),
                "hp": car.get("hp"),
                "lb-ft": car.get("lb-ft"),
                "lb": car.get("lb"),
            }
            await logger.log_info('get_name_and_specs_imperial()', f'Retrieved imperial specs for car {car_id} from garage {user_id}')
            return specs
        except Exception as e:
            await logger.log_error('get_name_and_specs_imperial()', f'Error retrieving imperial specs for car {car_id} from garage {user_id}: {e}')
            return -1

    async def get_name_and_specs_metric(self, user_id, car_id):
        try:
            car = await self.get_car(user_id, car_id)
            if car == 0:
                await logger.log_warning('get_name_and_specs_metric()', f'Car {car_id} not found in garage {user_id}')
                return 0
            specs = {
                "name": car.get("name"),
                "url": car.get("url"),
                "nation": car.get("nation"),
                "class": car.get("class"),
                "rating": car.get("rating"),
                "value": car.get("value"),
                "kph": car.get("kph"),
                "0-100": car.get("0-100"),
                "kpl": car.get("kpl"),
                "G": car.get("G"),
                "kW/kg": car.get("kW/kg"),
                "kW": car.get("kW"),
                "Nm": car.get("Nm"),
                "kg": car.get("kg"),
            }
            await logger.log_info('get_name_and_specs_metric()',
                                  f'Retrieved imperial specs for car {car_id} from garage {user_id}')
            return specs
        except Exception as e:
            await logger.log_error('get_name_and_specs_metric()',
                                   f'Error retrieving imperial specs for car {car_id} from garage {user_id}: {e}')
            return -1

    async def get_garage(self, user_id):
        try:
            garage = await self.garages.find_one(
                {'_id': user_id},
                {'cars': {'$slice': 20}}
            )
            if not garage:
                await logger.log_warning('get_garage()', f'Garage not found: {user_id}')
                return 0
            cars = garage.get('cars', {})
            await logger.log_info('get_garage()', f'Retrieved top 20 cars from garage {user_id}')
            return {'_id': user_id, 'cars': cars}
        except Exception as e:
            await logger.log_error('get_garage()', f'Error retrieving garage {user_id}: {e}')
            return None