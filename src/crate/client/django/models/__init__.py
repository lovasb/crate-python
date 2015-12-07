# -*- coding: utf-8 -*-
import time

from django.conf import settings
from django.db import models

from .fields import * #NOQA


class Model(models.Model):
    id = AutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if settings.WAIT_AFTER_SAVE:
            time.sleep(settings.WAIT_AFTER_SAVE)