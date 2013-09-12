import win32api, win32con

def is_char_shifted(character):
    """Returns True if the key character is uppercase or shifted."""
    if character.isupper():
        return True
    if character in '<>?:"{}|~!@#$%^&*()_+':
        return True
    return False

def tap_key(character):
    """
    Press and release a given character key.
    """
##    try:
    shifted = is_char_shifted(character)
##    except AttributeError:
##        win32api.keybd_event(character, 0, 0, 0)
##    else:
    if shifted:
        win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    char_vk = win32api.VkKeyScan(character)
    win32api.keybd_event(char_vk, 0, 0, 0)
    if shifted:
        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(char_vk, 0, win32con.KEYEVENTF_KEYUP, 0)

keymask = dict()
keymask["shift"] = win32con.VK_SHIFT
keymask["ctrl"] = win32con.VK_CONTROL

def toggle_key(keyname, action):
    win32api.keybd_event(Key.keymask[keyname], 0, \
                         0 if action \
                         else win32con.KEYEVENTF_KEYUP, 0)
