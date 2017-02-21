import sublime
import sublime_plugin


class pdbfixatomids(sublime_plugin.TextCommand):
	def run(self, edit):
		counter = 0
		for line in self.view.lines(sublime.Region(0, self.view.size())):
			text = self.view.substr(line)
			self.view.insert(edit, self.view.size(), "\n" + text)
import sublime
import sublime_plugin


class pdbfixatomids(sublime_plugin.TextCommand):
	def run(self, edit):
		# atom id in 6-10 
		counter = 1
		for line in self.view.lines(sublime.Region(0, self.view.size())):
			text = self.view.substr(line)
			if not text.startswith("ATOM") and not text.startswith("HETATM") and not text.startswith("TER"):
				continue
			fixed = text[0:6] + str(counter).rjust(5) + text[11:] 
			counter += 1
			self.view.replace(edit, line, fixed)
