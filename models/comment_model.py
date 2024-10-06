from datetime import datetime
from models.reviewer_model import ReviewerModel

class CommentModel:
    def __init__(self, reviewer=None, msg=None, created_at=None):
        self.reviewer = reviewer
        self.msg = msg
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        return cls(
            reviewer=ReviewerModel.from_dict(data.get('reviewer')) if data.get('reviewer') else None,
            msg=data.get('msg'),
            created_at=datetime.fromisoformat(data.get('createdAt')) if data.get('createdAt') else None
        )

    def to_dict(self):
        return {
            'reviewer': self.reviewer.to_dict() if self.reviewer else None,
            'msg': self.msg,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }