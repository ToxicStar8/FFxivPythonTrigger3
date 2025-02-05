import math
from ctypes import *
from typing import Dict, Set, Iterator, Tuple, Optional, TYPE_CHECKING

from FFxivPythonTrigger import game_ext, game_exv
from FFxivPythonTrigger.memory.struct_factory import OffsetStruct
from FFxivPythonTrigger.popular_struct import Position, Vector3

from FFxivPythonTrigger.utils.shape import circle
from .enum import Jobs, ActorType

ACTOR_TABLE_SIZE = 424


class Effect(OffsetStruct({
    'buff_id': (c_ushort, 0),
    'param': (c_ushort, 2),
    'timer': (c_float, 4),
    'actor_id': (c_uint, 8),
})):
    buff_id: int
    param: int
    timer: float
    actor_id: int

    def __hash__(self):
        return hash((self.buff_id, self.actor_id))


class Effects(Effect * 30):
    if TYPE_CHECKING:
        def __iter__(self) -> Iterator[Effect]:
            pass

        def __getitem__(self, item: int) -> Effect:
            pass

    def get_dict(self, source: Optional[int] = None) -> Dict[int, Effect]:
        return {e_id: effect for e_id, effect in self.get_items(source)}

    def get_set(self, source: Optional[int] = None) -> Set[Effect]:
        return {e_id for e_id, effect in self.get_items(source)}

    def get_items(self, source: Optional[int] = None) -> Iterator[Tuple[int, Effect]]:
        for effect in self:
            if effect.buff_id and (source is None or effect.actor_id == source):
                yield effect.buff_id, effect

    def has(self, status_id: int, source: Optional[int] = None):
        for effect in self:
            if effect.buff_id == status_id and (source is None or effect.actor_id == source):
                return effect.timer or 0.1
        return 0


class CastInfo(OffsetStruct({
    'is_casting': (c_ubyte, 0),
    'interruptible': (c_ubyte, 1),
    'action_type': (c_ushort, 2),
    'action_id': (c_uint, 4),
    'unk_08': (c_uint, 8),
    'cast_target_id': (c_uint, 16),
    'cast_location': (Vector3, 32),
    'unk_30': (c_uint, 48),
    'current_cast_time': (c_float, 52),
    'total_cast_time': (c_float, 56),
    'used_action_id': (c_uint, 60),
    'used_action_type': (c_ushort, 64),
})):
    is_casting: bool
    interruptible: bool
    action_type: int
    action_id: int
    unk_08: int
    cast_target_id: int
    cast_location: Vector3
    unk_30: int
    current_cast_time: float
    total_cast_time: float
    used_action_id: int
    used_action_type: int


if game_exv < (6, 1, 0):
    _actor_struct = {
        '_name': (c_char * 68, 0x30),
        'id': (c_uint, 0x74),
        'b_npc_id': (c_uint, 0x78),
        'e_npc_id': (c_uint, 0x80),
        'owner_id': (c_uint, 0x84),
        'type': (ActorType, 0x8c),
        'sub_type': (c_ubyte, 0x8d),
        'is_friendly': (c_ubyte, 0x8e),
        'effective_distance_x': (c_ubyte, 0x90),
        'player_target_status': (c_ubyte, 0x91),
        'effective_distance_y': (c_ubyte, 0x92),
        '_unit_status_1': (c_ubyte, 0x94),
        'pos': (Position, 0xa0),
        'hitbox_radius': (c_float, 0xc0),
        '_unit_status_2': (c_uint, 0x104),
        'current_hp': (c_uint, 0x1c4),
        'max_hp': (c_uint, 0x1c8),
        'current_mp': (c_uint, 0x1cc),
        'max_mp': (c_uint, 0x1d0),
        'current_gp': (c_ushort, 0x1d4),
        'max_gp': (c_ushort, 0x1d6),
        'current_cp': (c_ushort, 0x1d8),
        'max_cp': (c_ushort, 0x1da),
        'job': (Jobs, 0x1e0),
        'level': (c_ubyte, 0x1e1),
        'pc_target_id': (c_uint, 0x1f0),
        'pc_target_id_2': (c_uint, 0x230),
        'mount_id': (c_ushort, 0xC38),
        'npc_target_id': (c_uint, 0x1818),
        'omen_ptr': (c_ulonglong, 0x1870),
        'b_npc_target_id': (c_uint, 0x1940),
        'b_npc_base': (c_ushort, 0x1998),
        'current_world': (c_ushort, 0x19b4),
        'home_world': (c_ushort, 0x19b6),
        'shield_percent': (c_ubyte, 0x19D9),
        '_status_flags': (c_ubyte, 0x19DF),
        '_status_flags_2': (c_ubyte, 0x19E3),
        'effects': (Effects, 0x1A38),
        'cast_info': (CastInfo, 0x1bc0),
        # 'is_casting_2': (c_bool, 0x1bc2),
        # 'casting_id': (c_uint, 0x1bc4),
        # 'casting_target_id': (c_uint, 0x1bd0),
        # 'casting_progress': (c_float, 0x1bf4),
        # 'casting_time': (c_float, 0x1bf8),
    }
else:
    _actor_struct = {
        '_name': (c_char * 68, 0x30),
        'id': (c_uint, 0x74),
        'b_npc_id': (c_uint, 0x78),
        'e_npc_id': (c_uint, 0x80),
        'owner_id': (c_uint, 0x84),
        'type': (ActorType, 0x8c),
        'sub_type': (c_ubyte, 0x8d),
        'is_friendly': (c_ubyte, 0x8e),
        'effective_distance_x': (c_ubyte, 0x90),
        'player_target_status': (c_ubyte, 0x91),
        'effective_distance_y': (c_ubyte, 0x92),
        '_unit_status_1': (c_ubyte, 0x94),
        'pos': (Position, 0xa0),
        'hitbox_radius': (c_float, 0xc0),
        '_unit_status_2': (c_uint, 0x104),
        'current_hp': (c_uint, 0x1c4),
        'max_hp': (c_uint, 0x1c8),
        'current_mp': (c_uint, 0x1cc),
        'max_mp': (c_uint, 0x1d0),
        'current_gp': (c_ushort, 0x1d4),
        'max_gp': (c_ushort, 0x1d6),
        'current_cp': (c_ushort, 0x1d8),
        'max_cp': (c_ushort, 0x1da),
        'job': (Jobs, 0x1e0),
        'level': (c_ubyte, 0x1e1),
        'pc_target_id': (c_uint, 0x1f0),
        'pc_target_id_2': (c_uint, 0xc50),
        'mount_id': (c_ushort, 0x658),
        'npc_target_id': (c_uint, 0x1818),
        # 'omen_ptr': (c_ulonglong, 0x1870),
        'b_npc_target_id': (c_uint, 0x1940),
        'b_npc_base': (c_ushort, 0x1A94),
        'current_world': (c_ushort, 0x1ab0),
        'home_world': (c_ushort, 0x1ab2),
        'shield_percent': (c_ubyte, 0x19D9),
        '_status_flags': (c_ubyte, 0x1AD6),
        '_status_flags_2': (c_ubyte, 0x1ADA),
        'effects': (Effects, 0x1b28),
        'cast_info': (CastInfo, 0x1cb0),
        # 'is_casting_2': (c_bool, 0x1bc2),
        # 'casting_id': (c_uint, 0x1bc4),
        # 'casting_target_id': (c_uint, 0x1bd0),
        # 'casting_progress': (c_float, 0x1bf4),
        # 'casting_time': (c_float, 0x1bf8),
    }


class Actor(OffsetStruct(_actor_struct)):
    _name: bytes
    id: int
    b_npc_id: int
    e_npc_id: int
    owner_id: int
    type: ActorType
    sub_type: int
    is_friendly: int
    effective_distance_x: int
    player_target_status: int
    effective_distance_y: int
    _unit_status_1: int
    pos: Position
    hitbox_radius: float
    _unit_status_2: int
    current_hp: int
    max_hp: int
    current_mp: int
    max_mp: int
    current_gp: int
    max_gp: int
    current_cp: int
    max_cp: int
    job: Jobs
    level: int
    pc_target_id: int
    pc_target_id_2: int
    npc_target_id: int
    b_npc_target_id: int
    current_world: int
    home_world: int
    shield_percent: int
    _status_flags: int
    _status_flags_2: int
    effects: Effects
    # is_casting_1: bool
    # is_casting_2: bool
    # casting_id: int
    # casting_target_id: int
    # casting_progress: float
    # casting_time: float
    cast_info: CastInfo
    mount_id: int
    b_npc_base: int

    def __hash__(self):
        return self.id | self.b_npc_id

    def __eq__(self, other):
        match other:
            case int():
                return self.id == other
            case str():
                return self.name == other
            case Actor():
                return self.id == other.id
            case unexpected:
                raise TypeError(f'unexpected type: {unexpected}')

    def hitbox(self):
        return circle(self.pos.x, self.pos.y, self.hitbox_radius)

    def absolute_distance_xy(self, target: 'Actor'):
        return math.sqrt((self.pos.x - target.pos.x) ** 2 + (self.pos.y - target.pos.y) ** 2)

    def target_radian(self, target: 'Actor'):
        return math.atan2(target.pos.x - self.pos.x, target.pos.y - self.pos.y)

    def target_position(self, target: 'Actor'):
        a = abs(abs(self.target_radian(target) - self.pos.r) - math.pi)
        if a < math.pi / 4:
            return "BACK"
        elif a < math.pi / 4 * 3:
            return "SIDE"
        else:
            return "FRONT"

    @property
    def name(self):
        return self._name.decode('utf-8', errors='ignore') or f"{self.type.value}_{self.id:x}"

    @property
    def can_select(self):
        a1 = self._unit_status_1
        a2 = self._unit_status_2
        return bool(a1 & 0b10 and a1 & 0b100 and ((a2 >> 11 & 1) <= 0 or a1 >= 128) and not a2 & 0xffffe7f7)

    @property
    def is_hostile(self):
        return bool(self._status_flags & 0b1)

    @property
    def is_in_combat(self):
        return bool(self._status_flags & 0b10)

    @property
    def is_weapon_out(self):
        return bool(self._status_flags & 0b100)

    @property
    def is_party_member(self):
        return bool(self._status_flags & 0b10000)

    @property
    def is_alliance_member(self):
        return bool(self._status_flags & 0b100000)

    @property
    def is_friend(self):
        return bool(self._status_flags & 0b1000000)

    @property
    def is_casting(self):
        return bool(self._status_flags & 0x10000000)

    if game_exv < (6, 1, 0):
        @property
        def is_positional(self):
            return not bool(cast(byref(self), POINTER(c_ubyte))[0x19e3] & 0x80)
    else:
        @property
        def is_positional(self):
            return not bool(cast(byref(self), POINTER(c_ubyte))[0x1ada] & 0xf)  # TODO: check if this is correct

    @property
    def target_id(self):
        if self.type == 1:
            return self.pc_target_id_2
        elif self.type == 2:
            return self.b_npc_target_id
        else:
            return self.npc_target_id


class ActorTable(POINTER(Actor) * ACTOR_TABLE_SIZE):
    _aid_to_idx_cache: dict

    @property
    def me(self):
        return self.get_actor(0)

    def get_actor(self, idx: int) -> Optional[Actor]:
        try:
            return self[idx][0]
        except:
            return None

    def __iter__(self) -> Iterator[Actor]:
        for i in range(ACTOR_TABLE_SIZE):
            actor = self.get_actor(i)
            if actor is not None:
                yield actor

    def items(self) -> Iterator[Tuple[int, Actor]]:
        for i in range(ACTOR_TABLE_SIZE):
            actor = self.get_actor(i)
            if actor is not None:
                yield i, actor

    def get_actor_by_id(self, actor_id: int) -> Optional[Actor]:
        if not actor_id or actor_id == 0xe0000000: return
        if actor_id in self._aid_to_idx_cache:
            actor = self.get_actor(self._aid_to_idx_cache[actor_id])
            if actor and actor.id == actor_id:
                return actor
        for i, actor in self.items():
            self._aid_to_idx_cache[actor.id] = i
            if actor.id == actor_id: return actor

    def get_actors_by_ids(self, _actor_ids: Set[int]) -> Iterator[Actor]:
        actor_ids = set(_actor_ids)
        for actor_id in actor_ids.copy():
            if actor_id in self._aid_to_idx_cache:
                actor = self.get_actor(self._aid_to_idx_cache[actor_id])
                if actor and actor.id == actor_id:
                    actor_ids.remove(actor_id)
                    yield actor
        for i, actor in self.items():
            self._aid_to_idx_cache[actor.id] = i
            if actor.id in actor_ids:
                actor_ids.remove(actor.id)
                yield actor
                if not actor_ids: return

    def get_actors_by_name(self, name: str) -> Iterator[Actor]:
        for actor in self:
            if actor.name == name:
                yield actor
