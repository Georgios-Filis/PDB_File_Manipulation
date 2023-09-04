# PDB_File_Manipulation
Scripts which offer different types of analysis and data manipulation of PDB files. They can be used via the command-line or as a modules.

# Goal
PDB_Atom_Numbering.py:<br />
Numbers the atoms of all the chains of the the PDB file or of a specific chain starting from a specific number. The atom numberings in CONNECT lines (if any) are not changed.<br />

PDB_Chain_Numbering.py:<br />
Numbers the residues of all the chains of the the PDB file or of a specific chain starting from a specific number.

# Options
All scripts have been tested with Python 3.9.7.

## Command-line
PDB_Atom_Numbering.py:<br />
-i / --input: The file path of the input PDB file. Default: None<br />
-c / --chain: The chain selected for atom numbering. Default: None (All atoms are renumbered.)<br />
-n / --number: The starting number for the atom numbering. It cannot be negative nor above 99999. Default: 1<br />
-o / --output: The path for the output file. Default: Input_File_Name (wihtout the PDB file extension) + "_Atom_Mod.pdb" 

PDB_Chain_Numbering.py:<br />
-i / --input: The file path of the input PDB file. Default: None<br />
-c / --chain: The chain selected for residue numbering. Default: None (All residues are renumbered.)<br />
-mc / --missing-chains: If set to True, it means that the input file is missing chain IDs. Default: False<br />
-n / --number: The starting number for the residue numbering. It cannot be negative nor above 9999. Default: 1<br />
-o / --output: The path for the output file. Default: Input_File_Name (wihtout the PDB file extension) + "_Chain_Mod.pdb" 

## Module
PDB_Atom_Numbering.py:<br />
atomnum(input, chain, number, output)<br />

PDB_Chain_Numbering.py:<br />
chainnum(input, chain, number, output)<br />
