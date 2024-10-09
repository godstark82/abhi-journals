from typing import List, Optional
from db_instance import get_db
from models.journal_model import JournalModel
from services import journal_service


db = get_db();
#! Fetch all journals 
all_journals = journal_service.get_all_journals()
journal: JournalModel = None

def get_journal(all_journals: List[JournalModel], subdomain: str)-> Optional[JournalModel]:
    journal = None
    for journalItem in all_journals:
        if journalItem.domain == subdomain:
            journal = journalItem
            break

    if not journal:
        return None
    journal_details = journal_service.get_journal(journal.id)
    return journal_details

journal = get_journal(all_journals, "main")
# IID 5Nz5HZiBBSr2wkYfe3xC
print(journal.volumes[0].issues[0].articles[0].title)