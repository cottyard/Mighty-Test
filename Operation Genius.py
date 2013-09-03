from pymouse import PyMouseEvent
from recorder import Recorder
import time, sys
import cmd, shlex

class ClickEventListener(PyMouseEvent):
   def click(self, x, y, button, press):
      if press:
         recorder.OnLeftDown((x, y))

mouseListener = ClickEventListener()
mouseListener.start()

recorder = Recorder()

class CLI(cmd.Cmd):
   running = False
   
   def do_clear(self, line):
      """clear
      Clear the operation list."""
      recorder.clear()
      
   def do_list(self, line):
      """list
      Print operation list."""
      recorder.printOpList()

   def do_play(self, line):
      """play
      Play the operation list."""
      try:
         recorder.play()
      except:
         traceback.print_exc()
      

   def do_playlist(self, name):
      """playlist [filename]
      Play the operation list in file."""
      l = recorder.opList
      
      self.do_load(name)
      self.do_play()

      recorder.opList = l

   def do_save(self, name):
      """save [filename]
      Save the operation list to file."""
      try:
         recorder.save(name)
      except IOError:
         print "invalid path"

   def do_load(self, name):
      """load [filename]
      Load the operation list from file."""
      try:
         recorder.load(name)
      except IOError:
         print "file not found"
         
   def do_stop(self, line):
      """stop
      Stop listening to mouse event."""
      if self.running:
         recorder.stop()
         self.running = False
         print "recorder has stopped"
      else:
         print "recorder is not running"
      
   def do_start(self, line):
      """start
      Start listening to mouse event."""
      if self.running:
         print "recorder is already running"
      else:
         recorder.start()
         self.running = True
         print "recorder started running"

   def do_orient(self, flag = "tl"):
      """orient [flag]
      Change the reference point of mouse position
      relative to the window. This is also
      an operation that will be added to the list.
      Be careful to set it back when you're done
      or the coordinate will be messed up.
      
      Flags are: tl(Top Left)/tr(Top Right)/
                 bl(Bottom Left)/br(Bottom Right).
      Default flag is tl."""
      recorder.recordOrient(flag)
      
   def do_int(self, sec):
      """int [seconds]
      Insert intervals."""
      try:
         itv = float(sec)
         recorder.recordInterval(itv)
      except ValueError:
         print "invalid interval"
         
   def do_snap(self, title_and_filename):
      """snap [title] [filename]
      Add a Snap operation to the list. When this
      operation is played, the recorder will
      snap the window whose name contains the title
      and store the snippet as a file.

      Quote the arguments if they contain spaces."""
      try:
         t_n = shlex.split(title_and_filename)
         recorder.recordSnap(t_n[0], t_n[1])
      except:
         print "invalid argument"
      
   def do_checkpoint(self, title_and_filename):
      """checkpoint [title] [filename]
      Set a checkpoint in the list. At a checkpoint,
      recorder snaps the window and compares the snapshot
      with an image file, and stops playing and reports
      a failure if the comparison fails."""
      try:
         t_n = shlex.split(title_and_filename)
         recorder.recordCheckpoint(t_n[0], t_n[1])
      except:
         print "invalid argument"

   def do_check(self, title_and_filename):
      """check [title] [filename]
      Snaps the window, creates an image and adds a
      checkpoint to the list."""
      try:
         t_n = shlex.split(title_and_filename)
         recorder.createCheckpoint(t_n[0], t_n[1])
      except:
         print "invalid argument"

   def do_resolution(self, w_h):
      """resolution [width] [height]
      Add a Resolution operation to the list.
      When playing this operation, if the system resolution
      is not width * height, it will be reset."""
      try:
         res = map(int, w_h.split())
         recorder.recordResolution(tuple(res))
      except ValueError:
         print "invalid argument"

   def do_edit(self, position):
      """edit [position]
      Adjust where in the list to edit. Let position = -1 to
      jump to the bottom of the list."""
      try:
         recorder.setEdit(int(position))
      except ValueError:
         print "input should be an integer"
      
   def do_erase(self, line):
      """erase
      Delete the operation at the editting position."""
      recorder.erase()

   def do_quit(self, sec):
      """quit
      Quit cmd."""
      mouseListener.stop()
      return True

cmdInterpreter = CLI()

# if used in command line, execute
# the one command given by the arguments
args = sys.argv[1:]
if len(args) > 0:
   import traceback
   try:
      cmd = ""
      for c in args:
         cmd += c + ' '
      cmdInterpreter.onecmd(cmd)
   except:
      traceback.print_exc()
      
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
