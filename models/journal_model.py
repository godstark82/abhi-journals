import json
from typing import List

from models.volume_model import VolumeModel


class JournalModel:
    def __init__(self, title=None, domain=None, created_at=None, id=None,volumes:List[VolumeModel]=None):
        self.title = title
        self.domain = domain
        self.created_at = created_at
        self.id = id
        self.volumes = volumes

    def to_dict(self):
        return {
            'title': self.title,
            'domain': self.domain,
            'createdAt': self.created_at,
            'id': self.id
        }

    def from_dict(self, data):
        self.title = data.get('title')
        self.domain = data.get('domain')
        self.created_at = data.get('createdAt')
        self.id = data.get('id')

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        journal = cls()
        journal.from_dict(data)
        return journal
    
    def __str__(self):
        return f"JournalModel(title={self.title}, domain={self.domain}, created_at={self.created_at}, id={self.id})"
