from django.db import models
from settings import JAYA_CONFIG
from django.conf import settings
import os
import json

fixture_dir = JAYA_CONFIG.get('FIXTURE_DIR', settings.PROJECT_ROOT + "/jaya/fixtures")


class BlogPostCount(models.Model):
    counter = models.IntegerField()
    fixture_path = models.FilePathField(path=fixture_dir, match="*.json")

    def fixture_exists(self):
        if self.fixture_path not in [f for f in os.listdir(fixture_dir) if os.path.isfile(fixture_dir + "/" + f)]:
            return True
        return False

    def is_deleted(self):
        """
        compare the primary key of each object in the fixtures directory with the
        counter field to check if the fixture still exists
        :return:
        """
        fixtures = [f for f in os.listdir(fixture_dir) if os.path.isfile(fixture_dir + "/" + f)]
        match = False
        for fixture in BlogPostCount.objects.all():
            for f in fixtures:
                post = json.load(fixture_dir + "/" + f, encoding='utf8')
                if fixture.counter == post['pk']:
                    match = True
        return match

