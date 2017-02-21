import sublime
import sublime_plugin
import string

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

amino_acids = ['CYS', 'ASP', 'SER', 'GLN', 'LYS', 'ILE', 'PRO', 'THR', 'PHE', 'ASN', 'GLY', 'HIS', 'LEU', 'ARG', 'TRP', 'ALA', 'VAL', 'GLU', 'TYR', 'MET']
def is_as_line(line):
	for a in amino_acids:
		if a in line:
			return True
	return False

class pdbfixchainidmonomer(sublime_plugin.TextCommand):
	def run(self, edit):
		for line in self.view.lines(sublime.Region(0, self.view.size())):
			text = self.view.substr(line)
			if not text.startswith("ATOM") and not text.startswith("HETATM"):
				continue
			is_as = is_as_line(text)	
			fixed = None
			if not is_as:
				fixed = text[0:21] + " " + text[22:] 
			else:
				fixed = text[0:21] + "A" + text[22:] 
			self.view.replace(edit, line, fixed)

def fix_chain_id(obj, edit, chains):
	atom_counter = 0
	for line in obj.view.lines(sublime.Region(0, obj.view.size())):
		text = obj.view.substr(line)
		if not text.startswith("ATOM") and not text.startswith("HETATM"):
			continue	
		if is_as_line(text):
			atom_counter += 1
	if atom_counter % chains != 0:
		return
	atoms_per_chain = atom_counter / chains
	chain_counter = 0
	atom_counter = 0
	for line in obj.view.lines(sublime.Region(0, obj.view.size())):
		text = obj.view.substr(line)
		if not text.startswith("ATOM") and not text.startswith("HETATM"):
			continue
		is_as = is_as_line(text)	
		fixed = None
		if not is_as:
			fixed = text[0:21] + " " + text[22:] 
		else:
			fixed = text[0:21] + string.ascii_uppercase[chain_counter] + text[22:] 
			atom_counter += 1
			if atom_counter == atoms_per_chain:
				chain_counter += 1
				atom_counter = 0
		obj.view.replace(edit, line, fixed)

class pdbfixchainiddimer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 2)


class pdbfixchainidtrimer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 3)


class pdbfixchainidtetramer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 4)



