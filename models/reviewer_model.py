from firebase_admin import firestore

class ReviewerModel:
    def __init__(self, title=None, name=None, id=None, email=None, journal=None, 
                 role=None, password=None, country=None, mobile=None, 
                 corresponding_address=None, details_cv=None, research_domain=None):
        self.title = title
        self.name = name
        self.id = id
        self.email = email
        self.journal = journal
        self.role = role
        self.password = password
        self.country = country
        self.mobile = mobile
        self.corresponding_address = corresponding_address
        self.details_cv = details_cv
        self.research_domain = research_domain

    def to_dict(self):
        return {
            'title': self.title,
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'journal': self.journal,
            'password': self.password,
            'country': self.country,
            'mobile': self.mobile,
            'correspondingAddress': self.corresponding_address,
            'detailsCV': self.details_cv,
            'researchDomain': self.research_domain,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title'),
            email=data.get('email'),
            role=data.get('role'),
            journal=data.get('journal'),
            password=data.get('password'),
            country=data.get('country'),
            mobile=data.get('mobile'),
            corresponding_address=data.get('correspondingAddress'),
            details_cv=data.get('detailsCV'),
            research_domain=data.get('researchDomain'),
            id=data.get('id'),
            name=data.get('name'),
        )
