import unittest
import requests
from app import api_urls, average_strategy, minimum_deductible_strategy

class TestCoalescingStrategies(unittest.TestCase):
    def setUp(self):
        self.responses = [
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
            {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
        ]

    def test_average_strategy(self):
        expected_output = {
            'deductible': 1066,
            'stop_loss': 11000,
            'oop_max': 5666
        }
        self.assertEqual(average_strategy(self.responses), expected_output)

    def test_minimum_deductible_strategy(self):
        expected_output = {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000}
        self.assertEqual(minimum_deductible_strategy(self.responses), expected_output)

class TestAPIs(unittest.TestCase):

    def test_missing_member_id(self):
        response = requests.get('http://127.0.0.1:5000/api/coalesce')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['error'], 'Missing member_id')

    def test_api1(self):
        response = requests.get(api_urls[0], params={'member_id': 123})
        data = response.json()
        self.assertEqual(data['deductible'], 1000)
        self.assertEqual(data['stop_loss'], 10000)
        self.assertEqual(data['oop_max'], 5000)

    def test_api2(self):
        response = requests.get(api_urls[1], params={'member_id': 123})
        data = response.json()
        self.assertEqual(data['deductible'], 1200)
        self.assertEqual(data['stop_loss'], 13000)
        self.assertEqual(data['oop_max'], 6000)

    def test_api3(self):
        response = requests.get(api_urls[2], params={'member_id': 123})
        data = response.json()
        self.assertEqual(data['deductible'], 1000)
        self.assertEqual(data['stop_loss'], 10000)
        self.assertEqual(data['oop_max'], 6000)

    def test_average_strategy(self):
        responses = [
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
            {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
        ]
        coalesced_data = average_strategy(responses)
        self.assertEqual(coalesced_data['deductible'], 1066)
        self.assertEqual(coalesced_data['stop_loss'], 11000)
        self.assertEqual(coalesced_data['oop_max'], 5666)

    def test_minimum_deductible_strategy(self):
        responses = [
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 5000},
            {'deductible': 1200, 'stop_loss': 13000, 'oop_max': 6000},
            {'deductible': 1000, 'stop_loss': 10000, 'oop_max': 6000},
        ]
        coalesced_data = minimum_deductible_strategy(responses)
        self.assertEqual(coalesced_data['deductible'], 1000)
        self.assertEqual(coalesced_data['stop_loss'], 10000)
        self.assertEqual(coalesced_data['oop_max'], 5000)

    def test_coalesce_average_strategy(self):
        response = requests.get('http://127.0.0.1:5000/api/coalesce', params={'member_id': 123, 'strategy': 'average'})
        data = response.json()
        self.assertEqual(data['deductible'], 1066)
        self.assertEqual(data['stop_loss'], 11000)
        self.assertEqual(data['oop_max'], 5666)

    def test_coalesce_minimum_deductible_strategy(self):
        response = requests.get('http://127.0.0.1:5000/api/coalesce', params={'member_id': 123, 'strategy': 'minimum_deductible'})
        data = response.json()
        self.assertEqual(data['deductible'], 1000)
        self.assertEqual(data['stop_loss'], 10000)
        self.assertEqual(data['oop_max'], 5000)


if __name__ == '__main__':
    unittest.main()
