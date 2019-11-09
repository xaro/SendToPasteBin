import os
import re
import sublime
import sublime_plugin
import sys
import threading

# Ensure it works for python 2 and 3
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import urlencode, urlopen

ROOT_URL = "https://pastebin.com"
API_URL = ROOT_URL + "/api/api_post.php"


class SendToPasteBinPromptCommand(sublime_plugin.WindowCommand):
    """Show a window to allow the user to setup the Paste options"""

    def run(self):
        self.window.show_input_panel(
            "Paste Name:", "", self.on_done, None, None)

    def on_done(self, paste_name):
        if self.window.active_view():
            self.window.active_view().run_command(
                "send_to_paste_bin", {"paste_name": paste_name})


class SendToPasteBinCommand(sublime_plugin.TextCommand):

    def run(self, view, paste_name=None):
        self.settings = sublime.load_settings(
            "SendToPasteBin.sublime-settings")

        # These are all the syntaxes supported by PasteBin currently (https://pastebin.com/api)
        syntaxes = {
            'ActionScript.sublime-syntax': 'actionscript',
            'AppleScript.sublime-syntax': 'applescript',
            'ASP.sublime-syntax': 'asp',
            'Bibtex.sublime-syntax': 'bibtex',
            'C.sublime-syntax': 'c',
            'C#.sublime-syntax': 'csharp',
            'C++.sublime-syntax': 'cpp',
            'Clojure.sublime-syntax': 'clojure',
            'CoffeeScript.sublime-syntax': 'coffeescript',
            'CSS.sublime-syntax': 'css',
            'D.sublime-syntax': 'd',
            'Diff.sublime-syntax': 'diff',
            'DOT.sublime-syntax': 'dot',
            'Erlang.sublime-syntax': 'erlang',
            'Go.sublime-syntax': 'go',
            'Groovy.sublime-syntax': 'groovy',
            'Haskell.sublime-syntax': 'haskell',
            'HTML.sublime-syntax': 'html5',
            'Java.sublime-syntax': 'java',
            'JavaScript.sublime-syntax': 'javascript',
            'JSON.sublime-syntax': 'javascript',
            'JSON Generic Array Elements.sublime-syntax': 'javascript',
            'LaTeX.sublime-syntax': 'latex',
            'LaTeX Beamer.sublime-syntax': 'latex',
            'LaTeX Memoir.sublime-syntax': 'latex',
            'Lisp.sublime-syntax': 'lisp',
            'Literate Haskell.sublime-syntax': 'haskell',
            'Lua.sublime-syntax': 'lua',
            'Makefile.sublime-syntax': 'make',
            'Matlab.sublime-syntax': 'matlab',
            'Objective-C.sublime-syntax': 'objc',
            'Objective-C++.sublime-syntax': 'objc',
            'OCaml.sublime-syntax': 'ocaml',
            'OCamllex.sublime-syntax': 'ocaml',
            'OCamlyacc.sublime-syntax': 'ocaml',
            'Perl.sublime-syntax': 'perl',
            'PHP.sublime-syntax': 'php',
            'Plain text.sublime-syntax': 'text',
            'Python.sublime-syntax': 'python',
            'R.sublime-syntax': 'rsplus',
            'R Console.sublime-syntax': 'rsplus',
            'Regular Expressions (Python).sublime-syntax': 'python',
            'Ruby.sublime-syntax': 'ruby',
            'Ruby Haml.sublime-syntax': 'ruby',
            'Ruby on Rails.sublime-syntax': 'rails',
            'Scala.sublime-syntax': 'scala',
            'SCSS.sublime-syntax': 'css',
            'Shell-Unix-Generic.sublime-syntax': 'bash',
            'SQL.sublime-syntax': 'sql',
            'SQL (Rails).sublime-syntax': 'sql',
            'Tcl.sublime-syntax': 'tcl',
            'TeX.sublime-syntax': 'latex',
            'TeX Math.sublime-syntax': 'latex',
            'Textile.sublime-syntax': 'latex',
            'XML.sublime-syntax': 'xml',
            'YAML.sublime-syntax': 'yaml'
        }

        # Use the filename as a default paste name
        if paste_name is None:
            paste_name = self.view.file_name()

            # Check if file exists on disk
            if paste_name is not None:
                # Only use the basename (we don't care about the path)
                paste_name = os.path.basename(paste_name)
            else:
                paste_name = "Untitled"

        # Manage the user selected text
        for region in self.view.sel():
            syntax = syntaxes.get(self.view.settings().get(
                'syntax').split('/')[-1], 'text')

            text = self.view.substr(region)

            if not text:
                sublime.status_message(
                    'Error sending to PasteBin: Nothing selected')
            else:
                args = {
                    'api_dev_key': self.settings.get("api_dev_key"),
                    'api_user_key': self.settings.get("api_user_key"),
                    'api_paste_expire_date': self.settings.get("paste_expiration"),
                    'api_paste_private': self.settings.get("paste_privacy"),
                    'api_paste_code': text,
                    'api_option': 'paste',
                    'api_paste_format': syntax,
                    'api_paste_name': paste_name
                }

                # Use a background thread to avoid freezing the main thread
                thread = PasteBinApiCall(args)
                thread.start()


class PasteBinApiCall(threading.Thread):
    """Manages the call to PasteBin's API.
    Used to be able to do the call in another thread."""

    def __init__(self, call_args):
        self.call_args = call_args
        threading.Thread.__init__(self)
        self.settings = sublime.load_settings(
            "SendToPasteBin.sublime-settings")

    def run(self):
        sublime.status_message('Sending to PasteBin ...')

        response = urlopen(
            url=API_URL,
            data=urlencode(self.call_args).encode('utf8')
        ).read().decode('utf8')

        url_regex = '(.*//pastebin\.com/)(.*$)'
        paste_key = re.match(url_regex, response, flags=re.IGNORECASE).group(2)

        if self.settings.get("paste_url_type") == "raw":
            response = ROOT_URL + "/raw/" + paste_key

        sublime.set_clipboard(response)
        sublime.status_message('PasteBin URL copied to clipboard: ' + response)
