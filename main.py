from datasets import load_dataset
import os

def main():
    
    dataset = load_dataset("nielsr/funsd", split="train", streaming=True)
    
    os.makedirs("data", exist_ok=True)
        
    for row in dataset:
        image = row["image"]
        save_path = "data/sample_funsd_form.png"
        image.save(save_path)
        
        print(f"\nDocumento salvato in: {save_path}")
        
        # Nel dataset 'nielsr/funsd', il testo estratto si trova nella colonna 'words'
        print("\nAnteprima del testo estratto dai ricercatori (ground truth):")
        print(row["words"])
        break

if __name__ == "__main__":
    main()