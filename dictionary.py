# dictionary.py
# Create an empty dictionary
Gene_Dict = {}

# Initiate a while loop to allow for entering multiple inputs to the dictionary
while True:
    # Generate an input request to ask for a gene name
    gene_name = input("Enter a gene name (or type 'exit' to stop): ")    
    
    # Adding a condition to exit the loop
    if gene_name.lower() == 'exit':
    	break # Stop the loop if the user types 'exit'

    # Ask for additional information on the gene that has been input
    gene_info = input("Enter information for {gene_name}: ")

    # Add the new pair to the dictionary
    Gene_Dict[gene_name] = gene_info

    # Print the dictionary and the information it contains
    print("\nGene Dictionary:")
    print(Gene_Dict)
    print("\nThis dictionary contains names of the gene as keys and their associated information as values.")
