from fastapi import APIRouter, HTTPException
from schema import NucleotideResult, AminoAcidResult, SummaryStats
from storage import load_sequences, save_sequences
from AA_lookup import AA_Properties, Codon_Table
from statistics import mean

router = APIRouter()

def calculate_gc(sequence: str) -> float:
     sequence = sequence.upper()
     seq_length = len(sequence)
     gc_content = round((sequence.count("G") + sequence.count("C")) / seq_length, 4)
     return gc_content, seq_length

@router.get("/{id}/nucleotide", response_model= NucleotideResult)
def nucleotide_analysis(id:int):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            gc_content, seq_length = calculate_gc(sequence["sequence"])
            sequence["gc_content"] = gc_content
            sequence["seq_length"] = seq_length
            sequence["analysed"] = True
            save_sequences(all_sequences)
            
            return {
            "message": f"DNA Nucleotide sequence with ID:{id} successfully analysed. See below the length of the sequence and its total GC content, which can be used to design primer melting and annealing temperatures",
            "sequence_id": id,
            "label": sequence["label"],
            "length": seq_length,
            "gc_content": gc_content
        }
    raise HTTPException(status_code=404, detail=f"Analysis could not be performed on sequence ID:{id}: ID not found")

@router.get("/{id}/aminoacid", response_model= AminoAcidResult)
def aminoacid_analysis(id:int):
    all_sequences = load_sequences()
    for sequence in all_sequences:
        if id == sequence["id"]:
            amino_acids = []
            dna_str = sequence["sequence"].upper()

            #Converts the DNA nucleotide sequence into an amino acid sequence
            for i in range(0, len(dna_str), 3):
                codon = dna_str[i:i+3]
                if len(codon) < 3:  # ignore incomplete codons at the end
                    break
                amino_acid = Codon_Table.get(codon, "Unknown")
                if amino_acid == "Stop":
                    break
                amino_acids.append(amino_acid)
            
            if len(amino_acids) <1:
                raise HTTPException(status_code=400, detail=f"Nucleotide sequence ID:{id} consisted only of a STOP codon. Therefore, conversion to Amino Acids produced no viable sequence.")

            #Determines the proportions of each amino acid property in the amino acid sequence
            composition = {}
            for amino_acid in amino_acids:
                aa_property = AA_Properties.get(amino_acid, "Unknown")
                composition[aa_property] = composition.get(aa_property, 0) + 1
            
            #Calculates the top 3 Amino Acids appearing in the sequences by proportion
            residue_counts = {}
            for amino_acid in amino_acids:
                residue_counts[amino_acid] = residue_counts.get(amino_acid, 0) + 1
            
            residue_percentages = {}   
            for aa, count in residue_counts.items():
                residue_percentages[aa] = round((count / len(amino_acids)) * 100, 2)
            
            top_3_residues = sorted(residue_percentages.items(), key=lambda x: x[1], reverse=True) [:3]
            top_3_residues = [{"residue": aa, "percentage": pct} for aa, pct in top_3_residues]

            sequence["amino_acid_sequence"] = "-".join(amino_acids)
            sequence["residue_count"] = len(amino_acids)
            sequence["composition"] = composition
            sequence["top_3_residues"] = top_3_residues
            sequence["analysed"] = True
            save_sequences(all_sequences)

            return {
            "message": f"DNA Nucleotide conversion to Amino Acid sequence with ID:{id} successfully completed. See below the converted sequence, the Amino Acid sequence length, the proportion of the different types of Amino Acid proprties present in the sequence, and the top 3 most common Amino Acid Residues.",
            "sequence_id": id,
            "label": sequence["label"],
            "amino_acid_sequence": "-".join(amino_acids),
            "residue_count": len(amino_acids),
            "composition": composition,
            "top_3_residues": top_3_residues
          }
    raise HTTPException(status_code=404, detail=f"DNA to Amino Acid sequence conversion could not be performed on sequence ID:{id}: ID not found")

@router.get("/summary_statistics", response_model = SummaryStats)
def summary_analysis():
    all_sequences = load_sequences()
    if len(all_sequences) == 0:
        raise HTTPException(status_code=404, detail=f"Summary statistics cannot be calculated: No nucleotide sequences have been submitted to DNA Toolkit.")

    analysed_nuc_seqs = [s for s in all_sequences if s["gc_content"] is not None]
    if len(analysed_nuc_seqs) == 0:
        raise HTTPException(status_code=404, detail=f"Summary statistics cannot be calculated: No nucleotide sequences currently stored in the DNA Toolkit have undergone analysis.")

    av_gc = mean([s["gc_content"] for s in analysed_nuc_seqs])
    av_nuc_length = mean([s["seq_length"] for s in analysed_nuc_seqs])
    longest_nucseq = max(analysed_nuc_seqs, key=lambda x: x["seq_length"])
    shortest_nucseq = min(analysed_nuc_seqs, key=lambda x: x["seq_length"])

    analysed_aa_seqs = [s for s in all_sequences if s["residue_count"] is not None]
    if len(analysed_aa_seqs) == 0:
        av_aa_length = None
    else:
        av_aa_length = mean([s["residue_count"] for s in analysed_aa_seqs])
    
    return {
    "message": "Summary of key statistics of all sequences currently stored in DNA Toolkit. If a statistic is missing, it is likely due to GC content analysis or Amino Acid conversion not having been performed yet.",
    "total_sequences": len(all_sequences),
    "analysed_sequences": len(analysed_nuc_seqs),
    "average_gc_content": av_gc,
    "average_nucleotide_length": av_nuc_length,
    "average_amino_acid_length": av_aa_length,
    "longest_sequence": longest_nucseq["label"],
    "shortest_sequence": shortest_nucseq["label"]
}
