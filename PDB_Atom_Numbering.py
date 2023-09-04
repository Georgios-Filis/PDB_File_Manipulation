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


def chainnum(input_path, chain, start_number, output_path):
    if input_path is None:
        print("No input file was given or input path is wrong. Exiting.")
        exit()
    
    if output_path is None:
        input_path_mod = input_path[:-4]
        output_path = "{}_Atom_Mod.pdb".format(input_path_mod)
        print("File output path: {}".format(output_path))

    if start_number < 0 or start_number > 9999:
        print("Starting number is negative or above 99999. Exiting.")
        exit()
    
	# If the start_number is anything else but the default value, then subtract one in the beginning to start numbering from the selected value of the user.
    if start_number != 0:
        start_number -= 1
            
    # A variable that holds the atom number.
    atom_num_counter = start_number

    # Open the new file.
    new_file = open(output_path, "w")

    # Atomic Coordinate Entry Format Description Version 3.30
    # Columns:
    # 1 - 6  : Record name "ATOM "/"ANISOU"/"HETATM"
    # 7 - 11 : Integer serial
    # 13 - 16: Atom name
    # 17     : Character altLoc
    # 18 - 20: Residue name resName
    # 22     : Character chainID
    # 23 - 26: Integer resSeq
    # 27     : AChar iCode
    # ...
    # The rest of the lines are not of use for the purposes of this script.
    #
    # TER:
    # Columns:
    # 1 - 6  : Record name "ATOM "/"ANISOU"/"TER   "
    # 7 - 11 : Integer serial
    # 18 - 20: Residue name resName
    # 22     : Character chainID
    # 23 - 26: Integer resSeq
    # 27     : AChar iCode
    # ...
    # The rest of the lines are not of use for the purposes of this script.
	# Example from a PDB file:
    # Not missing chains:
	# ATOM      1  N   ALA A   1      13.172 -16.346  -1.789  0.00 26.27           N  
	# ATOM      2  CA  ALA A   1      13.663 -17.624  -2.403  0.00 26.40           C  
	# ATOM      3  C   ALA A   1      13.627 -17.432  -3.877  1.00 25.43           C  
    # TER       3      ALA A   1
    # Missing chains:
    # ATOM      1  N   THR     1      15.100  17.240  18.900  1.00  0.00           N
    # ATOM      2  H   THR     1      15.040  17.240  17.900  1.00  0.00           H
    # ATOM      3  CA  THR     1      14.870  18.580  19.440  1.00  0.00           C
    # TER       3      THR     1
    #
    # Find the unique combinations of chain IDs and residue numbers.
    # Correspond them to the new residues numbers.
    # If a combination is found again use the correspondance to find its residue number.
    pdb_lines = read_file(input_path)
    for line in pdb_lines:
        line_type = line[:6]
        line_type_nes = line_type.strip()
        if line_type_nes in ["ATOM", "HETATM", "ANISOU"]:
            chain_id = line[21]
            first_part = line[:6]
            last_part = line[11:]
            chain_id_nes = chain_id.strip()
            # If a chain ID has been selected check whether this chain ID is the chain of the current line.
            if chain is not None:
                # If the line is at another chain of the one selected then continue and write this line unchanged.
                if chain != chain_id_nes:
                    new_line = "{}\n".format(line)
                    new_file.write(new_line)
                    continue
            if line_type_nes != "ANISOU":
                atom_num_counter += 1
            new_line = "{}{:>5}{}\n".format(first_part, atom_num_counter, last_part)
            new_file.write(new_line)
        elif line_type_nes == "TER":
            if line[:21]:
                chain_id = line[21]
                first_part = line[:6]
                last_part = line[11:]
                chain_id_nes = chain_id.strip()
                # If a chain ID has been selected check whether this chain ID is the chain of the current line.
                if chain is not None:
                    # If the line is at another chain of the one selected then continue and write this line unchanged.
                    if chain != chain_id_nes:
                        new_line = "{}\n".format(line)
                        new_file.write(new_line)
                        continue
                if line_type_nes != "ANISOU":
                    atom_num_counter += 1
                new_line = "{}{:>5}{}\n".format(first_part, atom_num_counter, last_part)
                new_file.write(new_line)
            else:
                print("TER line information not found.")
        else:
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
    chainnum(arg_input_path, arg_chain, arg_start_number, arg_output_path)
