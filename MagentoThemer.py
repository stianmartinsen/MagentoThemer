import os
import re
import ntpath
import sublime, sublime_plugin

class MagentoThemer:
    AddContentView = None
    Content = None

class MagentoThemerInsertConentCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        self.view.insert(edit, 0, MagentoThemer.Content)

        MagentoThemer.AddContentView = None
        MagentoThemer.Content = None

class MagentoThemerListener(sublime_plugin.EventListener):
    def on_load(self, view):
        if MagentoThemer.AddContentView and MagentoThemer.AddContentView.id() == view.id():
            view.run_command("magento_themer_insert_conent")

class MagentoThemerCommand(sublime_plugin.WindowCommand):
    def run(self):
        project_name = self.window.project_file_name()
        project_name = ntpath.basename(project_name)
        project_name = re.sub('\.sublime-project$', '', project_name)
        self.window.show_input_panel("Give me: <interface name>/<theme name>:", "%s/default" % project_name, self.on_done, None, None)

    def on_done(self, text):
        # design/frontend/base/default/template/checkout/cart/item/default.phtml
        view = self.window.active_view()
        old_file = view.file_name()
        MagentoThemer.Content = view.substr(sublime.Region(0, view.size()))

        new_interface_name = text.split('/')[0]
        new_theme_name = text.split('/')[1]
        new_file = re.sub(r'([^$]*)/base/default/([^$]*)', r'\1/' + new_interface_name + '/' + new_theme_name + r'/\2', old_file)

        # Recursively create parent folder if it does not exist
        if not os.path.exists(os.path.dirname(new_file)):
            os.makedirs(os.path.dirname(new_file))

        # Open the file
        MagentoThemer.AddContentView = self.window.open_file(new_file)

        if os.path.exists(new_file):
            sublime.error_message('File already exists')