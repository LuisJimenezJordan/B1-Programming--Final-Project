from fastapi import APIRouter
from schema import DNATaskCreate, DNATask

router = APIRouter()

@router.post("/")
def GC_analysis(task_input: DNATaskCreate):
     dna_seq = task_input.sequence.upper()
     g_count = dna_seq.count("G")
     c_count = dna_seq.count("C")
     total_len = len(dna_seq)
     if total_len == 0:
          GC_content = 0
     else:
          GC_content =round((g_count + c_count)/total_len, 4)
     
     # This saves the data from the analysis to the file
     with open("debug_tasks.txt","a",encoding="utf-8") as f:
          f.write(f"TEST: {task_input.label} - {GC_content}\n")
          f.flush()

     return {
          "id":1,
          "label":task_input.label,
          "sequence":dna_seq,
          "gc_content":GC_content,
          "status":"completed"
     }