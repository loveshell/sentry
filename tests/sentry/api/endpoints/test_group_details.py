from django.core.urlresolvers import reverse
from sentry.constants import STATUS_RESOLVED
from sentry.models import Group
from sentry.testutils import APITestCase


class GroupDetailsTest(APITestCase):
    def test_simple(self):
        self.client.force_authenticate(user=self.user)

        group = self.create_group()

        url = reverse('sentry-api-0-group-details', kwargs={
            'project_id': self.project.slug,
            'team_slug': self.team.slug,
            'group_id': group.id,
        })
        response = self.client.get(url, format='json')

        assert response.status_code == 200, response.content
        assert response.data['id'] == group.id


class GroupUpdateTest(APITestCase):
    def test_simple(self):
        self.client.force_authenticate(user=self.user)

        group = self.create_group()

        url = reverse('sentry-api-0-group-details', kwargs={
            'project_id': self.project.slug,
            'team_slug': self.team.slug,
            'group_id': group.id,
        })
        response = self.client.put(url, data={
            'status': 'resolved',
        }, format='json')

        assert response.status_code == 200, response.content

        group = Group.objects.get(id=group.id)

        assert group.status == STATUS_RESOLVED
