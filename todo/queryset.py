import datetime

from django.db import models

class TodoListQuerySet(models.QuerySet):
    def get_expired_list(self):
        return self.filter(is_done=False, 
            deadline__lt=datetime.date.today())
    
    def get_incomplete_list(self):
        return self.filter(models.Q(is_done = False)&
            (
                models.Q(deadline__gte=datetime.date.today())|
                models.Q(deadline__isnull=True)
            )
        )

    def get_complete_list(self):
        return self.filter(is_done=True)