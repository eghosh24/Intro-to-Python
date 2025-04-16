
import argparse #To parse Command-line arguments
from Bio import SeqIO #For processing FASTA files

def parse_arguments():
    """Creating an argument parser and define the given three arguments."""
    parser = argparse.ArgumentParser(description="Filter sequences based on GC content and length.")
    parser.add_argument("--gc_threshold", type=float, default=25.5, help="GC content threshold (default: 25.5).")
    parser.add_argument("--length_threshold", type=int, default=80, help="Length threshold (default: 80).")
    parser.add_argument("--input_fasta", type=str, help="Input FASTA file.")
    return parser.parse_args()

def get_fasta_filename():
    """Prompting the user for a FASTA file."""
    file_name = input("Enter the FASTA file name: ")
    return file_name.strip()

def calculate_gc_content(sequence):
    """Calculating the GC content of a DNA sequence."""
    sequence = sequence.upper()  # Convert sequence to uppercase for consistency
    gc_count = sequence.count("G") + sequence.count("C")
    return (gc_count / len(sequence)) * 100 if len(sequence) > 0 else 0  # Avoid division by zero

def process_fasta(file_path, gc_threshold, length_threshold):
    """Processing the FASTA file and categorizing the sequences based on GC content and length."""
    low_gc_length_file = "low_gc_length.fasta"
    high_gc_length_file = "high_gc_length.fasta"
    intermediate_file = "intermediate.fasta"

    # Initializing lists to categorize sequences
    low_gc_length_seqs = []
    high_gc_length_seqs = []
    intermediate_seqs = []

    print(f"\nProcessing sequences from {file_path} with GC threshold = {gc_threshold}% and length threshold = {length_threshold}...\n")

    for record in SeqIO.parse(file_path, "fasta"): #reads sequence from the FASTA file
        sequence_str = str(record.seq) #converts the sequence to a string
        gc_content = calculate_gc_content(sequence_str) #Calculates GC content
        seq_length = len(sequence_str)  # Directly get length
		 #Categorizing the sequences
        if gc_content < gc_threshold and seq_length < length_threshold:
            low_gc_length_seqs.append(record)
        elif gc_content > gc_threshold and seq_length > length_threshold:
            high_gc_length_seqs.append(record)
        else:
            intermediate_seqs.append(record)

    # Writing categorized sequences to respective files
    SeqIO.write(low_gc_length_seqs, low_gc_length_file, "fasta")
    SeqIO.write(high_gc_length_seqs, high_gc_length_file, "fasta")
    SeqIO.write(intermediate_seqs, intermediate_file, "fasta")

	#displaying the Summary
    print(f"👍 Sequences with GC < {gc_threshold}% and length < {length_threshold} saved to: {low_gc_length_file}")
    print(f"👍 Sequences with GC > {gc_threshold}% and length > {length_threshold} saved to: {high_gc_length_file}")
    print(f"👍 Intermediate sequences saved to: {intermediate_file}\n")
    print("🎉 Task completed successfully!")

if __name__ == "__main__":
    args = parse_arguments()

    # If no input file is provided, prompt the user
    fasta_file = args.input_fasta if args.input_fasta else get_fasta_filename()

    process_fasta(fasta_file, args.gc_threshold, args.length_threshold)
