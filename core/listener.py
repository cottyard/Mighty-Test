import pyHook

class MouseListener:
    def __init__(self):
        self.hm = pyHook.HookManager()
        self.hm.MouseAllButtons = self._click
        
        self.callback_click = lambda a,b,c,d: None

    def _click(self, event):
        x, y = event.Position
        
        if event.Message == pyHook.HookConstants.WM_LBUTTONDOWN:
            self.callback_click(x, y, 1, True)
        elif event.Message == pyHook.HookConstants.WM_LBUTTONUP:
            self.callback_click(x, y, 1, False)
        elif event.Message == pyHook.HookConstants.WM_RBUTTONDOWN:
            self.callback_click(x, y, 2, True)
        elif event.Message == pyHook.HookConstants.WM_RBUTTONUP:
            self.callback_click(x, y, 2, False)
        elif event.Message == pyHook.HookConstants.WM_MBUTTONDOWN:
            self.callback_click(x, y, 3, True)
        elif event.Message == pyHook.HookConstants.WM_MBUTTONUP:
            self.callback_click(x, y, 3, False)

        return True

    def register_click(self, callback):
        self.callback_click = callback

    def start(self):
        self.hm.HookMouse()

    def stop(self):
        self.hm.UnhookMouse()
