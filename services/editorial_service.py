from typing import List
from firebase_admin import firestore
from models.editorial_board_model import EditorialBoardMember
from db_instance import get_db

def get_all_editorial_board_members() -> List[EditorialBoardMember]:
    db = get_db()
    editorial_board_ref = db.collection('editorialBoard')
    editorial_board_docs = editorial_board_ref.stream()

    editorial_board_members = []
    for doc in editorial_board_docs:
        member_data = doc.to_dict()

        editorial_board_member = EditorialBoardMember.from_dict(member_data)
        editorial_board_members.append(editorial_board_member)

    return editorial_board_members
