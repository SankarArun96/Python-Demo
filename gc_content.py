from Bio import SeqIO          # toolbox that reads FASTA files
import pandas as pd            # toolbox that makes tables (like a spreadsheet)

# An empty list: our "notebook" where each sequence's result will be written
results = []

# Look at one DNA sequence at a time
for record in SeqIO.parse("seqs.fasta", "fasta"):

    name = record.id                      # the sequence's name
    dna = str(record.seq).upper()         # the letters, made capital (a -> A)

    # Count the letters (like counting coloured beads)
    g = dna.count("G")
    c = dna.count("C")
    a = dna.count("A")
    t = dna.count("T")

    # Only A, T, G, C are counted. Other letters (like N = "unknown") are ignored.
    total = a + t + g + c

    # Do the maths, but only if there is something to count
    if total == 0:
        gc_percent = None                 # None = "no answer possible"
    else:
        gc_percent = (g + c) / total * 100

    # Write one line in the notebook: name, length, GC%
    results.append([name, len(dna), gc_percent])

# Turn the notebook into a table with column names
table = pd.DataFrame(results, columns=["name", "Length", "gc_percent"])

# Show the table (rounded to 1 decimal place)
print(table.round(1))

# Save the table so you can open it in Excel
table.to_csv("gc_results.csv", index=False)
print("Saved to gc_results.csv")
