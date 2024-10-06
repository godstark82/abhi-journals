from db_instance import get_db

def get_page(page_id) -> str:
    db = get_db()
    doc_ref = db.collection('pages').document(page_id)
    doc = doc_ref.get()
    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return content
    else:
        return "Document not found"