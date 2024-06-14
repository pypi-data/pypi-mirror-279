from rxnSMILES4AtomEco import parse_smiles_with_coefficients, calculate_atom_economy, get_atom_economy, main, atom_economy

atom_economy("C.O>catalyst>{3}[HH]")
input()
m = get_atom_economy("C.O>catalyst>{3}[HH]")
print(m)