import os
import sys
import asyncio
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def execute_nb(nb_path):
    print(f"--- Executing {nb_path} ---")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': 'notebooks'}})
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"--- Finished executing {nb_path} successfully! ---")

if __name__ == '__main__':
    notebooks = [
        'notebooks/00_master_spatial_decision_handbook.ipynb',
        'notebooks/01_exploratory_spatial_data_analysis.ipynb',
        'notebooks/02_spatial_statistics_modeling.ipynb',
        'notebooks/03_sectoral_decision_intelligence.ipynb'
    ]
    for nb in notebooks:
        execute_nb(nb)
    print("All notebooks executed and saved with outputs!")
