import base64
import time
from functools import cached_property
from pathlib import Path
from threading import Lock
from traceback import format_exc
from typing import TYPE_CHECKING

import math

from FFxivPythonTrigger import PluginBase, plugins, AddressManager, PluginNotFoundException, game_version, game_ext, frame_inject
from FFxivPythonTrigger.decorator import BindValue, event
from FFxivPythonTrigger.hook import PluginHook
from FFxivPythonTrigger.memory import *
from FFxivPythonTrigger.memory.struct_factory import OffsetStruct, PointerStruct
from FFxivPythonTrigger.text_pattern import get_original_text
from FFxivPythonTrigger.game_utils.se_string.messages import UIGlow, UIForeground
from . import afix, evt_finish
from .sigs import sigs
from .struct import MinMax, ActionParam, ActionEffectEntry

if TYPE_CHECKING:
    from XivNetwork.message_processors.zone_client.update_position_handler import ClientUpdatePositionHandlerEvent
    from XivNetwork.message_processors.zone_client.update_position_instance import ClientUpdatePositionInstanceEvent
    from XivNetwork.message_processors.zone_client.action_send import ClientActionSend
    from XivNetwork.message_processors.zone_server.ability import ActionEffectEvent

action_hook_args_type = [c_int, c_int64, c_int64, POINTER(ActionParam), POINTER(ActionEffectEntry * 8), POINTER(c_ulonglong)]
DEFAULT_SALOCK_FIX1 = 0.35
DEFAULT_SALOCK_FIX2 = 0.5

command = "@hacks"


def in_out_log(func):
    def wrapper(plugin, *args):
        res = func(plugin, *args)
        plugin.logger.debug(func.__name__, res, args)
        return res

    wrapper.__name__ = func.__name__
    return wrapper


hack_zoom = True
hack_swing_reduce = True
hack_ninja_stiff = True
hack_speed = True
hack_afix = True
hack_network_moving = True
hack_ani_lock = True
hack_anti_knock = True
hack_hit_box = True
no_misdirect = True
no_forced_march = True
cutscene_skip = True
status_no_lock_move = True
anti_afk = True or game_ext == 4
jump = True
no_hysteria = True
action_no_move = True
no_kill = True
all_cutscenes_skip = True
stalk_vis = True
anti_chat_block = True


class XivHacks(PluginBase):
    name = "XivHacks"
    layout = str(Path(__file__).parent / 'layout.js')

    def __init__(self):
        super().__init__()
        am = AddressManager(self.name, self.logger)
        self.version_data = self.storage.data.setdefault(game_version, {})
        self._address = am.load(sigs)

        # speed
        if hack_speed:
            self.SpeedMainHook(self, self._address['speed_main'])
            self.SpeedFlyHook(self, self._address['speed_fly'])

        if hack_network_moving:
            self.register_moving_swing()
            
    def onunload(self):
        if jump:
            self.set_jump(None)

    @event("plugin_load:Command")
    def register_command(self, _):
        try:
            plugins.Command.register(self, command, self.process_cmd)
        except PluginNotFoundException:
            self.logger.warning("Command is not found")

    def process_cmd(self, args):
        try:
            cmd = args[0]
            expression = ' '.join(args[1:])
            if isinstance(getattr(self.__class__, cmd, None), BindValue):
                setattr(self, cmd, eval(expression, {}, {'self': self, 'old': getattr(self, cmd)}))
            else:
                self.logger.warning("Command not found")
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(format_exc())

    # speed
    if hack_speed:
        speed_percent = BindValue(default=1, auto_save=True)

        @PluginHook.decorator(c_float, [c_int64, c_byte, c_int], True)
        def SpeedMainHook(self, hook, *args):
            return hook.original(*args) * self.speed_percent

        @PluginHook.decorator(c_float, [c_void_p], True)
        def SpeedFlyHook(self, hook, *args):
            return hook.original(*args) * self.speed_percent

    # moving swing & movement hacks
    if hack_network_moving:
        moving_z_modify = BindValue(default=0, auto_save=True)

        @event("plugin_load:XivNetwork")
        def register_moving_swing(self, _=None):
            try:
                plugins.XivNetwork.register_packet_fixer(self, 'zone', False, 'UpdatePositionInstance', self.makeup_moving_instance)
                plugins.XivNetwork.register_packet_fixer(self, 'zone', False, 'UpdatePositionHandler', self.makeup_moving_handler)
            except PluginNotFoundException:
                self.logger.warning("XivNetwork is not found")
            except Exception as e:
                self.logger.error(e)

        def makeup_moving_handler(self, bundle_header, message_header, raw_message, struct_message):
            if self.moving_swing_enable:
                me = plugins.XivMemory.actor_table.me
                if me and self.moving_swing_time > me.cast_info.total_cast_time - me.cast_info.current_cast_time > 0.3:  # TODO: flag check
                    return None
            if self.moving_no_fall: struct_message.unk0 &= 0xf000
            if self.moving_z_modify: struct_message.pos.z += self.moving_z_modify
            return struct_message

        def makeup_moving_instance(self, bundle_header, message_header, raw_message, struct_message):
            if self.moving_swing_enable:
                me = plugins.XivMemory.actor_table.me
                if me and self.moving_swing_time > me.cast_info.current_cast_time - me.cast_info.total_cast_time > 0.3:  # TODO: flag check
                    return None
            if self.moving_no_fall:
                struct_message.unk0 &= 0xf000
            if self.moving_z_modify:
                struct_message.new_pos.z += self.moving_z_modify
                struct_message.old_pos.z += self.moving_z_modify
            return struct_message

    if jump:
        def set_jump(self, val=None):
            if val is None:
                write_ubytes(self._address['jump'], bytearray(b'\x66\x66\x26\x41'))
            else:
                write_float(self._address['jump'], val)

        @BindValue.decorator(default=10.4, init_set=True, auto_save=True)
        def jump(self, new_val, old_val):
            self.set_jump(new_val)
            return True
