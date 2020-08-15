from django.db import models
from django.contrib.auth.models import User

from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
from meta.models import ModelMeta
from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator

class Video(ModelMeta, models.Model, HitCountMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    embed = models.TextField()
    thumbnail = models.ImageField(upload_to='contents/%Y/%m/%d/', blank=True)
    preview = models.FileField(upload_to='contents/%Y/%m/%d/', validators=[FileExtensionValidator(allowed_extensions=['webm'])], blank=True)
    keyword = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    STATUS = (
        ('A', 'Active'),
        ('I', 'Inactive')
    )
    active = models.CharField(max_length=1, choices=STATUS, default='A')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=5, null=True)
    hit_count_generic = GenericRelation(
                            HitCount, object_id_field='object_pk',
                            related_query_name='hit_count_generic_relation')
    _metadata = {
        'title': 'title',
        'description': 'keyword',
    }
    
    tags = TaggableManager()

    def __str__(self):
        return self.title
