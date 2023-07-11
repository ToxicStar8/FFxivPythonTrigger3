from FFxivPythonTrigger import game_ext, game_exv
from FFxivPythonTrigger.memory import BASE_ADDR, read_uint
from FFxivPythonTrigger.text_pattern import find_signature_address, find_signature_point


def find_ninj_stiff_addr(sig):
    a1 = find_signature_point(sig) + BASE_ADDR + 0x1b
    return read_uint(a1) + a1 + 4


sigs = {
    "swing_sync": {
        'call': find_signature_address,
        'param': "F6 05 ? ? ? ? ? 74 ? 0F 2F 05 ? ? ? ?",
        'add': BASE_ADDR,
    },
    "swing_read": {
        'call': find_signature_point,
        'param': "E8 * * * * 8B D0 48 8B CE E8 ? ? ? ? 49 8B D7",
        'add': BASE_ADDR,
    },
    "speed_main": {
        'call': find_signature_point,
        'param': "E8 * * * * 44 0F 28 D8 E9 ? ? ? ?",
        'add': BASE_ADDR,
    },
    "speed_fly": {
        'call': find_signature_address,
        'param': "40 ? 48 83 EC ? 48 8B ? 48 8B ? FF 90 ? ? ? ? 48 85 ? 75",
        'add': BASE_ADDR,
    },
    "jump": {
        # 'call': find_signature_address,
        # 'param': "66 66 26 41",
        # 'add': BASE_ADDR
        'call': find_signature_point,
        'param': "48 8D 0D * * * * E8 ? ? ? ? EB ? 48 8B 0D ? ? ? ? B2 ?",
        'add': BASE_ADDR + 0x54
    }
}
