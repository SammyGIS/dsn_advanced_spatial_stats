import os
import zipfile

def ensure_processed_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    processed_dir = os.path.join(data_dir, 'processed')
    parquet_path = os.path.join(processed_dir, 'nigeria_wards_master.parquet')
    zip_path = os.path.join(data_dir, 'processed_data_bundle.zip')
    
    os.makedirs(processed_dir, exist_ok=True)
    
    if os.path.exists(parquet_path):
        print(f"Master parquet dataset already present: {parquet_path}")
        return parquet_path
    
    if os.path.exists(zip_path):
        print(f"Extracting {zip_path} to {processed_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(processed_dir)
        print(f"Successfully extracted: {parquet_path}")
        return parquet_path
    else:
        print(f"Error: Neither {parquet_path} nor {zip_path} was found.")
        print("Please run 'python etl/run_pipeline.py' to generate the data.")
        return None

if __name__ == '__main__':
    ensure_processed_data()
