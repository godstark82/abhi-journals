from datetime import datetime
import json
from typing import List, Dict, Any
from models.comment_model import CommentModel

from enum import Enum

class ArticleStatus(Enum):
    PUBLISHED = "published"
    PENDING = "pending"
    REJECTED = "rejected"


class ArticleModel:
    def __init__(self, id: str, journal_id: str, abstract_string: str, authors: List[Dict[str, Any]],
                 issue_id: str, volume_id: str, document_type: str, image: str, keywords: List[str],
                 main_subjects: List[str], created_at: datetime, updated_at: datetime,
                 comments: List[CommentModel], pdf: str, references: List[str], title: str, status: ArticleStatus):
        self.id = id
        self.journal_id = journal_id
        self.abstract_string = abstract_string
        self.authors = authors
        self.issue_id = issue_id
        self.volume_id = volume_id
        self.document_type = document_type
        self.image = image
        self.keywords = keywords
        self.main_subjects = main_subjects
        self.created_at = created_at
        self.updated_at = updated_at
        self.comments = comments
        self.pdf = pdf
        self.references = references
        self.title = title
        self.status = status

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data['id'],
            journal_id=data['journalId'],
            abstract_string=str(data['abstractString']),
            authors=data['authors'],  # Assuming authors are already in dict format
            issue_id=data['issueId'],
            volume_id=data['volumeId'],
            document_type=data['documentType'],
            image=data['image'],
            keywords=data['keywords'],
            main_subjects=data['mainSubjects'],
            created_at=datetime.fromisoformat(data['createdAt']),
            updated_at=datetime.fromisoformat(data['updatedAt']),
            comments=[CommentModel.from_dict(comment) for comment in data['comments']],
            pdf=data['pdf'],
            references=data['references'],
            title=data['title'],
            status=ArticleStatus(data['status'])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'journalId': self.journal_id,
            'abstractString': self.abstract_string,
            'authors': self.authors,
            'issueId': self.issue_id,
            'volumeId': self.volume_id,
            'documentType': self.document_type,
            'image': self.image,
            'keywords': self.keywords,
            'mainSubjects': self.main_subjects,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'comments': [comment.to_dict() for comment in self.comments],
            'pdf': self.pdf,
            'references': self.references,
            'title': self.title,
            'status': self.status.value,
        }

    def copy_with(self, **kwargs) -> 'ArticleModel':
        new_data = self.__dict__.copy()
        new_data.update(kwargs)
        return ArticleModel(**new_data)
    
    def __str__(self):
        return f"ArticleModel(id={self.id}, title={self.title}, abstract_string={self.abstract_string}, authors={self.authors}, issue_id={self.issue_id}, volume_id={self.volume_id}, document_type={self.document_type}, image={self.image}, keywords={self.keywords}, main_subjects={self.main_subjects}, created_at={self.created_at}, updated_at={self.updated_at}, comments={self.comments}, pdf={self.pdf}, references={self.references}, status={self.status})"
    
    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls.from_dict(data)