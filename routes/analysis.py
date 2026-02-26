# analysis.py
# Contains all endpoints related to biological analysis of stored DNA sequences,
# including nucleotide analysis, amino acid conversion, and summary statistics.

from fastapi import APIRouter, HTTPException
from schema import NucleotideResult, AminoAcidResult, SummaryStats
from storage import load_sequences, save_sequences
from AA_lookup import AA_Properties, Codon_Table
from statistics import mean

router = APIRouter()

# --- Helper Function ---
# Calculates GC content (proportion of G and C bases) and total length of a sequence.
# GC content is biologically significant as it affects thermal stability and primer design.
def calculate_gc(sequence: str) -> float:
     sequence = sequence.upper()
     seq_length = len(sequence)
     gc_content = round((sequence.count("G") + sequence.count("C")) / seq_length, 4)
     return gc_content, seq_length


# --- Nucleotide Analysis Endpoint ---
# Loads all sequences, finds the one matching the given ID, calculates its GC content
# and length, updates the record in storage, and returns the results.
# Sets nuc_analysed to True so the sequence can be filtered and counted in summary stats.
@router.get("/{id}/nucleotide", response_model=NucleotideResult)
def nucleotide_analysis(id: int):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            gc_content, seq_length = calculate_gc(sequence["sequence"])
            sequence["gc_content"] = gc_content
            sequence["seq_length"] = seq_length
            sequence["nuc_analysed"] = True
            save_sequences(all_sequences)
            
            return {
                "message": f"DNA Nucleotide sequence with ID:{id} successfully analysed. See below the length of the sequence and its total GC content, which can be used to design primer melting and annealing temperatures",
                "sequence_id": id,
                "label": sequence["label"],
                "length": seq_length,
                "gc_content": gc_content
            }
    # Raised if no sequence with the given ID exists
    raise HTTPException(status_code=404, detail=f"Analysis could not be performed on sequence ID:{id}: ID not found")


# --- Amino Acid Analysis Endpoint ---
# Translates a DNA sequence into its amino acid sequence using the standard codon table.
# Codons are read in triplets; translation stops at a Stop codon or incomplete codon.
# Calculates amino acid composition by property type and identifies the top 3 most
# frequent residues. Updates the record in storage and sets aa_analysed to True.
@router.get("/{id}/aminoacid", response_model=AminoAcidResult)
def aminoacid_analysis(id: int):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            amino_acids = []
            dna_str = sequence["sequence"].upper()

            # Converts the DNA nucleotide sequence into an amino acid sequence
            # by reading codons (triplets of bases) and looking them up in the codon table
            for i in range(0, len(dna_str), 3):
                codon = dna_str[i:i+3]
                if len(codon) < 3:  # Ignore incomplete codons at the end
                    break
                amino_acid = Codon_Table.get(codon, "Unknown")
                if amino_acid == "Stop":  # Stop codon terminates translation
                    break
                amino_acids.append(amino_acid)
            
            # If translation produced no amino acids (e.g. sequence starts with a stop codon)
            if len(amino_acids) < 1:
                raise HTTPException(status_code=400, detail=f"Nucleotide sequence ID:{id} consisted only of a STOP codon. Therefore, conversion to Amino Acids produced no viable sequence.")

            # Determines the chemical property of each amino acid and counts
            # how many of each property type appear in the sequence
            composition = {}
            for amino_acid in amino_acids:
                aa_property = AA_Properties.get(amino_acid, "Unknown")
                composition[aa_property] = composition.get(aa_property, 0) + 1
            
            # Counts occurrences of each individual amino acid residue
            residue_counts = {}
            for amino_acid in amino_acids:
                residue_counts[amino_acid] = residue_counts.get(amino_acid, 0) + 1
            
            # Converts raw counts to percentages of the total sequence length
            residue_percentages = {}   
            for aa, count in residue_counts.items():
                residue_percentages[aa] = round((count / len(amino_acids)) * 100, 2)
            
            # Sorts by percentage descending and takes the top 3 most common residues
            top_3_residues = sorted(residue_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
            top_3_residues = [{"residue": aa, "percentage": pct} for aa, pct in top_3_residues]

            # Saves analysis results back to storage and marks sequence as AA analysed
            sequence["amino_acid_sequence"] = "-".join(amino_acids)
            sequence["residue_count"] = len(amino_acids)
            sequence["composition"] = composition
            sequence["top_3_residues"] = top_3_residues
            sequence["aa_analysed"] = True
            save_sequences(all_sequences)

            return {
                "message": f"DNA Nucleotide conversion to Amino Acid sequence with ID:{id} successfully completed. See below the converted sequence, the Amino Acid sequence length, the proportion of the different types of Amino Acid properties present in the sequence, and the top 3 most common Amino Acid Residues.",
                "sequence_id": id,
                "label": sequence["label"],
                "amino_acid_sequence": "-".join(amino_acids),
                "residue_count": len(amino_acids),
                "composition": composition,
                "top_3_residues": top_3_residues
            }
    # Raised if no sequence with the given ID exists
    raise HTTPException(status_code=404, detail=f"DNA to Amino Acid sequence conversion could not be performed on sequence ID:{id}: ID not found")


# --- Summary Statistics Endpoint ---
# Aggregates statistics across all stored sequences.
# Nucleotide stats (GC content, length, longest/shortest) are calculated only from
# sequences that have undergone nucleotide analysis.
# Amino acid stats are calculated only from sequences that have undergone AA analysis.
# If no AA analysis has been performed, average_amino_acid_length returns as null.
@router.get("/summary_statistics", response_model=SummaryStats)
def summary_analysis():
    all_sequences = load_sequences()

    # Raised if the toolkit has no sequences stored at all
    if len(all_sequences) == 0:
        raise HTTPException(status_code=404, detail="Summary statistics cannot be calculated: No nucleotide sequences have been submitted to DNA Toolkit.")

    # Filter to only sequences that have had nucleotide analysis performed
    analysed_nuc_seqs = [s for s in all_sequences if s.get("gc_content") is not None]

    # Raised if sequences exist but none have been nucleotide analysed yet
    if len(analysed_nuc_seqs) == 0:
        raise HTTPException(status_code=404, detail="Summary statistics cannot be calculated: No nucleotide sequences currently stored in the DNA Toolkit have undergone analysis.")

    # Calculate nucleotide summary statistics across all nucleotide-analysed sequences
    av_gc = mean([s["gc_content"] for s in analysed_nuc_seqs])
    av_nuc_length = mean([s["seq_length"] for s in analysed_nuc_seqs])
    longest_nucseq = max(analysed_nuc_seqs, key=lambda x: x["seq_length"])
    shortest_nucseq = min(analysed_nuc_seqs, key=lambda x: x["seq_length"])

    # Filter to only sequences that have had amino acid analysis performed
    # If none have, average amino acid length is returned as null rather than raising an error
    analysed_aa_seqs = [s for s in all_sequences if s.get("residue_count") is not None]
    if len(analysed_aa_seqs) == 0:
        av_aa_length = None
    else:
        av_aa_length = mean([s["residue_count"] for s in analysed_aa_seqs])
    
    return {
        "message": "Summary of key statistics of all sequences currently stored in DNA Toolkit. If a statistic is missing, it is likely due to GC content analysis or Amino Acid conversion not having been performed yet.",
        "total_sequences": len(all_sequences),
        "nuc_analysed_sequences": len(analysed_nuc_seqs),
        "aa_analysed_sequences": len(analysed_aa_seqs),
        "average_gc_content": av_gc,
        "average_nucleotide_length": av_nuc_length,
        "average_amino_acid_length": av_aa_length,
        "longest_nucleotide_sequence": longest_nucseq["label"],
        "shortest_nucleotide_sequence": shortest_nucseq["label"]
    }