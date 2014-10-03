import sublime
import sublime_plugin
import os

from QuickSearchEnhanced.quick_search import panels

def get_short_path(path):
  for folder in sublime.active_window().folders():
    if path.startswith(folder):
      return path[len(folder) + 1:], True

  return path, False

last_opened_view = None
def open_file(path):
  global last_opened_view

  if os.path.isdir(path):
    return None

  if not os.path.isfile(path):
    file = open(path, 'w')
    file.write('')
    file.close()

  return sublime.active_window().open_file(path)

class FileList():

  def __init__(self, callback, open = None, preview = None, text = None,
    open_if_one_file = True, callers = [], on_create = None):

    self.open = open
    self.preview = preview
    self.text = text
    self.open_if_one_file = open_if_one_file
    self.callback = callback
    self.callers = callers
    self.panel = None
    self.last_preview_id = None
    self.on_create = on_create

  def show(self):
    files = self._get_prepared_files()

    callers = [['file_list', self]] + self.callers
    self.panel = panels.create(files, self._open, None, self._preview,
      self.text, callers, self.on_create)

    should_be_opened = (
      len(files) == 1 and
      files[0] != [None, 'No files found'] and
      self.open_if_one_file
    )

    if should_be_opened:
      self.panel.current = 0
      self._open(self.panel)
      return

    self.panel.show()

  def get_panel(self):
    return self.panel

  def refresh(self):
    self.panel.set_values(self._get_prepared_files())

  def _get_prepared_files(self):
    files = []
    for file in self.callback():
      if not isinstance(file, list):
        file = [file]

      copy = []
      for value in file:
        copy.append(value)

      if len(copy) == 1:
        short_path, _ = get_short_path(copy[0])
        copy.append(os.path.basename(copy[0]))
        copy.append(short_path)

      files.append(copy)

    if len(files) == 0:
      files.append([None, "No files found"])

    return files

  def _open(self, panel):
    result = self.open and self.open(self.panel)
    if result == True:
      return

    path = panel.get_current_value()
    if path == None or os.path.isdir(path):
      sublime.active_window().focus_view(panel.opener)
      return

    open_file(path)

  def preview_file(self, panel):
    path = panel.get_current_value()

    if path != None and os.path.isfile(path):
      # open_file are necessary two times here due to sublime bug
      if self.last_preview_id == sublime.active_window().active_view().id():
        sublime.active_window().open_file(path, sublime.TRANSIENT)

      preview = sublime.active_window().open_file(path, sublime.TRANSIENT)
      is_file_in_views = False
      for view in sublime.active_window().views():
        if view.file_name() == path:
          is_file_in_views = True

      if not is_file_in_views:
        self.last_preview_id = preview.id()

      return preview
    else:

      opener = panel.get_opener()
      if len(sublime.active_window().views()) != 0:
        sublime.active_window().focus_view(opener)

      return opener

  def _preview(self, panel):
    result = self.preview and self.preview(self.panel)
    if result == True:
      return True

    self.preview_file(panel)