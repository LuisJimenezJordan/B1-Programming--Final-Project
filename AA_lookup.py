# AA_lookup.py
# Biological reference data used for DNA sequence analysis.
# Contains the standard genetic codon table and amino acid chemical property mappings.
# These are imported by analysis.py to perform amino acid translation and composition analysis.


# --- Codon Table ---
# Maps every possible DNA triplet (codon) to its corresponding amino acid using the
# standard genetic code. There are 64 possible codons (4 bases × 4 × 4), covering
# all 20 amino acids plus 3 stop codons.
# Amino acids are represented using standard 3-letter abbreviations (e.g. "Phe" for
# Phenylalanine). Stop codons signal the end of translation and produce no amino acid.
Codon_Table = {
    # Phenylalanine
    "TTT": "Phe", "TTC": "Phe",
    # Leucine — most codons of any amino acid (6 total)
    "TTA": "Leu", "TTG": "Leu", "CTT": "Leu", "CTC": "Leu", "CTA": "Leu", "CTG": "Leu",
    # Isoleucine
    "ATT": "Ile", "ATC": "Ile", "ATA": "Ile",
    # Methionine — also serves as the universal start codon (ATG)
    "ATG": "Met",
    # Valine
    "GTT": "Val", "GTC": "Val", "GTA": "Val", "GTG": "Val",
    # Serine
    "TCT": "Ser", "TCC": "Ser", "TCA": "Ser", "TCG": "Ser", "AGT": "Ser", "AGC": "Ser",
    # Proline
    "CCT": "Pro", "CCC": "Pro", "CCA": "Pro", "CCG": "Pro",
    # Threonine
    "ACT": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    # Alanine
    "GCT": "Ala", "GCC": "Ala", "GCA": "Ala", "GCG": "Ala",
    # Tyrosine
    "TAT": "Tyr", "TAC": "Tyr",
    # Histidine
    "CAT": "His", "CAC": "His",
    # Glutamine
    "CAA": "Gln", "CAG": "Gln",
    # Asparagine
    "AAT": "Asn", "AAC": "Asn",
    # Lysine
    "AAA": "Lys", "AAG": "Lys",
    # Aspartate
    "GAT": "Asp", "GAC": "Asp",
    # Glutamate
    "GAA": "Glu", "GAG": "Glu",
    # Cysteine
    "TGT": "Cys", "TGC": "Cys",
    # Tryptophan — only one codon, least redundant amino acid
    "TGG": "Trp",
    # Arginine
    "CGT": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg", "AGA": "Arg", "AGG": "Arg",
    # Glycine
    "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
    # Stop codons — signal end of translation, produce no amino acid
    "TAA": "Stop", "TAG": "Stop", "TGA": "Stop"
}


# --- Amino Acid Properties ---
# Maps each amino acid (3-letter code) to its chemical property classification.
# These properties describe the behaviour of the amino acid's side chain (R group)
# and are used in the amino acid analysis endpoint to calculate the overall
# chemical composition of a translated protein sequence.
#
# Property categories:
#   nonpolar          — hydrophobic, tend to cluster in protein interiors
#   polar             — hydrophilic, often found on protein surfaces
#   positively charged — carry a positive charge at physiological pH (basic)
#   negatively charged — carry a negative charge at physiological pH (acidic)
AA_Properties = {
    "Ala": "nonpolar",
    "Arg": "positively charged",
    "Asn": "polar",
    "Asp": "negatively charged",
    "Cys": "polar",
    "Gln": "polar",
    "Glu": "negatively charged",
    "Gly": "nonpolar",
    "His": "positively charged",
    "Ile": "nonpolar",
    "Leu": "nonpolar",
    "Lys": "positively charged",
    "Met": "nonpolar",
    "Phe": "nonpolar",
    "Pro": "nonpolar",
    "Ser": "polar",
    "Thr": "polar",
    "Trp": "nonpolar",
    "Tyr": "polar",
    "Val": "nonpolar"
}