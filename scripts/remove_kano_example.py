import json

nb_path = 'notebooks/00_master_spatial_decision_handbook.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell.get('cell_type') == 'code':
        src = "".join(cell.get('source', []))
        if "inspect_state_profile('Kano')" in src:
            new_source = []
            for line in cell['source']:
                if "Inspect Kano and Lagos States" in line:
                    new_source.append("# Example: Inspect Lagos State Profile\n")
                elif "inspect_state_profile('Kano')" in line:
                    continue
                else:
                    new_source.append(line)
            cell['source'] = new_source
            print("Successfully replaced Kano example with Lagos only in notebook 00!")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
