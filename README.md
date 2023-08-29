# PDB_File_Manipulation
Scripts which offer different types of analysis and data manipulation of PDB files.
PDB_Atom_Numbering.py: Can be used via the command-line and as a module.

# Goal
PDB_Atom_Numbering.py: Numbers the atoms of all the atoms of the the PDB file or of a specific chain starting from a specific number. The atom numberings in CONNECT lines (if any) are not changed.

# Options
## Command-line
PDB_Atom_Numbering.py:<br />
-i / --input: The file path of the input PDB file. Default: None<br />
-c / --chain: The chain selected for atom numbering. Default: None (All atoms are renumbered.)<br />
-n / --number: The starting number for the atom numbering. It cannot be negative nor above 99999. Default: 1<br />
-o / --output: The path for the output file. Default: Input_File_Name (wihtout the PDB file extension) + "_Atom_Mod.pdb" 

## Module
PDB_Atom_Numbering.py:<br />
atomnum(input, chain, number, output)<br />
