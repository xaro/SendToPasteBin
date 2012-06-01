import sublime, sublime_plugin
from urllib import urlencode, urlopen

PASTEBIN_URL = "http://pastebin.com/api/api_post.php"	

class SendToPasteBinPromptCommand( sublime_plugin.WindowCommand):
	
	def run(self):
		self.window.show_input_panel("Paste Name:", "", self.on_done, None, None)

	def on_done(self, paste_name):
		if self.window.active_view():
			self.window.active_view().run_command("send_to_paste_bin", {"paste_name": paste_name} )


class SendToPasteBinCommand( sublime_plugin.TextCommand ):

	def run(self, view, paste_name = None):
		syntaxes = {
			'ActionScript.tmLanguage': 'actionscript',
			'AppleScript.tmLanguage': 'applescript',
			'ASP.tmLanguage': 'asp',
			'Bibtex.tmLanguage': 'bibtex',
			'C.tmLanguage': 'c',
			'C#.tmLanguage': 'csharp',
			'C++.tmLanguage': 'cpp',
			'Clojure.tmLanguage': 'clojure',
			'CoffeeScript.tmLanguage': 'coffeescript',
			'CSS.tmLanguage': 'css',
			'D.tmLanguage': 'd',
			'Diff.tmLanguage': 'diff',
			'DOT.tmLanguage': 'dot',
			'Erlang.tmLanguage': 'erlang',
			'Go.tmLanguage': 'go',
			'Groovy.tmLanguage': 'groovy',
			'Haskell.tmLanguage': 'haskell',
			'HTML.tmLanguage': 'html5',
			'Java.tmLanguage': 'java',
			'JavaScript.tmLanguage': 'javascript',
			'JSON.tmLanguage': 'javascript',
			'JSON Generic Array Elements.tmLanguage': 'javascript',
			'LaTeX.tmLanguage': 'latex',
			'LaTeX Beamer.tmLanguage': 'latex',
			'LaTeX Memoir.tmLanguage': 'latex',
			'Lisp.tmLanguage': 'lisp',
			'Literate Haskell.tmLanguage': 'haskell',
			'Lua.tmLanguage': 'lua',
			'Makefile.tmLanguage': 'make',
			'Matlab.tmLanguage': 'matlab',
			'Objective-C.tmLanguage': 'objc',
			'Objective-C++.tmLanguage': 'objc',
			'OCaml.tmLanguage': 'ocaml',
			'OCamllex.tmLanguage': 'ocaml',
			'OCamlyacc.tmLanguage': 'ocaml',
			'Perl.tmLanguage': 'perl',
			'PHP.tmLanguage': 'php',
			'Plain text.tmLanguage': 'text',
			'Python.tmLanguage': 'python',
			'R.tmLanguage': 'rsplus',
			'R Console.tmLanguage': 'rsplus',
			'Regular Expressions (Python).tmLanguage': 'python',
			'Ruby.tmLanguage': 'ruby',
			'Ruby Haml.tmLanguage': 'ruby',
			'Ruby on Rails.tmLanguage': 'rails',
			'Scala.tmLanguage': 'scala',
			'SCSS.tmLanguage': 'css',
			'Shell-Unix-Generic.tmLanguage': 'bash',
			'SQL.tmLanguage': 'sql',
			'SQL (Rails).tmLanguage': 'sql',
			'Tcl.tmLanguage': 'tcl',
			'TeX.tmLanguage': 'latex',
			'TeX Math.tmLanguage': 'latex',
			'Textile.tmLanguage': 'latex',
			'XML.tmLanguage': 'xml',
			'YAML.tmLanguage': 'yaml'
		}

		if paste_name is None:
			paste_name = self.view.file_name()				# Get full file name (Path + Base Name)

			if paste_name is not  None: 					# Check if file exists on disk
				paste_name = 	os.path.basename(paste_name)	# Extract base name
			else:
				paste_name = "Untitled"

		for region in self.view.sel():

			syntax = syntaxes.get(self.view.settings().get('syntax').split('/')[-1], 'text')

			text = self.view.substr(region).encode('utf8')

			if not text:
				sublime.status_message('Error sending to PasteBin: Nothing selected')
			else:
				args = {
					'api_dev_key': '9defe36b1e886d4c35f7e6383095ac1e',
					'api_paste_code': text,
					'api_paste_private': '0',
					'api_option': 'paste',
					'api_paste_format': syntax,
					'api_paste_name': paste_name
				}

				response = urlopen(url=PASTEBIN_URL, data=urlencode(args)).read()

				sublime.set_clipboard(response)
				sublime.status_message('PasteBin URL copied to clipboard: ' + response)
