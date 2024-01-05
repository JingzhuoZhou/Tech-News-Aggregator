from django.contrib import admin
from .models import ArticleInfo,Comment,Dic
from import_export.admin import ImportExportModelAdmin
from .resources import ArticleResource,CommentResource,DicResource

class ArticleAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource
class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentResource
class DicAdmin(ImportExportModelAdmin):
    resource_class = DicResource

admin.site.register(ArticleInfo, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Dic, DicAdmin)