# from django.db import models

#  # Create your models here.

# # # 그룹
# class Group(models.Model) : 
#     name = models.CharField(max_length=20, verbose_name='그룹이름')
#     tag1 = models.CharField(max_length=100, verbose_name='그룹태그1', blank=True)
#     tag2 = models.CharField(max_length=100, verbose_name='그룹태그2', blank=True)
#     tag3 = models.CharField(max_length=100, verbose_name='그룹태그3', blank=True)
#     tag4 = models.CharField(max_length=100, verbose_name='그룹태그4', blank=True)
#     tag5 = models.CharField(max_length=100, verbose_name='그룹태그5', blank=True)      

#     def __str__(self) :
#          return self.name

#     class Meta : 
#         db_table = 'Group_table'
#         verbose_name = '그룹'
#         verbose_name_plural = '그룹'


# # # 그룹별 멤버
# class Member(models.Model) :
#     name = models.CharField(max_length=20, verbose_name='멤버이름')
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     tag1 = models.CharField(max_length=100, verbose_name='멤버태그1', blank=True)
#     tag2 = models.CharField(max_length=100, verbose_name='멤버태그2', blank=True)
#     tag3 = models.CharField(max_length=100, verbose_name='멤버태그3', blank=True)
#     tag4 = models.CharField(max_length=100, verbose_name='멤버태그4', blank=True)
#     tag5 = models.CharField(max_length=100, verbose_name='멤버태그5', blank=True)
    
#     def __str__(self) :
#         return self.name

#     class Meta : 
#         db_table = 'Member_table'
#         verbose_name = '멤버'
#         verbose_name_plural = '멤버'




