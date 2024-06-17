import unittest
from unittest.mock import patch, MagicMock
from web_monitor.checker import WebsiteChecker

class TestWebsiteChecker(unittest.TestCase):

    @patch('web_monitor.checker.requests.get')
    def test_check_valid_url(self, mock_get):
        # Mock a successful HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.elapsed.total_seconds.return_value = 0.123
        mock_response.text = '<html><title>Example Domain</title></html>'
        mock_get.return_value = mock_response

        checker = WebsiteChecker('https://example.com', regex='<title>Example Domain</title>')
        result = checker.check()

        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['status_code'], 200)
        self.assertAlmostEqual(result['response_time'], 0.123, places=3)
        self.assertTrue(result['content_match'])

    @patch('web_monitor.checker.requests.get')
    def test_check_invalid_url(self, mock_get):
        # Mock a failed HTTP response
        mock_get.side_effect = Exception("Connection error")

        checker = WebsiteChecker('https://invalidurl')
        result = checker.check()

        self.assertEqual(result['url'], 'https://invalidurl')
        self.assertIsNone(result['response_time'])
        self.assertIsNone(result['status_code'])
        self.assertIsNone(result['content_match'])
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main()
