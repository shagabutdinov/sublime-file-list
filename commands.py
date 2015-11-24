import sublime
import sublime_plugin
import os
import shutil

try:
  from QuickSearchEnhanced import quick_search
  from FileList.file_list import get_short_path
  from FolderFiles.folder_files import FolderFiles
except ImportError as error:
  sublime.error_message("Dependency import failed; please read readme for " +
   "FileList plugin for installation instructions; to disable this " +
   "message remove this plugin; message: " + str(error))
  raise error

class DeleteFileInList(sublime_plugin.TextCommand):
  def run(self, edit, confirm = True):
    panel = quick_search.panels.get_current()
    value = panel.get_current_value()

    type = None
    if os.path.isfile(value):
      type = 'file'
    elif os.path.isdir(value):
      type = 'directory'

    if type == None:
      return

    panel.hide()

    delete = not confirm or sublime.ok_cancel_dialog('Are you sure you want ' +
      'to delete ' + type + ' "' +os.path.basename(value) + '"?', 'DELETE ' +
      type.upper())

    if delete:
      try:
        if type == 'file':
          os.remove(value)
        else:
          shutil.rmtree(value)
      except Exception as error:
        sublime.error_message('Delete failed: {0}'.format(error))

    panel.refresh()
    panel.show()

class InsertFileInListToView(sublime_plugin.TextCommand):
  def run(self, edit, type = 'relative'):
    panel = quick_search.panels.get_current()
    value = panel.get_current_value()
    opener = panel.get_opener()

    if type == 'relative':
      value = os.path.relpath(value, os.path.dirname(opener.file_name()))
    elif type == 'short':
      value, _ = get_short_path(value)
    elif type == 'name':
      value = os.path.basename(value)
    elif type != 'absolute':
      raise Exception('Unknown type "' +type + '"')

    opener.run_command('insert', {'characters': value})
    panel.close(None)


class RenameFile():
  def __init__(self, file_name):
    self.file_name = file_name
    self.folder = FolderFiles(os.path.dirname(file_name), None, False,
      '♻', {'text': os.path.basename(file_name)}, [['rename', self]])

  def get_path(self):
    return self.path

  def show(self):
    self.folder.show()

  def rename(self, file_name):
    try:
      path = self.folder.get_current_path() + '/' + file_name
      if os.path.isdir(path):
        sublime.error_dialog('File "' +path + '" is directory; can not save')
        return None

      overwrite = not os.path.isfile(path) or (sublime.ok_cancel_dialog('File "' +
        path + '" exists; ' +'do you want to overwrite it?', 'OVERWRITE'))

      if not overwrite:
        return None

      os.rename(self.file_name, path)
    except Exception as error:
      sublime.error_message('Error while renaming file: {0}'.format(error))
      return None

    return path

class PromptRenameFileInList(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = quick_search.panels.get_current()
    file_list = panel.get_caller('file_list')
    if file_list == None:
      return

    RenameFile(panel.get_current_value()).show()

class RenameFileInListComplete(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = quick_search.panels.get_current()
    rename = panel.get_caller('rename')
    if rename == None:
      return

    panel.hide()
    new_path = rename.rename(panel.get_current_text())
    if new_path == None:
      panel.show()
      return

    panel.close(None, False)

class FileListHelper(sublime_plugin.TextCommand):
  def _get_panels(self):
    panel = quick_search.panels.get_current()
    file_list = panel and panel.get_caller('file_list')
    return panel, file_list

class OpenFileInList(FileListHelper):
  def run(self, edit):
    panel, file_list = self._get_panels()
    if file_list == None:
      return

    sublime.active_window().open_file(panel.get_current_value())

class PreviewFileInList(FileListHelper):
  def run(self, edit):
    panel, file_list = self._get_panels()
    if file_list == None:
      return

    sublime.active_window().open_file(panel.get_current_value(),
      sublime.TRANSIENT)
