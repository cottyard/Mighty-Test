import sys

args = sys.argv[1:]
if len(args) > 0:
    if args[0] == 'playlist':
        import core
        r = core.recorder.Recorder()
        r.load(args[1])
        r.play()
else:
    import core
    import gui

    gui.delegate.recorder = core.recorder.Recorder()
    gui.delegate.listener = core.listener.MouseListener()

    gui.guimain.InitGUI()

    gui.delegate.gui = gui.guimain.GuiMeta()

    gui.guimain.StartGUI()

    del gui.delegate.recorder
    del gui.delegate.listener
    del gui.delegate.gui
    del gui.guimain.app


##
##import gc, time
##
##gc.set_debug(gc.DEBUG_COLLECTABLE)
##gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
##gc.set_debug(gc.DEBUG_INSTANCES)
##gc.set_debug(gc.DEBUG_OBJECTS)
##
##gc.enable()
##    
##while True:
##    time.sleep(2)
##    gc.collect()
##    print gc.get_referents(gui.guimain.app)
##
