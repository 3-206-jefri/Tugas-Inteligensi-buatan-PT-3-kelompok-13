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

def recursive_backward_chaining(goal: str, rule_base: List[Dict[str, Any]], initial_facts: List[str], depth: int = 0) -> bool:
    """Fungsi rekursif inti dari Backward Chaining."""
    
    indent = "  " * depth
    print(f"{indent}**GOAL**: Mencari bukti untuk '{goal}'")

    if goal in initial_facts:
        print(f"{indent}  **SUKSES**: '{goal}' sudah ada di Fakta Awal.")
        return True

    applicable_rules = [rule for rule in rule_base if rule["THEN"] == goal]

    if not applicable_rules:
        print(f"{indent}  **GAGAL**: Tidak ada aturan yang menyimpulkan '{goal}'.")
        return False

    applicable_rules_ids = [r["ID"] for r in applicable_rules]
    print(f"{indent}  Aturan yang mungkin: {applicable_rules_ids}")
    
    for rule in applicable_rules:
        print(f"{indent}  Mencoba Aturan {rule['ID']}: JIKA {rule['IF']}")
        all_sub_goals_proven = True
        
        for sub_goal in rule["IF"]:
            is_sub_goal_proven = recursive_backward_chaining(
                sub_goal, rule_base, initial_facts, depth + 1
            )
            
            if not is_sub_goal_proven:
                all_sub_goals_proven = False
                print(f"{indent}    Gagal membuktikan sub-goal, Aturan {rule['ID']} tidak bisa dipakai.")
                break
        
        if all_sub_goals_proven:
            print(f"{indent}  **BERHASIL**: '{goal}' terbukti melalui Aturan {rule['ID']}")
            return True
    
    print(f"{indent}  **Gagal total**: Semua jalur untuk membuktikan '{goal}' habis.")
    return False


def backward_chaining_implementation(goal_to_prove: str, rule_base: List[Dict[str, Any]], initial_facts: List[str]) -> bool:
    print("\n===================================================")
    print("IMPLEMENTASI: ALGORITMA BACKWARD CHAINING (Goal-Driven)")
    print("===================================================")
    print(f"TUJUAN UTAMA: Membuktikan '**{goal_to_prove}**'")
    print(f"Fakta Awal: {initial_facts}\n")
    
    is_proven = recursive_backward_chaining(goal_to_prove, rule_base, initial_facts, 0)
    
    print("\n-------------------------------------")
    if is_proven:
        print(f"HASIL AKHIR: TUJUAN '{goal_to_prove}' **TERBUKTI**.")
    else:
        print(f"HASIL AKHIR: TUJUAN '{goal_to_prove}' **GAGAL DIBUKTIKAN**.")
    print("-------------------------------------")
    return is_proven

if __name__ == "__main__":
    
    backward_chaining_implementation("Ganti Aki", RULE_BASE, FACT_BASE_INITIAL)
