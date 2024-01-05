from import_export import resources
from .models import ArticleInfo,Comment,Dic

class ArticleResource(resources.ModelResource):
    class Meta:
        model = ArticleInfo

class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment

class DicResource(resources.ModelResource):
    class Meta:
        model=Dic