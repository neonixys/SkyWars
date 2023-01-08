import json
from dataclasses import dataclass
from random import uniform
from typing import Optional

import marshmallow
import marshmallow_dataclass


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    """
    Класс содержит 2 списка - с оружием и с броней
    """
    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        """
        Метод возвращает объект оружия по имени
        """
        for weapon in self.equipment.weapons:
            if weapon_name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name) -> Optional[Armor]:
        """
        Метод возвращает объект брони по имени
        """
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> list:
        """
        :return: список с оружием
        """
        return [
            weapon.name for weapon in self.equipment.weapons
        ]

    def get_armors_names(self) -> list:
        """
        :return: список с броней
        """
        return [
            armor.name for armor in self.equipment.armors
        ]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:

        """
        Метод загружает json в переменную EquipmentData
        """
        my_absolute_path = './data/equipment.json'
        with open(my_absolute_path, 'r', encoding='utf-8') as file:

            data = json.load(file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError

