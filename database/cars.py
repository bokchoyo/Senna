from helpers.logger import Logger
import asqlite
import re
import orjson

logger = Logger('cars.log')

def load_data(file_name):
    try:
        with open(rf'C:\Users\bokch\PyCharm\W1\data\{file_name}', 'rb') as file:
            return orjson.loads(file.read())
    except Exception as e:
        print(f"Failed to load JSON data: {e}")
        raise

class Cars:
    def __init__(self):
        self.data = load_data('cars.json')
        self.list = load_data('cars_list.json')

    async def get_car(self, make, model, trim=None, year=None):
        try:
            trims = self.data.get(make, {}).get(model)
            if not trims:
                await logger.log_warning('get_car()', f'Car not found: {make}, {model}')
                return None
            if trim and year:
                car = trims.get(trim, {}).get(year)
                if not car:
                    await logger.log_warning('get_car()', f'Car not found: {make}, {model}, {trim}, {year}')
                    return None
                await logger.log_info('get_car()', f'Retrieved car: {make}, {model}, {trim}, {year}')
                return car
            elif trim and not year:
                years = trims.get(trim)
                if not years:
                    await logger.log_warning('get_car()', f'Car not found: {make}, {model}, {trim}')
                    return None
                top_year = next(iter(years.keys()), None)
                car = years[top_year]
                await logger.log_info('get_car()', f'Retrieved default {make}, {model}, {trim}: {top_year}')
                return car
            elif not trim and not year:
                top_trim = next(iter(trims.keys()), None)
                top_year = next(iter(trims[top_trim].keys()), None)
                car = trims[top_trim][top_year]
                await logger.log_info('get_car()', f'Retrieved default {make}, {model}: {top_trim}, {top_year}')
                return car
        except Exception as e:
            await logger.log_error('get_car()', f'Error retrieving {make}, {model}, {trim}, {year}: {e}')
            return None

    async def get_specs_imperial(self, make, model, trim=None, year=None):
        try:
            car = await self.get_car(make, model, trim, year)
            if car is None:
                await logger.log_warning('get_specs_imperial()', f'Car not found: {make}, {model}, {trim}, {year}')
                return None
            specs = {
                'url': car.get('url'),
                'nation': car.get('nation'),
                'class': car.get('class'),
                'rating': car.get('rating'),
                'value': car.get('value'),
                'mph': car.get('mph'),
                'spd_r': car.get('spd_r'),
                '0-60': car.get('0-60'),
                'acc_r': car.get('acc_r'),
                'mpg': car.get('mpg'),
                'fuel_r': car.get('fuel_r'),
                'G': car.get('G'),
                'hand_r': car.get('hand_r'),
                'hp/lb': car.get('hp/lb'),
                'hp': car.get('hp'),
                'lb-ft': car.get('lb-ft'),
                'lb': car.get('lb'),
            }
            if not trim and not year:
                specs['name'] = car.get('name')
                specs['year'] = car.get('year')
            await logger.log_info('get_specs_imperial()', f'Retrieved imperial specs for {make} {model} {trim} {year}')
            return specs
        except Exception as e:
            await logger.log_error('get_specs_imperial()', f'Error retrieving imperial specs for {make} {model} {trim} {year}: {e}')
            return None

    async def get_specs_metric(self, make, model, trim=None, year=None):
        try:
            car = await self.get_car(make, model, trim, year)
            if car is None:
                await logger.log_warning('get_specs_metric()', f'Car not found: {make}, {model}, {trim}, {year}')
                return None
            specs = {
                'url': car.get('url'),
                'nation': car.get('nation'),
                'class': car.get('class'),
                'rating': car.get('rating'),
                'value': car.get('value'),
                'kph': car.get('kph'),
                'spd_r': car.get('spd_r'),
                '0-100': car.get('0-100'),
                'acc_r': car.get('acc_r'),
                'kpl': car.get('kpl'),
                'fuel_r': car.get('fuel_r'),
                'G': car.get('G'),
                'hand_r': car.get('hand_r'),
                'kW/kg': car.get('kW/kg'),
                'kW': car.get('kW'),
                'Nm': car.get('Nm'),
                'kg': car.get('kg'),
            }
            if not trim and not year:
                specs['name'] = car.get('name')
                specs['year'] = car.get('year')
            await logger.log_info('get_specs_metric()', f'Retrieved metric specs for {make} {model} {trim} {year}')
            return specs
        except Exception as e:
            await logger.log_error('get_specs_metric()', f'Error retrieving metric specs for {make} {model} {trim} {year}: {e}')
            return None

    async def get_makes(self):
        return self.list['makes']

    async def get_models(self, make):
        try:
            return self.list[make]['models']
        except Exception as e:
            await logger.log_error('get_models()', f'Error retrieving models for {make}: {e}')
            return None

    async def get_trims(self, make, model):
        try:
            return self.list[make][model]['trims']
        except Exception as e:
            await logger.log_error('get_trims()', f'Error retrieving trims for {make} {model}: {e}')
            return None

    async def get_years(self, make, model, trim):
        try:
            return self.list[make][model][trim]
        except Exception as e:
            await logger.log_error('get_years()', f'Error retrieving years for {make} {model} {trim}: {e}')
            return None

    async def contains(self, *keys):
        data = self.data
        try:
            for key in keys:
                data = data[key]
            return True
        except KeyError:
            return False
