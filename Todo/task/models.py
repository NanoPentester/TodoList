from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=255 , null= False , blank= False , db_index=True)
    desc = models.TextField(default="")
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=False , blank=False , related_name= 'tasks' , default='')
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"