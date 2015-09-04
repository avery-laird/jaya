# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jaya', '0002_blogpostcount_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpostcount',
            name='fixture_path',
            field=models.FilePathField(default='test', path=b'/home/avery/Websites/averylaird.com/project/jaya/fixtures', match=b'*.json'),
            preserve_default=False,
        ),
    ]
