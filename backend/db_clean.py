import firebase_admin
from firebase_admin import credentials, firestore
import os

# 1. Initialize Firebase
# Ensure 'firebase_config.json' is in backend/core/ or update path below
cred_path = "backend/core/firebase_config.json" 

if not os.path.exists(cred_path):
    # Try looking in current directory if running from backend folder
    cred_path = "core/firebase_config.json"

if not os.path.exists(cred_path):
    print(f"❌ Error: Cannot find {cred_path}")
    exit(1)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def clean_database():
    print("🧹 Starting Database Cleanup...")
    
    # 1. Target the 'videos' collection (Old Schema)
    collection_ref = db.collection("videos")
    docs = collection_ref.stream()
    
    deleted_count = 0
    
    for doc in docs:
        print(f"Deleting doc: {doc.id} - {doc.to_dict().get('title', 'Untitled')}")
        doc.reference.delete()
        deleted_count += 1
        
    print(f"\n✅ Cleanup Complete. Deleted {deleted_count} video records.")
    print("Note: This did NOT delete files from Azure Blob Storage (to save bandwidth/time).")

if __name__ == "__main__":
    confirm = input("⚠️ Are you sure you want to delete ALL videos from Firestore? (y/n): ")
    if confirm.lower() == 'y':
        clean_database()
    else:
        print("Cancelled.")