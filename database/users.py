import asyncio
from decimal import Decimal
from helpers.config import Config
from prettytable import PrettyTable
from helpers.logger import Logger
from motor.motor_asyncio import AsyncIOMotorClient

logger = Logger('users.log')
config = Config()

class Users:
    def __init__(self):
        self.client = AsyncIOMotorClient(config.get_mongodb_uri())
        self.users = self.client['private']['users']

    async def add_user(self, user_id, user_name):
        doc = {
            '_id': user_id,
            'name': user_name,
            'metric': False,
            'cmds': 1,
            'lvl': 0,
            'xp': 0,
            'last_car_id': 0,
            'type_win': 0,
            'type_loss': 0,
            'triv_cor': 0,
            'triv_inc': 0,
            'bal': 100000,
            'life_bal': 100000,
            'garage_val': 0,
            'trunk_val': 0,
            'car': 1,
            'location': 'Earth',
        }

        try:
            await self.users.insert_one(doc)
            await logger.log_info('add_user()', f'Added user {user_id}')
        except Exception as e:
            await logger.log_error('add_user()', e)

    async def contains(self, user_id):
        try:
            found_id = await self.users.find_one({'_id': user_id}, {'_id': 1})
            await logger.log_info('contains()', f'Users contains {found_id}')
            return found_id is not None
        except Exception as e:
            await logger.log_error('contains()', f'Error while finding {user_id} in users: {e}')
            return False

    async def increment_last_car_id(self, user_id):
        try:
            user = await self.users.find_one_and_update(
                {'_id': user_id},
                {'$inc': {'last_car_id': 1}},
                return_document=True
            )
            if user:
                return user.get('last_car_id', 0)
            else:
                await logger.log_warning('increment_last_car_id()', f'User not found: {user_id}')
                return 0
        except Exception as e:
            await logger.log_error('get_last_car_id()',
                                   f'Error retrieving and updating last_car_id for user {user_id}: {e}')
            return -1

    async def get_metric(self, user_id):
        try:
            user = await self.users.find_one({'_id': user_id}, {'_id': 0, 'metric': 1})
            if user is not None:
                return user.get('metric', False)
            else:
                await logger.log_warning('uses_metric()', f'User not found: {user_id}')
                return None
        except Exception as e:
            await logger.log_error('uses_metric()', f'Error retrieving metric for user {user_id}: {e}')
            return None

    #
    # async def get_user(self, user_id):
    #     return await self.users_get('SELECT * FROM users WHERE id = ?', user_id)
    #
    # async def add_to_garage(self, user_id, car_name):
    #     car_data = await self.car_db.get_car(car_name)
    #     await self.execute_set('''
    #     INSERT INTO garage (name, make, model, trim, year, nationality, urls, tier, rating, value, parts,
    #                   imperial_top_speed, metric_top_speed, top_speed_rating,
    #                   imperial_acceleration, metric_acceleration, acceleration_rating,
    #                   handling, handling_rating, range,
    #                   imperial_power, metric_power, imperial_torque, metric_torque, imperial_weight, metric_weight,
    #                   user_id)
    #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     ''', *car_data, user_id)
    #
    # async def get_highest_car_id(self, user_id):
    #     return await self.users_get('SELECT COALESCE(MAX(id), 0) FROM garage WHERE user_id = ?;', user_id)
    #
    # async def get_lowest_car_id(self, user_id):
    #     return await self.users_get('SELECT MIN(id) FROM garage WHERE user_id = ?', user_id)
    #
    # async def remove_car(self, user_id, car_id):
    #     await self.execute_set('DELETE FROM garage WHERE user_id = ? AND id = ?', user_id, car_id)
    #
    # async def has_car(self, user_id, car_id):
    #     car = await self.users_get('SELECT id FROM garage WHERE user_id = ? AND id = ?', user_id, car_id)
    #     return True if car else False
    #
    # async def get_car_msrp(self, user_id, car_id):
    #     return await self.users_get('SELECT msrp FROM garage WHERE user_id = ? AND id = ?;', user_id, car_id)
    #
    # async def get_location(self, user_id):
    #     return await self.users_get('SELECT location FROM users WHERE id = ?;', user_id)
    #
    # async def has_one_car(self, user_id):
    #     car_count = await self.users_get('SELECT COUNT(id) FROM garage WHERE user_id = ?;', user_id)
    #     return True if car_count == 1 else False
    #
    # async def get_top_speeds(self, user_id, car_id):
    #     return await self.users_get(
    #         'SELECT imperial_top_speed, metric_top_speed FROM garage WHERE user_id = ? AND id = ?;', user_id, car_id)
    #
    # async def get_top_speed_quality(self, user_id, car_id):
    #     return await self.users_get('SELECT top_speed_quality FROM garage WHERE user_id = ? AND id = ?;', user_id,
    #                                 car_id)
    #
    # async def get_acceleration_quality(self, user_id, car_id):
    #     return await self.users_get('SELECT acceleration_quality FROM garage WHERE user_id = ? AND id = ?;', user_id,
    #                                 car_id)
    #
    # async def get_accelerations(self, user_id, car_id):
    #     return await self.users_get(
    #         'SELECT imperial_acceleration, metric_acceleration FROM garage WHERE user_id = ? AND id = ?;', user_id,
    #         car_id)
    #
    # async def get_qualities(self, user_id, car_id):
    #     return await self.users_get(
    #         'SELECT top_speed_quality, acceleration_quality FROM garage WHERE user_id = ? AND id = ?;', user_id, car_id)
    #
    # async def get_top_speed_levels(self, user_id, car_id):
    #     return await self.users_get('SELECT level, top_speed_level FROM garage WHERE user_id = ? AND id = ?;', user_id,
    #                                 car_id)
    #
    # async def get_acceleration_levels(self, user_id, car_id):
    #     return await self.users_get('SELECT level, acceleration_level FROM garage WHERE user_id = ? AND id = ?;',
    #                                 user_id, car_id)
    #
    # async def get_top_speed_level(self, user_id, car_id):
    #     return await self.users_get('SELECT top_speed_level FROM garage WHERE user_id = ? AND id = ?;', user_id, car_id)
    #
    # async def get_acceleration_level(self, user_id, car_id):
    #     return await self.users_get('SELECT acceleration_level FROM garage WHERE user_id = ? AND id = ?;', user_id,
    #                                 car_id)
    #
    # async def upgrade_top_speed(self, user_id, car_id):
    #     levels = await self.get_top_speed_levels(user_id, car_id)
    #     top_speed_quality = await self.get_top_speed_quality(user_id, car_id)
    #     base_top_speeds = await self.car_db.get_top_speeds(await self.get_car_name_by_id(user_id, car_id))
    #     current_top_speeds = await self.get_top_speeds(user_id, car_id)
    #     increment = top_speed_quality / 10000
    #     new_imperial_top_speed = current_top_speeds[0] + (base_top_speeds[0] * increment)
    #     new_metric_top_speed = current_top_speeds[1] + (base_top_speeds[1] * increment)
    #     new_level = levels[0] + 1
    #     new_top_speed_level = levels[1] + 1
    #     await self.execute_set('''
    #     UPDATE garage
    #     SET level = ?, top_speed_level = ?, imperial_top_speed = ?, metric_top_speed = ?
    #     WHERE user_id = ? and id = ?;''', new_level, new_top_speed_level, new_imperial_top_speed, new_metric_top_speed, user_id, car_id)
    #
    # async def upgrade_acceleration(self, user_id, car_id):
    #     levels = await self.get_acceleration_levels(user_id, car_id)
    #     acceleration_quality = await self.get_acceleration_quality(user_id, car_id)
    #     base_accelerations = await self.car_db.get_accelerations(await self.get_car_name_by_id(user_id, car_id))
    #     current_accelerations = await self.get_accelerations(user_id, car_id)
    #     increment = acceleration_quality / 10000
    #     new_imperial_acceleration = current_accelerations[0] - (base_accelerations[0] * increment)
    #     new_metric_acceleration = current_accelerations[1] - (base_accelerations[1] * increment)
    #     new_level = levels[0] + 1
    #     new_acceleration_level = levels[1] + 1
    #     await self.execute_set('''
    #             UPDATE garage
    #             SET level = ?, acceleration_level = ?, imperial_acceleration = ?, metric_acceleration = ?
    #             WHERE user_id = ? and id = ?;''', new_level, new_acceleration_level, new_imperial_acceleration, new_metric_acceleration, user_id, car_id)
    #
    # # async def qualify_car(self, user_id, car_id, car_quality, top_speed_quality, acceleration_quality):
    # #     car_name = await self.get_car_name_by_id(user_id, car_id)
    # #     car_specs = await self.car_db.get_specifications(car_name)
    # #     await self.qualify_base_top_speed(user_id, car_id, top_speed_quality, car_specs[0], car_specs[1])
    # #     await self.qualify_base_acceleration(user_id, car_id, acceleration_quality, car_specs[2], car_specs[3])
    # #
    # # async def qualify_power_and_torque(self, user_id, car_id, car_quality, imperial_power, metric_power, imperial_torque, metric_torque):
    # #     pass
    # #
    # # async def qualify_base_top_speed(self, user_id, car_id, top_speed_quality, imperial_top_speed, metric_top_speed):
    # #     multiplier = 1 + ((top_speed_quality - 50) / 500)
    # #     new_imperial_top_speed = round(imperial_top_speed * multiplier, 2)
    # #     new_metric_top_speed = round(metric_top_speed * multiplier, 2)
    # #     await self.execute_set('''
    # #     UPDATE garage
    # #     SET imperial_top_speed = ?, metric_top_speed = ?
    # #     WHERE user_id = ? and id = ?;''', new_imperial_top_speed, new_metric_top_speed, user_id, car_id)
    # #
    # # async def qualify_base_acceleration(self, user_id, car_id, acceleration_quality, imperial_acceleration, metric_acceleration):
    # #     multiplier = 1 + ((acceleration_quality - 50) / 500)
    # #     new_imperial_acceleration = round(imperial_acceleration * multiplier, 2)
    # #     new_metric_acceleration = round(metric_acceleration * multiplier, 2)
    # #     await self.execute_set('''
    # #     UPDATE garage
    # #     SET imperial_acceleration = ?, metric_acceleration = ?
    # #     WHERE user_id = ? and id = ?;''', new_imperial_acceleration, new_metric_acceleration, user_id, car_id)
    #
    # async def get_garage_msrp(self, user_id):
    #     return await self.execute_set('''
    #     SELECT COALESCE(SUM(garage.msrp), 0) FROM users
    #     LEFT JOIN garage ON users.id = garage.user_id
    #     WHERE users.id = ?;
    #     ''', user_id)
    #
    # async def get_garage_size(self, user_id):
    #     return await self.users_get('''
    #     SELECT COALESCE(COUNT(garage.name), 0) FROM users
    #     LEFT JOIN garage ON users.id = garage.user_id WHERE users.id = ?;
    #     ''', user_id)
    #
    # async def get_garage_list(self, user_id):
    #     return await self.execute_get_all('''
    #     SELECT id, name, rating, quality
    #     FROM garage WHERE user_id = ?;
    #     ''', user_id)
    #     # for i, row in enumerate(result):
    #     #     if row is None:
    #     #         print(f'{i}: None')
    #     #     else:
    #     #         print(f'Garage row {i}: {row}')
    #     # return result
    #
    # async def set_driving_car(self, user_id, car_id):
    #     await self.execute_set('UPDATE users SET driving_car_id = ? WHERE id = ?;', car_id, user_id)
    #
    # async def get_balance(self, user_id):
    #     return await self.users_get('SELECT balance FROM users WHERE id = ?;', user_id)
    #
    # async def add_to_balance(self, user_id, amount):
    #     current_balance = await self.get_balance(user_id)
    #     await self.execute_set('UPDATE users SET balance = ? WHERE id = ?', current_balance + int(amount), user_id)
    #
    # async def subtract_from_balance(self, user_id, amount):
    #     current_balance = await self.get_balance(user_id)
    #     await self.execute_set('UPDATE users SET balance = ? WHERE id = ?', current_balance - amount, user_id)
    #
    # async def get_car_name_by_id(self, user_id, car_id):
    #     return await self.users_get('SELECT name FROM garage WHERE user_id = ? AND id = ?;', user_id, car_id)
    #
    # async def get_driving_car_id(self, user_id):
    #     return await self.users_get('SELECT driving_car_id FROM users WHERE id = ?;', user_id)
    #
    # async def get_general_info(self, user_id, car_id):
    #     return await self.users_get('''
    #     SELECT level, rating, quality, top_speed_level, acceleration_level, top_speed_quality, acceleration_quality, year, color, image_url, name, msrp
    #     FROM garage WHERE user_id = ? AND id = ?;
    #     ''', user_id, car_id)
    #
    # async def get_performance_imperial(self, user_id, car_id):
    #     return await self.users_get('''
    #     SELECT imperial_top_speed, imperial_acceleration, imperial_power, imperial_torque
    #     FROM garage WHERE user_id = ? AND id = ?;
    #     ''', user_id, car_id)
    #
    # async def get_performance_metric(self, user_id, car_id):
    #     return await self.users_get('''
    #     SELECT metric_top_speed, metric_acceleration, metric_power, metric_torque
    #     FROM garage WHERE user_id = ? AND id = ?;
    #     ''', user_id, car_id)
    #
    # async def get_url_and_msrp(self, user_id, car_id):
    #     return await self.users_get('''
    #     SELECT image_url, msrp
    #     FROM garage WHERE user_id = ? AND id = ?;
    #     ''', user_id, car_id)
    #
    # async def get_car_for_drag_race(self, user_id):
    #     return await self.users_get('''
    #     SELECT name, rating, tier
    #     FROM garage WHERE user_id = ? AND id = ?;
    #     ''', user_id, await self.get_driving_car_id(user_id))
    #
    # async def get_car_for_track_race(self, user_id):
    #     return await self.users_get('''
    #     SELECT name, imperial_top_speed, acceleration_rating, handling_rating
    #     FROM garage WHERE user_id = ? AND id = ?;
    #     ''', user_id, await self.get_driving_car_id(user_id))
    #
    # async def get_car_for_sell(self, user_id, car_id):
    #     return await self.users_get('SELECT name, msrp FROM garage WHERE user_id = ? AND id = ?;', user_id, car_id)
    #
    # async def get_car_for_showcase(self, user_id, car_id):
    #     return await self.users_get('SELECT name, msrp, rating FROM garage WHERE user_id = ? AND id = ?;', user_id,
    #                                 car_id)
    #
    # async def create_user(self, user_id, username):
    #     await self.execute_set('INSERT INTO users (id, username) VALUES (?, ?);', user_id, username)
    #
    # async def get_imperial(self, user_id):
    #     return await self.users_get('SELECT imperial FROM users WHERE id = ?;', user_id)
    #
    # async def set_imperial(self, user_id, boolean):
    #     await self.execute_set('UPDATE users SET imperial = ? WHERE id = ?;', boolean, user_id)
    #
    # async def print_garage_table(self):
    #     query_columns = 'PRAGMA table_info(garage);'
    #     columns_info = await self.execute_get_all(query_columns)
    #
    #     if not columns_info:
    #         print('Error: Unable to retrieve column information.')
    #         return
    #
    #     column_names = [column[1] for column in columns_info]
    #
    #     query_data = f'SELECT {', '.join(column_names)} FROM garage;'
    #     result = await self.execute_get_all(query_data)
    #
    #     if result:
    #         table = PrettyTable()
    #         table.field_names = column_names
    #
    #         for row in result:
    #             table.add_row(row)
    #
    #         print(table)
    #     else:
    #         print('No data found in the garage table.')
