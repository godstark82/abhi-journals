import json
from typing import List

from models.issue_model import IssueModel

class VolumeModel:
    def __init__(self, title=None, journal_id=None, created_at=None, id=None, is_active=None, description=None,volume_number=None,issues:List[IssueModel]=None):
        self.title = title
        self.journal_id = journal_id
        self.created_at = created_at
        self.id = id
        self.is_active = is_active
        self.description = description
        self.volume_number = volume_number
        self.issues = issues

    def to_dict(self):
        return {
            'title': self.title,
            'journalId': self.journal_id,
            'createdAt': self.created_at,
            'id': self.id,
            'isActive': self.is_active,
            'description': self.description,
            'volumeNumber': self.volume_number
        }
    
    def __str__(self):
        return f"VolumeModel(title={self.title}, journal_id={self.journal_id}, created_at={self.created_at}, id={self.id}, is_active={self.is_active}, description={self.description}, volume_number={self.volume_number})"

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            journal_id=data.get('journalId'),
            created_at=data.get('createdAt'),
            id=data.get('id'),
            is_active=data.get('isActive'),
            description=data.get('description'),
            volume_number=data.get('volumeNumber')
        )

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls.from_dict(data)




