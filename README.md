# PDB_File_Manipulation
Scripts which offer different types of analysis and data manipulation of PDB files.
PDB_Atom_Numbering.py: Can be used via the command-line and as a module.

# Goal
PDB_Atom_Numbering.py: Numbers the atoms of all the atoms of the the PDB file or of a specific chain starting from a specific number. The atom numberings in CONNECT lines (if any) are not changed.

# Options
PDB_Atom_Numbering.py for command-line usage:
-i / --input: The file path of the input PDB file. Default: None
-c / --chain: The chain selected for atom numbering. Default: None (All atoms are renumbered.)
-n / --number: The starting number for the atom numbering. It cannot be negative nor above 99999. Default: 1
-o / --output: The path for the output file. Default: Input_File_Name (wihtout the PDB file extension) + "_Atom_Mod.pdb"

PDB_Atom_Numbering.py as a module:
atomnum(input, chain, number, output)
