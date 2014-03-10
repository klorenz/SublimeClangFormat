import sublime, sublime_plugin, subprocess

def clang_format(text, settings):
	cmd = settings.get('clang_format_command', 'clang-format-3.3')

	p = subprocess.Popen([cmd] + settings.get('clang_format_options',[]),
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE
		)
	return p.communicate(text.encode('utf-8'))[0].decode('utf-8')

class ClangFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		did_format = False
		settings = self.view.settings()

		for sel in self.view.sel():
			if sel.begin() >= sel.end(): continue

			text = self.view.substr(sel)
			self.view.replace(edit, sel, clang_format(text, settings))
			did_format = True

		if not did_format:
			all = sublime.Region(0, self.view.size())
			text = self.view.substr(all)
			self.view.replace(edit, all, clang_format(text, settings))

