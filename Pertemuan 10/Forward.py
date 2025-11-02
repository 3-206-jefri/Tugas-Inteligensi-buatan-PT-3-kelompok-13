import copy
from typing import List, Dict, Any

FACT_BASE_INITIAL = [
    "Mesin Mati Total",
    "Suara Klik saat Start",
    "Tidak ada Karat pada Terminal"
]

RULE_BASE = [
    {"ID": "R1", "IF": ["Mesin Mati Total"], "THEN": "Cek Kelistrikan", "Priority": 1},
    {"ID": "R2", "IF": ["Mesin Berputar Lambat"], "THEN": "Aki Lemah", "Priority": 2},
    {"ID": "R3", "IF": ["Lampu Redup"], "THEN": "Aki Lemah", "Priority": 2},
    {"ID": "R4", "IF": ["Aki Lemah", "Tidak ada Karat pada Terminal"], "THEN": "Ganti Aki", "Priority": 3},
    {"ID": "R5", "IF": ["Suara Klik saat Start"], "THEN": "Aki Lemah", "Priority": 2},
    {"ID": "R6", "IF": ["Mesin Mati Total", "Tidak ada Suara"], "THEN": "Fungsi Kelistrikan Terputus", "Priority": 4},
    {"ID": "R7", "IF": ["Aki Lemah"], "THEN": "Mesin Sulit Start", "Priority": 1},
    {"ID": "R8", "IF": ["Cek Kelistrikan", "Terjadi Konsleting"], "THEN": "Isolasi Kelistrikan", "Priority": 5}
]


def forward_chaining_implementation(fact_base: List[str], rule_base: List[Dict[str, Any]]) -> List[str]:
    print("===================================================")
    print("IMPLEMENTASI: ALGORITMA FORWARD CHAINING (Data-Driven)")
    print("===================================================")
    
    current_fact_base = copy.deepcopy(fact_base)
    rules_fired: list = []
    
    print(f"Fakta Awal: {current_fact_base}")
    
    new_fact_added = True
    iteration = 0

    while new_fact_added:
        iteration += 1
        new_fact_added = False
        conflict_set = []

        print(f"\n--- ITERASI {iteration} ---")

        for rule in rule_base:
            if rule["ID"] not in rules_fired:
                all_conditions_met = all(condition in current_fact_base for condition in rule["IF"])
                
                if all_conditions_met:
                    conflict_set.append(rule)
        
        conflict_set_ids = sorted([f"{r['ID']} (P:{r['Priority']})" for r in conflict_set])
        print(f"   Conflict Set ditemukan: {conflict_set_ids}")

        if conflict_set:
            best_rule = max(conflict_set, key=lambda r: r["Priority"])
            
            print(f"   Aturan Dieksekusi: {best_rule['ID']} (Prioritas: {best_rule['Priority']})")

            new_fact = best_rule["THEN"]
            
            if new_fact not in current_fact_base:
                current_fact_base.append(new_fact)
                new_fact_added = True
                print(f"   **FAKTA BARU DITAMBAHKAN**: {new_fact}")
            else:
                print(f"   Fakta '{new_fact}' sudah ada.")
            
            rules_fired.append(best_rule["ID"])
            
        else:
            print("   Tidak ada aturan yang cocok lagi. Proses berhenti.")
            break

    print("\n===================================================")
    print("SELESAI: FORWARD CHAINING")
    print(f"**Kesimpulan Akhir**: {current_fact_base}")
    print("===================================================")
    return current_fact_base


if __name__ == "__main__":
    
    forward_chaining_implementation(FACT_BASE_INITIAL, RULE_BASE)
    
    FACT_BASE_SIMULASI_R8 = FACT_BASE_INITIAL + ["Terjadi Konsleting"]
    
    print("\n\n" + "="*70)
    print("SIMULASI P.3: MENGAKTIFKAN R8 (Prioritas Tertinggi)")
    print("Fakta Awal Ditambah: 'Terjadi Konsleting'")
    print("="*70)
    forward_chaining_implementation(FACT_BASE_SIMULASI_R8, RULE_BASE)
