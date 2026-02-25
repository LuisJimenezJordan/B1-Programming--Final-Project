# Biological reference data for DNA sequence analysis

# Standard codon table (DNA triplets -> Amino Acids)
Codon_Table = {
    # Phenylalanine
    "TTT": "Phe", "TTC": "Phe",
    # Leucine
    "TTA": "Leu", "TTG": "Leu", "CTT": "Leu", "CTC": "Leu", "CTA": "Leu", "CTG": "Leu",
    # Isoleucine
    "ATT": "Ile", "ATC": "Ile", "ATA": "Ile",
    # Methionine (Start)
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
    # Tryptophan
    "TGG": "Trp",
    # Arginine
    "CGT": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg", "AGA": "Arg", "AGG": "Arg",
    # Glycine
    "GGT": "Gly", "GGC": "Gly", "GGA": "Gly", "GGG": "Gly",
    # Stop codons
    "TAA": "Stop", "TAG": "Stop", "TGA": "Stop"
}

# Amino acid properties
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