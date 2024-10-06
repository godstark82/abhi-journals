from datetime import datetime
from typing import Dict, Any, List
import json

from models.article_model import ArticleModel

class IssueModel:
    def __init__(self, id: str, title: str, issue_number: str, volume_id: str,
                 journal_id: str, description: str, from_date: datetime,
                 to_date: datetime, is_active: bool, articles:List[ArticleModel]=None):
        self.id = id
        self.title = title
        self.issue_number = issue_number
        self.volume_id = volume_id
        self.journal_id = journal_id
        self.description = description
        self.from_date = from_date
        self.to_date = to_date
        self.is_active = is_active
        self.articles = articles

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data['id'],
            title=data['title'],
            issue_number=data['issueNumber'],
            volume_id=data['volumeId'],
            journal_id=data['journalId'],
            description=data['description'],
            from_date=datetime.fromisoformat(data['fromDate']),
            to_date=datetime.fromisoformat(data['toDate']),
            is_active=data['isActive']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'issueNumber': self.issue_number,
            'volumeId': self.volume_id,
            'journalId': self.journal_id,
            'description': self.description,
            'fromDate': self.from_date.isoformat(),
            'toDate': self.to_date.isoformat(),
            'isActive': self.is_active,
        }
    
    def __str__(self):
        return f"IssueModel(id={self.id}, title={self.title}, issue_number={self.issue_number}, volume_id={self.volume_id}, journal_id={self.journal_id}, description={self.description}, from_date={self.from_date}, to_date={self.to_date}, is_active={self.is_active})"
    
    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls.from_dict(data)

    def copy_with(self, **kwargs) -> 'IssueModel':
        new_data = self.__dict__.copy()
        new_data.update(kwargs)
        return IssueModel(**new_data)