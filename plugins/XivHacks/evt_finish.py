from ctypes import *
from FFxivPythonTrigger import text_pattern, memory, game_version, PluginBase

# from func 40 57 48 83 EC ? 48 8B F9 48 8B 89 ? ? ? ? 48 8B C1 (i.6.0.8)

void_6void_func = CFUNCTYPE(*([c_void_p] * 7))


class EvtFinish:
    def __init__(self, plugin: PluginBase):
        self.plugin = plugin
        self.storage = plugin.storage.data.setdefault(f"evt_finish_{game_version}", {})
        if not self.from_storage():
            self.init_new()
            self.plugin.storage.save()

    def init_new(self):
        pattern, offsets = text_pattern.sig_to_pattern("48 8B 2D * * * * 48 8B F9 48 81 C5 * * * *")
        matches = text_pattern._search_from_text(pattern)
        if len(matches) != 1: raise Exception(f"Failed to find signature 0, found {len(matches)} matches")
        address, vals = matches[0]
        self.storage['evt_module_ptr'] = offset = address + offsets[0] + vals[0]
        self.evt_module_ptr = cast(memory.BASE_ADDR + offset, POINTER(c_ulonglong))
        self.storage['evt_module_add'] = self.evt_module_add = vals[1]

        pattern, offsets = text_pattern.sig_to_pattern("88 8F * * * * 48 89 47 * 48 8B 0D * * * *")
        matches = text_pattern._search_from_text(pattern)
        if len(matches) != 1: raise Exception(f"Failed to find signature 1, found {len(matches)} matches")
        address, vals = matches[0]
        self.storage['or_20'] = self.or_20 = vals[0]
        self.storage['to_mod_10'] = self.to_mod_10 = vals[1]
        self.storage['director_module_ptr'] = offset = address + offsets[2] + vals[2]
        self.director_module_ptr = cast(memory.BASE_ADDR + offset, POINTER(c_ulonglong))

        pattern, offsets = text_pattern.sig_to_pattern("80 BF * * * * ? 48 8B 0D ? ? ? ? 75 ? E8 * * * *")
        matches = text_pattern._search_from_text(pattern)
        if len(matches) != 1: raise Exception(f"Failed to find signature 2, found {len(matches)} matches")
        address, vals = matches[0]
        self.storage['director_act_flag'] = self.director_act_flag = vals[0]
        self.storage['get_director_module'] = offset = address + offsets[1] + vals[1]
        self.get_director_module = CFUNCTYPE(POINTER(POINTER(c_ulonglong)), c_int64)(memory.BASE_ADDR + offset)

        pattern, offsets = text_pattern.sig_to_pattern("88 5C 24 ? 4C 8B 10 48 8B C8 41 FF 92 * * * *")
        matches = text_pattern._search_from_text(pattern)
        if len(matches) != 1: raise Exception(f"Failed to find signature 3, found {len(matches)} matches")
        self.storage['direct_action1_idx'] = self.direct_action1_idx = matches[0][1][0] // 8
        self.storage['direct_action2_idx'] = self.direct_action2_idx = self.direct_action1_idx - 1

        data = text_pattern.search_from_text("E8 * * * * 48 85 C0 74 ? 44 0F B6 C3 48 8B D0 48 8B CF E8 * * * *")
        if len(data) != 1: raise Exception(f"Failed to find signature 4, found {len(data)} matches")
        address, vals = data[0]
        self.storage['get_evt'] = offset = address + vals[0]
        self.get_evt = CFUNCTYPE(c_int64, c_void_p)(memory.BASE_ADDR + offset)
        self.storage['finish_evt'] = offset = address + vals[1]
        self.finish_evt = CFUNCTYPE(c_void_p, c_void_p, c_void_p, c_ubyte)(memory.BASE_ADDR + offset)

    def from_storage(self):
        try:
            self.evt_module_ptr = cast(memory.BASE_ADDR + self.storage['evt_module_ptr'], POINTER(c_ulonglong))
            self.evt_module_add = self.storage['evt_module_add']
            self.or_20 = self.storage['or_20']
            self.to_mod_10 = self.storage['to_mod_10']
            self.director_module_ptr = cast(memory.BASE_ADDR + self.storage['director_module_ptr'], POINTER(c_ulonglong))
            self.director_act_flag = self.storage['director_act_flag']
            self.get_director_module = CFUNCTYPE(POINTER(POINTER(c_ulonglong)), c_int64)(memory.BASE_ADDR + self.storage['get_director_module'])
            self.direct_action1_idx = self.storage['direct_action1_idx']
            self.direct_action2_idx = self.storage['direct_action2_idx']
            self.get_evt = CFUNCTYPE(c_int64, c_void_p)(memory.BASE_ADDR + self.storage['get_evt'])
            self.finish_evt = CFUNCTYPE(c_void_p, c_void_p, c_void_p, c_ubyte)(memory.BASE_ADDR + self.storage['finish_evt'])
        except KeyError:
            return False
        return True

    def __call__(self, module=None):
        if module is None: module = self.evt_module_ptr[0] + self.evt_module_add
        director_module = self.get_director_module(self.director_module_ptr[0])
        if director_module:
            if cast(module + self.director_act_flag, POINTER(c_ubyte))[0] == 1:
                # void_6void_func(director_module[0][117])(director_module, 1, 0, 0, 0, 0)
                void_6void_func(director_module[0][self.direct_action2_idx])(director_module, 0, 15, 1, 0, 0)
            # else:
            #     void_6void_func(director_module[0][117])(director_module, 1, 15, 1, 0, 0)
        cast(module + self.to_mod_10, POINTER(c_ulonglong))[0] = module + 0x10
        cast(module + self.or_20, POINTER(c_ubyte))[0] |= 0x20
        _v1 = self.get_evt(module)
        if _v1: self.finish_evt(module, _v1, 0)
