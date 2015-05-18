# Sublime FileList plugin

Library for displaying list of files.


### Demo

![Demo](https://github.com/shagabutdinov/sublime-enhanced-demos/raw/master/file_list.gif "Demo")


### WARNING

This plugin provides "rename file" functionality. If you enter rename mode you
should type new file name and hit "tab" (not "enter") for complete renaming.

### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Commands

All commands will works when file list is visible.

| Description                       | Keyboard shortcut |
|-----------------------------------|-------------------|
| Open file or folder               | ctrl+o            |
| Preview file                      | ctrl+p            |
| Delete file                       | ctrl+d            |
| Rename file                       | ctrl+r            |
| Complete file rename              | tab               |
| Insert short file name to view    | alt+p             |
| Insert relative file name to view | alt+shift+p       |
| Insert file name to view          | alt+ctrl+p        |
| Insert absolute file name to view | alt+ctrl+shift+p  |


### Dependencies

* [QuickSearchEnhanced](https://github.com/shagabutdinov/sublime-quick-search-enhanced)
* [FolderFiles](https://github.com/shagabutdinov/sublime-folder-files)


### API

FileList class methods:


##### __init__(callback, open = None, preview = None, text = None, open_if_one_file = True, callers = [], on_create = None)

Create file list.

Arguments:

  - `callback` - callback function that provides list of files; callback should
    receive no arguments;

  - `open` - open callback; if no open callback provided default open callback will
    be used

  - `preview` - preview callback; if no preview callback provided default preview
    callback will be used

  - `text` - initial text in panel

  - `open_if_one_file` - bool; if only one file found should be it opened right away
    or displayed in list

  - `callers` - callers stack; refer to [sublime-quick-search-enhanced](htt://github.com/shagabutdinov/sublime-quick-search-enhanced)
    for information

  - `on_create` - callback that will be executed after panel will be created showed


##### show()

Show created panel.


##### refresh()

Refresh file list


##### preview_file(panel)

Preview file from QuickSearch panel and return opened view.

Arguments:

  - `panel` - QuickSearch panel.

Result:

  A sublime view object that was created to show the file.