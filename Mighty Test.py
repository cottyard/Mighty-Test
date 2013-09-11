import core
import gui

gui.delegate.recorder = core.recorder.Recorder()
gui.delegate.listener = core.listener.MouseListener()

gui.guimain.InitGUI()

gui.delegate.gui = gui.guimain.GuiMeta()

gui.guimain.StartGUI()
