# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from tests.apidocs.util import APIDocsTestCase


class OrganizationGroupDocs(APIDocsTestCase):
    endpoint = "sentry-api-0-organization-group-index"

    def setUp(self):
        project = self.create_project(name="foo")
        self.repo = self.create_repo(project=project, name=project.name)
        self.commit = self.create_commit(project=project, repo=self.repo)

        self.url = reverse(self.endpoint, args=[project.organization.slug])
        self.login_as(user=self.user)

    def test_get(self):
        response = self.client.get(self.url)
        request = RequestFactory().get(self.url)

        self.validate_schema(request, response)

    def test_put(self):
        data = {
            "status": "resolved",
            "statusDetails": {
                "inCommit": {"commit": self.commit.key, "repository": self.repo.name},
            },
        }
        response = self.client.put(self.url, data=data, format="json")
        request = RequestFactory().put(self.url, data)

        self.validate_schema(request, response)

    def test_delete(self):
        response = self.client.delete(self.url)
        request = RequestFactory().delete(self.url)

        self.validate_schema(request, response)
