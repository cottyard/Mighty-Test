from pymouse import PyMouseEvent
from recorder import Recorder
import winutil
import time, sys
import cmd, shlex

class ClickEventListener(PyMouseEvent):
   def click(self, x, y, button, press):
      if press:
         if button == 1:
            recorder.OnLeftDown((x, y))
         elif button == 2:
            recorder.OnRightDown((x, y))

mouseListener = ClickEventListener()
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

   def do_play(self, interval):
      """play [interval]
      Play the operation list to the editting point.
      The argument is the time to wait between operations
      (Interval operations not included).

      Omit the argument to use a default interval of 0.5s"""
      try:
         recorder.play(int(interval))
      except ValueError:
         recorder.play()
      except:
         traceback.print_exc()

   def do_playlist(self, name):
      """playlist [filename]
      Play the operation list in file."""
      l = recorder.opList
      
      self.do_load(name)
      self.do_play("")

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
      The flag is set to tl everytime before playing the list."""
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
      Add a CheckPoint operation to the list. At a checkpoint,
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
   
   def do_maximize(self, title):
      """maximize [title]
      Maximize the window."""
      recorder.recordWinState(title, "max")

   def do_normalize(self, title):
      """normalize [title]
      Normalize the window."""
      recorder.recordWinState(title, "norm")

   def do_minimize(self, title):
      """minimize [title]
      Minimize the window."""
      recorder.recordWinState(title, "min")

   def do_keydown(self, key):
      """keydown [key]
      Add a Key operation to the list.
      Press down the key.
      Keys supported:
         shift
         ctrl
      """
      recorder.recordKey(key, Recorder.KEY_DOWN)
      
   def do_keyup(self, key):
      """keyup [key]
      Add a Key operation to the list.
      Release the key.
      """
      recorder.recordKey(key, Recorder.KEY_UP)
   
   def do_resolution(self, w_h):
      """resolution [width] [height]
      Add a Resolution operation to the list.
      When playing this operation, the system resolution
      will be set to width * height if it's not.

      The system resolution will be recovered after
      playing the list."""
      try:
         res = map(int, w_h.split())
         recorder.recordResolution(tuple(res))
      except ValueError:
         print "invalid argument"

   def do_edit(self, position):
      """edit [position]
      Adjust where in the list to edit. Omit the argument
      to jump to the bottom of the list."""
      try:
         recorder.setEdit(int(position))
      except ValueError:
         recorder.setEdit(-1)
      
   def do_erase(self, n):
      """erase [n]
      Delete n operations above the editting position.
      Omit the argument to delete 1 operation."""
      try:
         recorder.erase(int(n))
      except ValueError:
         recorder.erase(1)

   def do_quit(self, sec):
      """quit
      Quit cmd."""
      mouseListener.stop()
      return True




if __name__ == '__main__':
   
   interpreter = CLI()
   mouseListener.start()
   
   # if used in command line, execute
   # the one command given by the arguments
   import traceback
   args = sys.argv[1:]
   if len(args) > 0:
      
      try:
         cmd = ""
         for c in args:
            cmd += c + ' '
         interpreter.onecmd(cmd)
      except:
         traceback.print_exc()
         
      interpreter.onecmd("quit")
      
   else:
      try:
         interpreter.cmdloop()
      except:
         traceback.print_exc()
         interpreter.onecmd("quit")


#################################################################
#
# Only the first instance of PyMouseEvent class works, i.e.,
# If you destroy mouseListener and creat another ClickEventListener,
# the new listener won't work.
#
# Fix this problem if you know how.
#
#################################################################
