import threading, wx

# make sure to refer to these variables as delegate.var
# because they will not be initialized until runtime

listener = None
recorder = None
gui = None

# always put this decorator around the daemon decorator
# otherwise the gui will be updated from other threads
# which is a dangerous thing to do

def gui_updator(fn):
    def wrapper(*arg, **kw):
        r = fn(*arg, **kw)
        if r == 'daemon':
            wx.CallLater(500, gui.update)
        elif r == 'pass':
            pass
        else:
            gui.update()
    return wrapper

def daemon(fn):
    def wrapper(*arg, **kw):
        threading.Thread(target = fn, args = arg).start()
        return 'daemon'
    return wrapper
