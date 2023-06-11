import datetime
from uuid import uuid4

from Modules.session.session_shifter import suppose_time_when_enough_resources


FIELD_TYPES = {
    'NONE': 'NONE',
    'RESOURCE': 'RESOURCE',
    'BUILDING': 'BUILDING',
}


class Construction:

    def __init__(self, building_id, field_id):
        self.id = ''
        self.required_resources = {'Wood': 0, 'Clay': 0,
                                   'Iron': 0, 'Crop': 0}
        self.from_level = 0
        self.to_level = 0
        self.building_id = building_id
        self.started_time = 0
        self.supposed_started_time = 0
        self.building_time = ''

        self.finish_date = 0
        self.free_crop = 0
        self.field_type = FIELD_TYPES['NONE']
        self.field_id = field_id
        self.previous_construction = None
        self.next_construction = None

    def __str__(self):
        return str(self.building_id) + ', ' + str(self.started_time) + ', ' + str(self.building_time) + ', ' + str(
            self.finish_date)


class ConstructionsManager:

    def __init__(self, village, building_speed_multiple, navigator):
        self.building_speed_multiple = building_speed_multiple
        self.village = village
        self.keep_order = False
        self.constructions = []
        self.navigator = navigator

    def get_new_id(self) -> str:
        return str(uuid4())

    def recognize_construction_field_type(self, construction: Construction):
        if 5 > construction.building_id and 19 > construction.field_id:
            construction.field_type = FIELD_TYPES['RESOURCE']
        else:
            construction.field_type = FIELD_TYPES['BUILDING']

    def remove(self, item_id):
        construction_to_remove = None

        for construction in self.constructions:
            if construction.id == item_id:
                construction_to_remove = construction
                break
        if not construction_to_remove:
            return False

        next_construction = construction_to_remove.next_construction
        while next_construction:
            next_construction.from_level = construction_to_remove.from_level
            next_construction.to_level = construction_to_remove.to_level
            self.refresh_construction_data(next_construction)
            next_construction = next_construction.next_construction

        self.constructions.remove(construction_to_remove)

    def refresh_construction_data(self, construction: Construction):
        from main import database
        building = database.building_db.select_building_by_id(construction.building_id)
        if not building:
            return False

        if construction.to_level > max([key for key, value in building.build_data.items()]):
            return False

        for key, value in building.build_data[construction.to_level]['required_resources'].items():
            if key == 'free_crop':
                construction.free_crop = int(value) if value else 0
            else:
                construction.required_resources[key] = value

        main_building = self.village.get_construction_site_by_building_id(15)
        main_building_level = main_building['level'] if main_building['level'] else 0
        construction.building_time = building.build_data[construction.to_level]['times'][main_building_level]
        return True

    def append(self, item: Construction):


        if not item.id:
            self.recognize_construction_field_type(item)

        try:
            construction_site = [cs for cs in self.village.construction_sites if cs['id'] == item.field_id][0]
        except IndexError:
            return False

        if not item.id:
            item.from_level = construction_site['level']
            item.to_level = construction_site['level'] + 1

        if not construction_site['id']:
            if not self.village.is_building_id_in_available_building(construction_site['id']):
                return False

        for construction in self.constructions:
            if construction.building_id == item.building_id\
                    and construction.field_id == item.field_id:

                item.from_level = construction.to_level
                item.to_level = construction.to_level + 1
                construction.next_construction = item
                item.previous_construction = construction
        if not item.id:
            item.id = self.get_new_id()

        if not self.refresh_construction_data(item):
            return

        stripped_time = item.building_time.split(':')
        item.building_time = datetime.timedelta(hours=int(stripped_time[0]),
                                                minutes=int(stripped_time[1]),
                                                seconds=int(stripped_time[2]))
        self.constructions.append(item)

    def is_anything_building_currently(self):
        self.refresh_construction_list()
        current_time = datetime.datetime.now()
        for construction in self.constructions:
            if not construction.started_time:
                continue

            if construction.finish_date > current_time:
                return True

        return False

    def refresh_construction_list(self):
        to_delete = []
        current_time = datetime.datetime.now()
        for construction in self.constructions:
            if not construction.started_time:
                continue

            if current_time >= construction.finish_date:
                to_delete.append(construction)

        for construction in to_delete:
            self.constructions.remove(construction)

        return True if to_delete else False

    def build_new_building(self, new_building_id, field_id=0):
        if not field_id:
            empty_field = self.village.get_empty_construction_site()
            if not empty_field:
                return
            field_id = empty_field['id']
        self.navigator.build_new_building(field_id, new_building_id,
                                          self.village.get_available_building_category_index(new_building_id))

    def is_enough_resources(self, construction):
        if construction.free_crop > self.village.free_crop:
            return False

        for key, value in construction.required_resources.items():
            if value > self.village.resources[key]['amount']:
                return False

        return True

    def on_update(self):
        current_buildings = []
        current_time = datetime.datetime.now()
        for construction in self.constructions:
            if construction.started_time:
                current_buildings.append(construction)
                continue

            if not current_buildings:
                if self.build(construction, current_time):
                    return True

                if self.keep_order:
                    return True

                continue
            else:
                if self.village.tribe != 'Romans':
                    continue

                field_types = ['RESOURCE', 'BUILDING']

                for current_building in current_buildings:
                    field_types.remove(current_building.field_type)

                if construction.field_type in field_types:
                    if self.build(construction, current_time):
                        return True

                    if self.keep_order:
                        return True
                    continue

        self.on_supposed_time_calculate()

    def build(self, construction: Construction, current_time):
        if not self.is_enough_resources(construction):
            return False

        if not construction.field_id \
                and not self.village.is_building_id_in_available_building(construction.building_id):
            return

        construction.started_time = current_time
        construction.finish_date = current_time + construction.building_time

        if construction.field_id:
            self.navigator.upgrade_field(construction.field_id)
        else:
            self.build_new_building(construction.building_id, construction.field_id)

        return True

    def on_supposed_time_calculate(self):

        current_resources = {
            'Wood': self.village.resources['Wood']['amount'],
            'Clay': self.village.resources['Clay']['amount'],
            'Iron': self.village.resources['Iron']['amount'],
            'Crop': self.village.resources['Crop']['amount'],
            'free_crop': self.village.free_crop,
        }
        production = {
            'Wood': self.village.resources['Wood']['production'],
            'Clay': self.village.resources['Clay']['production'],
            'Iron': self.village.resources['Iron']['production'],
            'Crop': self.village.resources['Crop']['production'],
        }
        current_time = datetime.datetime.now()
        for construction in self.village.constructions:
            required_resources = {
                'Wood': construction.required_resources['Wood'],
                'Clay': construction.required_resources['Clay'],
                'Iron': construction.required_resources['Iron'],
                'Crop': construction.required_resources['Crop'],
                'free_crop': construction.free_crop
            }
            result = suppose_time_when_enough_resources(required_resources, current_resources,
                                                        production, self.village.magazine_size,
                                                        self.village.granary_size)
            if result:
                current_resources = {
                    'Wood': current_resources['Wood'] - required_resources['Wood'],
                    'Clay': current_resources['Clay'] - required_resources['Clay'],
                    'Iron': current_resources['Iron'] - required_resources['Iron'],
                    'Crop': current_resources['Crop'] - required_resources['Crop'],
                    'free_crop': current_resources['free_crop'] - required_resources['free_crop'],
                }
                time = current_time + datetime.timedelta(seconds=result)
                construction.supposed_started_time = time if result > 0 else ''

    def __len__(self) -> int:
        return len(self.constructions)

    def __iter__(self):
        return iter(self.constructions)

    def __getitem__(self, item) -> Construction:
        return self.constructions[item]

    def __contains__(self, item) -> bool:
        if item in self.constructions:
            return True
        return False
