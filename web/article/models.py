from django.db import models
import random
# Create your models here.
    
class ArticleInfo(models.Model):
    title=models.CharField(max_length=100)
    brief=models.CharField(max_length=100,default='')
    date=models.CharField(max_length=20)
    like=models.IntegerField(default=0)
    author=models.CharField(max_length=100)
    comment_num=models.IntegerField(default=0)
    category=models.CharField(max_length=10,default='')
    url=models.CharField(max_length=100,default='')
    def __cmp__(self, other):
        return self.like>other.like
    class Meta:
        indexes=[
            models.Index(
                fields=['id'],name='id_index'
            )
        ]

class Comment(models.Model):
    article=models.ForeignKey(ArticleInfo,on_delete=models.CASCADE,related_name='comments')
    body=models.TextField()
    post_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=(['-post_time'])

class Dic(models.Model):
    name=models.CharField(max_length=100)
    content=models.TextField()