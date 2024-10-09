import json
from typing import List

from models.issue_model import IssueModel
from models.volume_model import VolumeModel
from models.article_model import ArticleModel, ArticleStatus


class JournalModel:
    def __init__(self, title=None, domain=None, created_at=None, id=None, volumes: List[VolumeModel] = None):
        self.title = title
        self.domain = domain
        self.created_at = created_at
        self.id = id
        self.volumes = volumes or []

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

    
    def get_all_active_volumes(self) -> List[VolumeModel]:
        result_volumes = []
        for volume in self.volumes:
            if volume.is_active:
                result_volumes.append(volume)
        return result_volumes
    
    def get_all_active_issues(self) -> List[IssueModel]:
        result_issues = []
        for volume in self.volumes:
            if volume.is_active:
                for issue in volume.issues:
                    if issue.is_active:
                        result_issues.append(issue)
        return result_issues
    
    def get_all_artcles_of_active_issues(self) -> List[ArticleModel]:
        result_articles = []
        for issue in self.get_all_active_issues():
            for article in issue.articles:
                if article.status == ArticleStatus.PUBLISHED:
                    result_articles.append(article)
        return result_articles
    
    def get_all_published_articles_of_journal(self) -> List[ArticleModel]:
        result_articles = []
        for volume in self.volumes:
            for issue in volume.issues:
                for article in issue.articles:
                    if article.status == ArticleStatus.PUBLISHED:
                        result_articles.append(article)
        return result_articles
    
    def get_all_published_articles_of_journal_by_volume(self, volume_id: str) -> List[ArticleModel]:
        result_articles = []
        for volume in self.volumes:
            if volume.id == volume_id:
                for issue in volume.issues:
                    for article in issue.articles:
                        if article.status == ArticleStatus.PUBLISHED:
                            result_articles.append(article)
        return result_articles
    
    def get_all_published_articles_of_journal_by_issue(self, issue_id: str) -> List[ArticleModel]:
        result_articles = []
        for volume in self.volumes:
            for issue in volume.issues:
                if issue.id == issue_id:
                    for article in issue.articles:
                        if article.status == ArticleStatus.PUBLISHED:
                            result_articles.append(article)
        return result_articles

    def get_all_issues(self) -> List[IssueModel]:
        result_issues = []
        for volume in self.volumes:
            for issue in volume.issues:
                result_issues.append(issue)
        return result_issues
    
    def get_all_issues_of_volume(self, volume_id: str) -> List[IssueModel]:
        result_issues = []
        for volume in self.volumes:
            if volume.id == volume_id:
                for issue in volume.issues:
                    result_issues.append(issue)
        return result_issues
    
    def get_all_articles_of_issue(self, issue_id: str) -> List[ArticleModel]:
        result_articles = []
        for volume in self.volumes:
            for issue in volume.issues:
                if issue.id == issue_id:
                    for article in issue.articles:
                        result_articles.append(article)
        return result_articles

    def get_article_by_id(self, article_id: str) -> ArticleModel:
        for volume in self.volumes:
            for issue in volume.issues:
                for article in issue.articles:
                    if article.id == article_id:
                        return article
        return None
