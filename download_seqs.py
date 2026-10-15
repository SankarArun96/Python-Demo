from Bio import Entrez         # toolbox that talks to NCBI (the big DNA database)

# ----- ASK THE USER FOR INPUTS ---------------------------------------------
print("=" * 60)
print("  NCBI sequence downloader")
print("=" * 60)
print("Press Enter to accept the default shown in [brackets].\n")

# 1. Email (NCBI asks for one so they can contact you if there is a problem)
print("1) Your email address (required by NCBI)")
print("   Example: jane.doe@gmail.com")
email = input("   Email: ").strip()
while "@" not in email:
    print("   That doesn't look like an email. Please try again.")
    email = input("   Email: ").strip()
Entrez.email = email

# 2. Keyword
print("\n2) Keyword to search for")
print("   Examples:  insulin")
print("              insulin AND human[Organism]")
print("              SARS-CoV-2 spike")
print("              16S ribosomal RNA AND Escherichia coli[Organism]")
keyword = input("   Keyword [insulin AND human[Organism]]: ").strip()
if keyword == "":
    keyword = "insulin AND human[Organism]"

# 3. How many sequences
print("\n3) How many sequences to download")
print("   Examples:  10  (quick test)   100  (default)   500")
how_many_text = input("   Number [100]: ").strip()
while how_many_text != "" and not how_many_text.isdigit():
    print("   Please type a whole number, like 100.")
    how_many_text = input("   Number [100]: ").strip()
how_many = 100 if how_many_text == "" else int(how_many_text)

# 4. Output file name
print("\n4) Name of the FASTA file to create")
print("   Examples:  seqs.fasta   insulin_human.fasta")
print("   (Keep 'seqs.fasta' if you want to use it with gc_content.py)")
output_file = input("   File name [seqs.fasta]: ").strip()
if output_file == "":
    output_file = "seqs.fasta"
if not output_file.lower().endswith((".fasta", ".fa")):
    output_file = output_file + ".fasta"
# ---------------------------------------------------------------------------

# Step 1: Search NCBI's nucleotide database and get a list of ID numbers
print("\nSearching NCBI for:", keyword)
search = Entrez.esearch(db="nucleotide", term=keyword, retmax=how_many)
search_results = Entrez.read(search)
search.close()

id_list = search_results["IdList"]        # the ID numbers found (like a list of library cards)
print("Found", search_results["Count"], "matches in total.")

if len(id_list) == 0:
    print("No sequences found. Try a different keyword.")
else:
    print("Downloading", len(id_list), "of them...")

    # Step 2: Use the ID numbers to download the actual sequences in FASTA format
    fetch = Entrez.efetch(db="nucleotide", id=id_list, rettype="fasta", retmode="text")
    fasta_text = fetch.read()
    fetch.close()

    # Step 3: Save everything into ONE fasta file
    with open(output_file, "w") as f:
        f.write(fasta_text)

    # Step 4: Check how many sequences were saved (each one starts with ">")
    saved = fasta_text.count(">")
    print("Saved", saved, "sequences to", output_file)
