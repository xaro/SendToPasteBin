import sublime, sublime_plugin
from urllib import urlencode, urlopen

class UploadPasteCommand( sublime_plugin.TextCommand ):
	def run(self, view):
		url = "http://pastebin.com/api/api_post.php"	

		for region in self.view.sel():

			args = {
				'api_dev_key': '9defe36b1e886d4c35f7e6383095ac1e',
				'api_paste_code': self.view.substr(region),
				'api_paste_private': '0',
				'api_option': 'paste'
			}

			response = urlopen(url=url, data=urlencode(args)).read()

			sublime.set_clipboard(response)
			sublime.status_message(response)