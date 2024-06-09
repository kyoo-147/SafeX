# -*- encoding: utf-8 -*-
#   Copyright SafeX (https://github.com/kyoo-147/SafeX) 2024. All Rights Reserved.
#   MIT License  (https://opensource.org/licenses/MIT)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from datetime import datetime
from google.cloud import storage

# Initialize Firebase
cred = credentials.Certificate("X_Config/firebase_credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-test-5183c-default-rtdb.firebaseio.com/'  # Thay <your-database-name> bằng tên của Realtime Database của bạn
})

db_firestore = firestore.client()
storage_client = storage.Client.from_service_account_json("X_Config/firebase_credentials.json")
bucket_name = 'face-test-5183c'  # Thay thế bằng tên bucket của bạn

def upload_to_storage(file_path, name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f'{name}/{file_path}')
    blob.upload_from_filename(file_path)
    return blob.public_url

def update_firebase(name, image_url):
    # Cập nhật Firestore
    doc_ref = db_firestore.collection(u'faces').document(name)
    doc_ref.set({
        u'name': name,
        u'time': firestore.SERVER_TIMESTAMP,
        u'image_url': image_url
    }, merge=True)
    
    # Cập nhật Realtime Database
    db.reference(f'faces/{name}').set({
        'name': name,
        'time': datetime.now().isoformat(),
        'image_url': image_url
    })

def log_entry_exit(name, image_url):
    timestamp = datetime.now()
    date_str = timestamp.strftime("%Y-%m-%d")
    
    # Ghi log vào Firestore
    log_ref = db_firestore.collection(u'faces').document(name).collection('daily_logs').document(date_str).collection('entries').add({
        u'time': timestamp,
        u'image_url': image_url
    })
    
    # Ghi log vào Realtime Database
    db.reference(f'faces/{name}/daily_logs/{date_str}/entries').push({
        'time': timestamp.isoformat(),
        'image_url': image_url
    })
