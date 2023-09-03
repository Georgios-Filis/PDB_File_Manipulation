import re
import sys


def read_file(file_path):
    file_handle = open(file_path, "r")
    pre_lines = file_handle.readlines()
    lines = []
    for i in pre_lines:
        i = i.rstrip("\n")
        lines.append(i)
    file_handle.close()
    return lines


def atomnum(input_path, chain, start_number, output_path):
    if input_path is None:
        print("No input file was given or input path is wrong. Exiting.")
        exit()
    
    if output_path is None:
        input_path_mod = input_path[:-4]
        output_path = "{}_Chain_Mod.pdb".format(input_path_mod)
        print("File output path: {}".format(output_path))

    if start_number < 0 or start_number > 99999:
        print("Starting number is negative or above 99999. Exiting.")
        exit()
    
	# If the start_number is anything else but the default value, then subtract one in the beginning to start numbering from the selected value of the user.
    if start_number != 0:
        start_number -= 1
            
    # A variable that holds the atom number.
    chain_num = start_number

    # Open the new file.
    new_file = open(output_path, "w")

	# Example from a PDB file:
	# ATOM      1  N   ALA A   1      13.172 -16.346  -1.789  0.00 26.27           N  
	# ATOM      2  CA  ALA A   1      13.663 -17.624  -2.403  0.00 26.40           C  
	# ATOM      3  C   ALA A   1      13.627 -17.432  -3.877  1.00 25.43           C  
    # Renumbers the atoms of all the atoms of the the PDB file or of a specific chain starting from a specific number.
    # The pattern to find the lines with atom numbers and the specified chain (if any) which will be changed.
    # The atom numberings in CONNECT lines (if any) do not change.
    pattern_info = re.compile(r'^(\S+\s+\d+(\s+\S+\s+|\s+)\S+\s+(\S+))\s+(\d+)(.*)')
    pdb_lines = read_file(input_path)
    chain_aa_combs_unique = []
    for line in pdb_lines:
        result_info = pattern_info.search(line)
        if result_info:
            line_start_part = result_info.group(1)
            chain_type = result_info.group(3)
            aa_num = result_info.group(4)
            line_end_part = result_info.group(5)
            chain_aa_comb = "{}_{}".format(chain_type, aa_num)
			# If a chain (chain type) is selected then renumber only the lines whose chain matches the selected chain.
            if chain is not None:
            	# If the current line does not contain information for the selected chain, then continue to the next line and write the current one unchanged in the new file.
                if chain != chain_type:
                    new_file.write("{}\n".format(line))
                    continue
            # If this combination of chain type (e.g., A, B, C) and residue number has not been found before in the lines, then add one to the counter used for numbering the residues.
            if chain_aa_comb not in chain_aa_combs_unique:
                chain_aa_combs_unique.append(chain_aa_comb)
                chain_num += 1				
            # The atom number is placed by starting from the right side.
            phrase = "{}{:>4}{}".format(line_start_part, chain_num, line_end_part)
            new_file.write("{}\n".format(phrase))
        else:
            # For each line not catched by the pattern, it is written unchanged in the new file.
            new_file.write("{}\n".format(line))
    # Close the new file.
    new_file.close()


if __name__ == "__main__":
    arg_input_path = None
    arg_chain = None
    arg_start_number = 0
    arg_output_path = None
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv), 2):
            if sys.argv[i] == "-i" or sys.argv[i] == "--input":
                arg_input_path = sys.argv[i+1]
            elif sys.argv[i] == "-c" or sys.argv[i] == "--chain":
                arg_chain = sys.argv[i+1]
            elif sys.argv[i] == "-n" or sys.argv[i] == "--number":
                arg_start_number = int(sys.argv[i+1])
            elif sys.argv[i] == "-o" or sys.argv[i] == "--output":
                arg_output_path = sys.argv[i+1]
    atomnum(arg_input_path, arg_chain, arg_start_number, arg_output_path)
