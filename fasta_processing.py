from Bio import SeqIO
for RECORD in SeqIO.parse('gc_fasta.fa', 'fasta'):
	print("ID:", RECORD.id)
	print('Sequence:', RECORD.seq)

# Function to calculate GC content of a DNA sequence
def calculate_gc_content(sequence):
    """Calculate the percentage of G and C bases in a sequence."""
    gc_count = sequence.count("G") + sequence.count("C")  # Count G and C bases
    return (gc_count / len(sequence)) * 100 if sequence else 0  # Calculate percentage

# Function to read and process a FASTA file
def process_fasta(file_path):
    """Categorize sequences based on GC content and save them into separate files."""
    high_gc_file = "high_gc.fasta"  # File to store high GC content sequences
    low_gc_file = "low_gc.fasta"  # File to store low GC content sequences
    high_gc_sequences = []  # List to store sequences with high GC content
    low_gc_sequences = []  # List to store sequences with low GC content
    high_gc_ids = []  # List to store IDs of high GC sequences
    low_gc_ids = []  # List to store IDs of low GC sequences

    print("Starting to process sequences...")
    
    # Read each sequence from the FASTA file
    for record in SeqIO.parse(file_path, "fasta"):
        print(f"Processing sequence: {record.id}")  # Show which sequence is being processed
        gc_content = calculate_gc_content(str(record.seq))  # Compute GC content
        print(f"Processing {record.id}: GC Content = {gc_content:.2f}%")
        
        # Categorize based on GC content
        if gc_content > 40:
            high_gc_sequences.append(record)  # Add to high GC list
            high_gc_ids.append(record.id)  # Store ID of high GC sequence
        else:
            low_gc_sequences.append(record)  # Add to low GC list
            low_gc_ids.append(record.id)  # Store ID of low GC sequence
    
    # Save categorized sequences into respective files
    SeqIO.write(high_gc_sequences, high_gc_file, "fasta")
    SeqIO.write(low_gc_sequences, low_gc_file, "fasta")
    
    # Print categorized sequence IDs
    print("\nHigh GC content sequences:")
    for id in high_gc_ids:
        print(id)
    
    print("\nLow GC content sequences:")
    for id in low_gc_ids:
        print(id)
    
    print(f"\nSequences with >40% GC content saved to {high_gc_file}")
    print(f"Sequences with <=40% GC content saved to {low_gc_file}")
    print("\nWohooo!! Task completed successfully!")

# Run the script when executed
if __name__ == "__main__":
    fasta_file = "gc_fasta.fa"  # Name of the input FASTA file
    process_fasta(fasta_file)  # Process the file
