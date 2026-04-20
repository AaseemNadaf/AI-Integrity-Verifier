import os
import shutil
from hash_utils import compute_model_hash
from blockchain_utils import verify_model, is_model_registered

MODEL_PATH = "../model/model.pkl"
BACKUP_PATH = "../model/model_backup.pkl"
MODEL_NAME = "iris_v1"

def print_separator():
    print("=" * 60)

def run_simulation():
    print_separator()
    print("   AI MODEL INTEGRITY - TAMPER SIMULATION")
    print_separator()

    if not os.path.exists(MODEL_PATH):
        print("ERROR: model.pkl not found. Run train_model.py first.")
        return

    if not is_model_registered(MODEL_NAME):
        print(f"ERROR: Model '{MODEL_NAME}' is not registered on blockchain.")
        print("Please register it first using the web dashboard.")
        return

    print("\n STEP 1 - Computing original hash...")
    original_hash = compute_model_hash(MODEL_PATH)
    print(f" Original Hash: {original_hash}")

    print("\n STEP 2 - Verifying original model on blockchain...")
    result = verify_model(MODEL_NAME, original_hash)
    if result:
        print(" Blockchain Verification: PASSED ✅")
    else:
        print(" Blockchain Verification: FAILED ❌")
        return

    print("\n STEP 3 - Creating backup of original model...")
    shutil.copy2(MODEL_PATH, BACKUP_PATH)
    print(f" Backup saved to: {BACKUP_PATH}")

    print("\n STEP 4 - Tampering with the model file...")
    with open(MODEL_PATH, "ab") as f:
        f.write(b"\x00\xFF\x00\xFF malicious payload injected")
    print(" Model file has been modified!")

    print("\n STEP 5 - Computing tampered model hash...")
    tampered_hash = compute_model_hash(MODEL_PATH)
    print(f" Tampered Hash: {tampered_hash}")

    print("\n STEP 6 - Comparing hashes...")
    print_separator()
    print(f" Original Hash : {original_hash}")
    print(f" Tampered Hash : {tampered_hash}")
    print(f" Hashes Match  : {original_hash == tampered_hash}")
    print_separator()

    print("\n STEP 7 - Verifying tampered model on blockchain...")
    tampered_result = verify_model(MODEL_NAME, tampered_hash)
    if tampered_result:
        print(" Blockchain Verification: PASSED ✅")
    else:
        print(" TAMPERING DETECTED BY BLOCKCHAIN ⚠️")
        print(" The model has been compromised!")

    print("\n STEP 8 - Restoring original model from backup...")
    shutil.copy2(BACKUP_PATH, MODEL_PATH)
    os.remove(BACKUP_PATH)
    print(" Original model restored successfully!")

    print("\n STEP 9 - Final verification after restore...")
    restored_hash = compute_model_hash(MODEL_PATH)
    final_result = verify_model(MODEL_NAME, restored_hash)
    if final_result:
        print(" Restored model verified successfully ✅")
    else:
        print(" Restore failed ❌")

    print_separator()
    print(" SIMULATION COMPLETE")
    print_separator()
    print(f"\n SUMMARY")
    print(f" Original Hash  : {original_hash[:32]}...")
    print(f" Tampered Hash  : {tampered_hash[:32]}...")
    print(f" Tamper Caught  : {not tampered_result}")
    print(f" Model Restored : {final_result}")
    print_separator()

if __name__ == "__main__":
    run_simulation()