import sublime, sublime_plugin
import os
from pathlib import Path

# TODO:
# * Settings for:
#     - Exclude extensions
#     - Set Max number of entries
#     - Make MRU behaves user wide (same as vim-mru)

# This setting affects the number of entries we *show* on the quick panel. It
# has no effect on the number of entries we store.
QUICK_PANEL_MAX_ENTRIES = 30
MRU_FILE_NAME = ".sublime-mru"
MSG_NO_MRU_FILES = "There are no recently used files."

class Mru():
    # Returns a list of key value pairs for each entry in the MRU file
    # where the *key* is the caption we use for the quick_panel and *value*
    # is the absolute file path that allows us to open the selected item.
    def describe_mru_files(self):
        if self.mru_file_exists():
            files_descriptions = []
            with open(self.mru_file_fullpath(), "r") as f:
                for line in f:
                    file_path = line.strip()
                    if file_path:
                        files_descriptions.append({
                            "file_description": self.describe_file(file_path),
                            "full_path": file_path
                        }
                    )
            return files_descriptions

    # Returns a list of MRU files paths.
    def read_mru_file(self):
        mru_files_paths = []
        if self.mru_file_exists():
            with open(self.mru_file_fullpath(), "r") as f:
                for line in f:
                    file_path = line.strip()
                    if file_path:
                        mru_files_paths.append(file_path)

        return mru_files_paths

    def update_mru_file(self, file_path):
        mru_files_paths = self.read_mru_file()

        if file_path in mru_files_paths:
            mru_files_paths.remove(file_path)

        mru_files_paths.insert(0, file_path)
        with open(self.mru_file_fullpath(), "w") as f:
            for file_path in mru_files_paths:
                if file_path:
                    f.write(file_path + os.linesep)

    # Returns a string in the form of:
    # foo.txt (/Users/jane/tmp/foo.txt)
    def describe_file(self, file_path):
        return os.path.basename(file_path) + " (" + file_path + ")"

    def mru_file_exists(self):
        full_path = self.mru_file_fullpath()
        if Path(full_path).is_file():
            return True

    def mru_file_fullpath(self):
        home = os.path.expanduser("~")
        return os.path.join(home, MRU_FILE_NAME)


class MruOnSave(sublime_plugin.EventListener, Mru):
    def on_activated_async(self, view):
        self.update_mru_file(view.file_name())


class MruClearCommand(sublime_plugin.WindowCommand, Mru):
    def run(self):
        os.remove(self.mru_file_fullpath())


# Shows most recently used files in the current project.
class MruCommand(sublime_plugin.WindowCommand, Mru):
    def run(self):
        files_descriptions = self.describe_current_project_mru_files()
        if files_descriptions:
            items = [x["file_description"] for x in files_descriptions]
            self.window.show_quick_panel(
                items=items[:QUICK_PANEL_MAX_ENTRIES],
                on_select=lambda idx: self.open_file(files_descriptions, idx))
        else:
            print(MSG_NO_MRU_FILES)

    def describe_current_project_mru_files(self):
        return [d for d in self.describe_mru_files() if self.is_current_project_file(d["full_path"])]

    def is_current_project_file(self, file_path):
        return self.current_project_path() in file_path

    def current_project_path(self):
        folders = self.window.folders()
        return folders[0] if len(folders) else ""

    def open_file(self, mru_files, idx):
        if idx >= 0:
            self.window.open_file(mru_files[idx]['full_path'])
