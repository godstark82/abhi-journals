from db_instance import get_db

def get_page(name, journal_id) -> str:
    db = get_db()
    doc_ref = db.collection('pages').where('name', '==', name).where('journalId', '==', journal_id).get()
    if len(doc_ref) == 0:
        return "Document not found"
    doc = doc_ref[0].to_dict()
    if doc:
        # Extract 'content' field from the document
        content = doc.get('content', '')
        return content
    else:
        return "Document not found"