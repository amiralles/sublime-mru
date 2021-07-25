import sublime_plugin
import os
from pathlib import Path

class MruCommand(sublime_plugin.WindowCommand):
    def run(self):
        files_descriptions = self.describe_mru_files()
        if files_descriptions:
            self.window.show_quick_panel(
                items=[x["file_description"] for x in files_descriptions],
                on_select=lambda idx: self.open_file(files_descriptions, idx))
        else:
            print("There are no MRU files.")

    def open_file(self, mru_files, idx):
        if idx >= 0:
            self.window.open_file(mru_files[idx]['full_path'])

    # Returns a list of key value pairs for each entry in `.sublime-mru` file
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
        return os.path.join(home, ".sublime-mru")
