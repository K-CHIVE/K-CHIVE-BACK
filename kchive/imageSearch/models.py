# from datetime import date
# from email.headerregistry import HeaderRegistry
# from re import T
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from common.models import Group

# Create your models here.
class Content(models.Model):
    author=models.CharField(max_length=50,verbose_name='작성자',blank=True)
    author_id=models.CharField(max_length=15,verbose_name='작성자 id',blank=True)
    date=models.PositiveIntegerField(default=1,verbose_name='작성 날짜',validators=[MaxValueValidator(1000000)])#220813형태로만 입력
    retweets=models.BigIntegerField(verbose_name='리트윗',validators=[MinValueValidator(0)])
    replies=models.BigIntegerField(verbose_name='답장',validators=[MinValueValidator(0)])
    hearts=models.BigIntegerField(verbose_name='좋아요',validators=[MinValueValidator(0)])
    images=models.ImageField(blank=True, null=True,verbose_name='사진', upload_to='images')
    gifs=models.FileField(blank=True,null=True,verbose_name='gif',upload_to='gifs')
    group=models.ForeignKey(Group,on_delete=models.CASCADE) #무엇에 대한 콘텐츠인가?

    def __str__(self) :
        return self.author
    
    class Meta : 
        db_table = 'content_table'
        verbose_name = '콘텐츠'
        verbose_name_plural = '콘텐츠'


class Notice(models.Model):
    author=models.ForeignKey(Group,on_delete=models.CASCADE)#그룹모델과 연결
    notices=models.TextField(max_length=200)
    
    def __str__(self) :
        return self.author
    
    class Meta : 
        db_table = 'notice_table'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'

    

class Fantweet(models.Model):
    author=models.CharField(max_length=50,verbose_name='작성자',blank=True)
    author_id=models.CharField(max_length=15,verbose_name='작성자 id',blank=True)
    date=models.PositiveIntegerField(default=1,verbose_name='작성 날짜',validators=[MaxValueValidator(1000000)])#220813형태로만 입력
    retweets=models.BigIntegerField(verbose_name='리트윗',validators=[MinValueValidator(0)])
    replies=models.BigIntegerField(verbose_name='답장',validators=[MinValueValidator(0)])
    hearts=models.BigIntegerField(verbose_name='좋아요',validators=[MinValueValidator(0)])
    group=models.ForeignKey(Group,on_delete=models.CASCADE) #무엇에 대한 콘텐츠인가?
    
    def __str__(self) :
        return self.author

    class Meta : 
        db_table = 'fantweet_table'
        verbose_name = '팬트윗'
        verbose_name_plural = '팬트윗'


