# Sublime MRU
Vim's MRU inspired plugin for Sublime Text.

It allows you to open (or activate) any **recently used file** in the current project.

The advantage of using this plugin over the standard Sublime's menus, is that it provides 
_**a unified list of currently open and recently closed files**_. If you are switching 
from vim and missing the [MRU](https://github.com/yegappan/mru) plugin, you may want to give this package a try.

https://user-images.githubusercontent.com/2120820/127004743-e27bd9af-57f1-4352-b26d-2e0c02993350.mp4

### Installation
At the moment, there is no "official" packge to install this plugin, but you can still uset it by copying `mru.py` into `<Sublime's Installation Path>/Packages/User`.

Once you did that, just add a shortcut to run the `mru` command and trigger the autocomplete list. For instance:

```json
{ "keys": ["ctrl+,"], "command": "save"}
```

## TODO
Create a package so that it's easier to install.
