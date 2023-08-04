from unittest import TestCase

from .oidc import SignData, SignMetadata


class OIDCSchemaTest(TestCase):

    def test_empty_create_with_metadata(self):
        payload = {
            'data': {},
            'metadata': {
                'duration': 15 * 60,
                'audience': 'test'
            }
        }
        actual = SignData.model_validate(payload)
        expected = SignData(data=dict(), metadata=SignMetadata(duration=900, audience='test'))
        self.assertEqual(expected, actual)

    def test_metadata_overlap(self):
        a = SignData(data={'uid': 1})
        b = SignData(data={'uid': 2})
        b.metadata.duration = 60
        self.assertNotEqual(a.metadata, b.metadata)
