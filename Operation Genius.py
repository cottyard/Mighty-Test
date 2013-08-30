from pymouse import PyMouseEvent
from recorder import Recorder
import time, sys
import cmd

class ClickEventListener(PyMouseEvent):
   def click(self, x, y, button, press):
      if press:
         recorder.OnLeftDown((x, y))

mouseListener = ClickEventListener()
mouseListener.start()

recorder = Recorder()

class CLI(cmd.Cmd):
   running = False
   def do_stop(self, line):
      """stop
      stop listening to mouse event"""
      if self.running:
         recorder.stop()
         self.running = False
         print "recorder has stopped"
      else:
         print "recorder is not running"
      
   def do_clear(self, line):
      """clear
      clear the operation list"""
      recorder.clear()
      
   def do_start(self, line):
      """start
      start listening to mouse event"""
      if self.running:
         print "recorder is already running"
      else:
         recorder.start()
         self.running = True
         print "recorder started running"

   def do_list(self, line):
      """list
      print operation list"""
      recorder.printOpList()

   def do_play(self, line):
      """play
      play the operation list"""
      recorder.play()

   def do_playlist(self, name):
      """playlist [filename]
      play the operation list in file"""
      l = recorder.opList
      
      recorder.load(name)
      recorder.play()

      recorder.opList = l

   def do_save(self, name):
      """save [filename]
      save the operation list to file"""
      recorder.save(name)

   def do_load(self, name):
      """load [filename]
      load the operation list from file"""
      recorder.load(name)
   
   def do_int(self, sec):
      """int [seconds]
      insert intervals"""
      try:
         itv = float(sec)
         recorder.recordInterval(itv)
      except ValueError:
         print "invalid interval."

   def do_check(self, title):
      """check [title]
      snapshot the window whose name contains the title
      as a checkpoint. Recorder will stop playing the list
      and report a failure if a check fails at the checkpoint"""
      recorder.recordCheckpoint(title)

   def do_erase(self, line):
      """undo
      revoke last operation in the list"""
      recorder.erase()
      
   def do_quit(self, sec):
      """quit
      quit cmd"""
      mouseListener.stop()
      return True

cmdInterpreter = CLI()

# if used in command line, execute
# the one command given by the arguments
args = sys.argv[1:]
if len(args) > 0:
   try:
      cmd = ""
      for c in args:
         cmd += c + ' '
      cmdInterpreter.onecmd(cmd)
   except:
      print "Failed due to exceptions"
      
   cmdInterpreter.onecmd("quit")
   
else:
   cmdInterpreter.cmdloop()


#################################################################
#
# Only the first instance of PyMouseEvent class works, i.e.,
# If you destroy mouseListener and creat another ClickEventListener,
# the new listener won't work.
#
# Fix this problem if you know how.
#
#################################################################
