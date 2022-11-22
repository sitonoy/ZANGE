from django.db import models
from django.utils import timezone

class ZangeModel(models.Model):

  date = models.DateField('投稿日',default=timezone.now)
  title = models.CharField('タイトル',max_length=100)
  text = models.TextField('コンテンツ')
  id = models.AutoField(primary_key=True)
  url = models.URLField('URL',null=True)

  def __str__(self):
    return self.title

