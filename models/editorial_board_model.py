from datetime import datetime
import json

from enum import Enum
import json

class EditorialRole(Enum):
    EDITOR = "Editor"
    ASSOCIATE_EDITOR = "Associate Editor"
    CHIEF_EDITOR = "Chief Editor"

class EditorialBoardMember:
    def __init__(self, created_at, email, id, institution, name, role):
        self.created_at = created_at
        self.email = email
        self.id = id
        self.institution = institution
        self.name = name
        self.role = EditorialRole(role)  # Convert string to Enum

    @classmethod
    def from_dict(cls, data):
        return cls(
            created_at=datetime.fromisoformat(data['createdAt']) if 'createdAt' in data else None,
            email=data.get('email'),
            id=data.get('id'),
            institution=data.get('institution'),
            name=data.get('name'),
            role=data.get('role')
        )

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self):
        return f"EditorialBoardMember(created_at={self.created_at}, email='{self.email}', id='{self.id}', institution='{self.institution}', name='{self.name}', role={self.role.value})"

