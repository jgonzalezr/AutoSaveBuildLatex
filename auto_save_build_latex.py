'''
AutoSaveBuildLatex - Sublime Text Plugin

Provides a convenient way to turn on and turn off
automatically saving the current file after every modification.

The MIT License (MIT)

Copyright (c) 2015 Jorge Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import sublime
import sublime_plugin
import os.path
from threading import Timer


settings_filename = "auto_save_build_latex.sublime-settings"
save_enable_field = "auto_save_latex_on_modified"
build_enable_field = "auto_build_latex_on_modified"
delay_field = "auto_save_latex_delay_in_seconds"

  
class AutoSaveBuildLatexListener(sublime_plugin.EventListener):

  event_queue = [] # Save queue for on_modified events.

  def on_modified(self, view):
    tex_root = view.file_name()
    self.tex_dir, self.tex_name = os.path.split(tex_root)
    self.base_name, self.tex_ext = os.path.splitext(self.tex_name)
    # sublime.status_message(self.tex_ext.upper()) # Print File extension

    settings = sublime.load_settings(settings_filename)
    if not ((settings.get(save_enable_field) or settings.get(build_enable_field)) and view.file_name() and view.is_dirty() and (self.tex_ext.upper() == ".TEX")):
      sublime.status_message('This is not a .tex file')   
      return
  
    delay = settings.get(delay_field)
 

    def callback(): 
      '''
      Must use this callback for ST2 compatibility
      '''
      if view.is_dirty() and not view.is_loading():
        if settings.get(save_enable_field):
          view.run_command("save")
          # sublime.status_message("Save Command")
        if settings.get(build_enable_field):
          view.window().run_command("build") 
          # sublime.status_message("Build Command") 
      else:
        print("auto-save-build-latex callback invoked, but view is",
              "currently loading." if view.is_loading() else "unchanged from disk.")


    def debounce_save_build():
      '''
      If the queue is longer than 1, pop the last item off,
      Otherwise save and reset the queue.
      '''
      if len(AutoSaveBuildLatexListener.event_queue) > 1:
        AutoSaveBuildLatexListener.event_queue.pop()
      else:
        sublime.set_timeout(callback, 0)
        AutoSaveBuildLatexListener.event_queue = []


    AutoSaveBuildLatexListener.event_queue.append(0) # Append to queue for every on_modified event.
    Timer(delay, debounce_save_build).start() # Debounce save by the specified delay.


'''
Toggle auto-save-latex and auto-build-latex on and off. Can be bound to a keystroke, e.g. ctrl+shift+b
and ctrl+shif+s for build and save respectively.
If enable argument is given, auto save or build will be enabled (if True) or disabled (if False).
If enable is not provided, auto save or build will be toggled (on if currently off and vice versa).
'''

class AutoSaveLatexCommand(sublime_plugin.ApplicationCommand):

  def run(self, enable=None):
    settings = sublime.load_settings(settings_filename)
    if enable is None: # toggle
      enable = not settings.get(save_enable_field)
    settings.set(save_enable_field, enable)
    sublime.status_message("AutoSaveLatex Turned %s" % ("On" if enable else "Off"))

class AutoBuildLatexCommand(sublime_plugin.ApplicationCommand):

  def run(self, enable=None): 
    settings = sublime.load_settings(settings_filename)
    if enable is None: # toggle
      enable = not settings.get(build_enable_field)
    settings.set(build_enable_field, enable)
    sublime.status_message("AutoBuildLatex Turned %s" % ("On" if enable else "Off"))
