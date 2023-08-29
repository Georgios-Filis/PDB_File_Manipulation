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
        output_path = "{}_Atom_Mod.pdb".format(input_path_mod)
        print("File output path: {}".format(output_path))

    if start_number < 0 or start_number > 99999:
        print("Starting number is negative or above 99999. Exiting.")
        exit()

    # A variable that holds the atom number.
    atom_num = start_number

    # Open the new file.
    new_file = open(output_path, "w")

    # Renumbers the atoms of all the atoms of the the PDB file or of a specific chain starting from a specific number.
    # The pattern to find the lines with atom numbers and the specified chain (if any) which will be changed.
    # The atom numberings in CONNECT lines (if any) do not change.
    if arg_chain is None:
        pattern_atom_1 = re.compile(r'^(ATOM|HETATM|ANISOU|TER)\s+\d+(.*)')
    else:
        pattern_atom_2 = re.compile(r'^(ATOM|HETATM|ANISOU)\s+\d+(\s+\S+\s+\S+\s+(\S+).*)')
        pattern_atom_3 = re.compile(r'^(TER)\s+\d+(\s+(\S+).*)')
    pdb_lines = read_file(input_path)
    for line in pdb_lines:
        if arg_chain is None:
            result_atom_nc = pattern_atom_1.search(line)
            if result_atom_nc:
                result_type = result_atom_nc.group(1)
                line_end_part = result_atom_nc.group(2)
                # Perform the change based on the starting atom number.
                # The first label takes 6 positions. The atom number takes 5 positions.
                if result_type == "ATOM":
                    phrase = "ATOM  "
                elif result_type == "HETATM":
                    phrase = "HETATM"
                elif result_type == "ANISOU":
                    phrase = "ANISOU"
                elif result_type == "TER":
                    phrase = "TER   "
                # If the current line is with teh ANISOU label then the atom number must remain the same as with the previous line,
                # therefore the atom number is decreased by one.
                if result_type == "ANISOU":
                    atom_num -= 1
                # The atom number is placed by starting from the right side.
                phrase = "{}{:>5}{}".format(phrase, atom_num, line_end_part)
                new_file.write("{}\n".format(phrase))
                atom_num += 1
            else:
                # For each line not catched by the pattern, it is written unchanged in the new file.
                new_file.write("{}\n".format(line))
        else:
            result_atom_c = None
            result_atom_2 = pattern_atom_2.search(line)
            result_atom_3 = pattern_atom_3.search(line)
            if result_atom_2:
                result_atom_c = result_atom_2
            elif result_atom_3:
                result_atom_c = result_atom_2
            else:
                # For each line not catched by the pattern, it is written unchanged in the new file.
                new_file.write("{}\n".format(line))
            if result_atom_c is not None:                
                result_atom_c = pattern_atom_2.search(line)
                result_type = result_atom_c.group(1)
                result_chain = result_atom_c.group(3)
                if result_chain == chain:
                    # Perform the change based on the starting atom number.
                    line_end_part = result_atom_c.group(2)
                    # Perform the change based on the starting atom number.
                    # The first label takes 6 positions. The atom number takes 5 positions.
                    if result_type == "ATOM":
                        phrase = "ATOM  "
                    elif result_type == "HETATM":
                        phrase = "HETATM"
                    elif result_type == "ANISOU":
                        phrase = "ANISOU"
                    elif result_type == "TER":
                        phrase = "TER   "
                    # If the current line is with teh ANISOU label then the atom number must remain the same as with the previous line,
                    # therefore the atom number is decreased by one.
                    if result_type == "ANISOU":
                        atom_num -= 1
                    # The atom number is placed by starting from the right side.
                    phrase = "{}{:>5}{}".format(phrase, atom_num, line_end_part)
                    new_file.write("{}\n".format(phrase))
                    atom_num += 1
                    print(line)
                else:
                    # If the line is catched by the pattern but not of the specified chain then it is written unchanged in
                    # the new file.
                    new_file.write("{}\n".format(line))

    # Close the new file.
    new_file.close()


if __name__ == "__main__":
    arg_input_path = None
    arg_chain = None
    arg_start_number = 1
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
