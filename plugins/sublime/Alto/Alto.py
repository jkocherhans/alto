import sublime
import sublime_plugin
import webbrowser

settings = sublime.load_settings('Alto.sublime-settings')

class AltoOpenCommand(sublime_plugin.TextCommand):
    def get_view_name(self):
        previous_view_name = ''
        selection = self.view.sel()[0]
        selector = 'entity.name.function'
        for region in self.view.find_by_selector(selector):
            if region.a > selection.a:
                return previous_view_name
            previous_view_name = self.view.substr(region)
        return previous_view_name

    def run(self, edit):
        url = settings.get('url')
        view_name = self.get_view_name()
        if view_name:
            url += '?q={0}'.format(view_name)
        webbrowser.open(url)
