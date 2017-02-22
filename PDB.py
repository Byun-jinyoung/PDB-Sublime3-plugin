import sublime
import sublime_plugin
import string

amino_acids = ['CYS', 'ASP', 'SER', 'GLN', 'LYS', 'ILE', 'PRO', 'THR', 'PHE',
'ASN', 'GLY', 'HIS', 'LEU', 'ARG', 'TRP', 'ALA', 'VAL', 'GLU', 'TYR', 'MET']

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

def is_amino_acid_entry(line):
	for a in amino_acids:
		if a in line:
			return True
	return False

class pdbfixchainidmonomer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 1)

def fix_chain_id(obj, edit, chains):
	atom_counter = 0
	for line in obj.view.lines(sublime.Region(0, obj.view.size())):
		text = obj.view.substr(line)
		if not text.startswith("ATOM") and not text.startswith("HETATM"):
			continue	
		if is_amino_acid_entry(text):
			atom_counter += 1
	if atom_counter % chains != 0:
		print("Number of atoms not divideable by %s" % chains)
		return
	atoms_per_chain = atom_counter / chains
	chain_counter = 0
	atom_counter = 0
	for line in obj.view.lines(sublime.Region(0, obj.view.size())):
		text = obj.view.substr(line)
		if not text.startswith("ATOM") and not text.startswith("HETATM"):
			continue
		is_as = is_amino_acid_entry(text)	
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


class pdbfixchainid(sublime_plugin.TextCommand):
	def run(self, edit):
		old_resid = None
		chain_counter = -1
		for line in self.view.lines(sublime.Region(0, self.view.size())):
			text = self.view.substr(line)
			if text.startswith("ATOM") or text.startswith("HETATM"):
				is_as = is_amino_acid_entry(text)
				
				chainid = text[21:22]
				if is_as:
					resid = int(text[23:26])
					if old_resid == None or resid < old_resid:
						chain_counter += 1
					if chainid != string.ascii_uppercase[chain_counter]:
						fixed = text[0:21] + string.ascii_uppercase[chain_counter] + text[22:]
						self.view.replace(edit, line, fixed)
						old_resid = resid
				elif chainid != " ":
					fixed = text[0:21] + " " + text[22:]
					self.view.replace(edit, line, fixed)		
			


class pdbfixchainiddimer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 2)


class pdbfixchainidtrimer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 3)


class pdbfixchainidtetramer(sublime_plugin.TextCommand):
	def run(self, edit):
		fix_chain_id(self, edit, 4)



