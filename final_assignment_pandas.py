import pandas as pd #Structured data processing
import glob #To find all .out files
import os #for file path manipulation and checking directory validity

def process_te_files(input_dir, output_file): #function to process Te_files
    summary_rows = [] #build a list of dictionary, each summarizing one.out file 

    # Get and sort all .out files in the input directory
    files = sorted(glob.glob(os.path.join(input_dir, "*.out")))

    if not files: #If argument to exit early if no files found
        print(f"No .out files found in {input_dir}")
        return

    for filepath in files:
        species_id = os.path.splitext(os.path.basename(filepath))[0] #Get species/sample identifier from the file name

        columns = [
            "Score", "Pct_div", "Pct_del", "Pct_ins", "Query",
            "Start_in_query", "End_in_query", "(left_in_scaffold)",
            "Orientation", "TE_ID", "Class/Family", "Start_in_TE",
            "End_in_TE", "(left_in_TE)", "RM_ID"
        ] #Renamed the columns

        try: #to load the file with pandas
            df = pd.read_csv(filepath, sep=r'\s+', names=columns, skiprows=3, engine='python')
        except Exception as e: #Handles corrupted or improperly formatted files
            print(f"Error reading {filepath}: {e}")
            continue

        # Ensure column is string before splitting
        df["Class/Family"] = df["Class/Family"].astype(str) 

        # Split Class and Family
        split_cols = df["Class/Family"].str.split("/", n=1, expand=True)
        df["Class"] = split_cols[0]

        if split_cols.shape[1] > 1:
            df["Family"] = split_cols[1].fillna("Unknown") #
        else:
            df["Family"] = "Unknown" #handles missing family name

        row = {"Species_ID": species_id} #initialize summary row for the file
        te_classes = ["LINE", "SINE", "LTR", "DNA", "RC"] #count occurrences of each TE class

        for te_class in te_classes:
            class_df = df[df["Class"] == te_class]
            row[f"{te_class}_counts"] = class_df.shape[0] #.shape[0] to count rows and .mean for average
            row[f"{te_class}_div"] = round(class_df["Pct_div"].mean(), 2) if not class_df.empty else 0.0 #compute avg % divergence as proxy for TE age

        summary_rows.append(row) #stores the result

    summary_df = pd.DataFrame(summary_rows) #after the loop, constructs final dataframe

    # Fill in missing columns (for classes absent in some species): Ensures all columns exist in final table
    all_columns = ["Species_ID"]
    for cls in ["LINE", "SINE", "LTR", "DNA", "RC"]:
        all_columns.extend([f"{cls}_counts", f"{cls}_div"])

    for col in all_columns:
        if col not in summary_df.columns:
            summary_df[col] = 0

    summary_df = summary_df[all_columns]
    summary_df = summary_df.sort_values("Species_ID") #reorder columns and sort rows (clean and consistent output)

    summary_df.to_csv(output_file, index=False)
    print(f"\n✅ Summary saved to: {output_file}") #export to .CSV


# ======== Entry point ========
if __name__ == "__main__":
    print("=== TE Summary Generator ===") #ensures the code runs when the script is executed directly not when imported as a module

    # Ask user for input directory
    input_directory = input("Enter the path to the directory containing .csv files: ").strip()
    while not os.path.isdir(input_directory):
        print("❌ That path does not exist or is not a directory.")
        input_directory = input("Please enter a valid directory path: ").strip()

    # Ask user for output file name
    output_csv = input("Enter the desired name for the output CSV file (e.g., summary.csv): ").strip()
    if not output_csv.endswith(".csv"):
        output_csv += ".csv"

    # Run the processing function
    process_te_files(input_directory, output_csv)
