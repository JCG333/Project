'''
Filename: api_test.py

This is the unit test script for the API. It contains the tests that will be run against the API. The tests are:
    - test_region: tests for the region filter
    - test_park: tests for the park filter
    - test_parkAndRegion: tests for the park and region filters
    - test_noFilters: tests for no filters
'''
import unittest
import requests

# Define test case for the script
class TestSearchEndpoint(unittest.TestCase):

    # Define the base URL for all API endpoints
    BASE_URL = 'http://api:4000'  

    # Test 1: testing for region filter
    def test_region(self):

        # Define the filters for the test request
        filters = {
            'company': 'Company1',
            'region': 'Region1',
            'park': ' '
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('turbines', data)
        self.assertIsInstance(data['turbines'], list)
        self.assertTrue(data['turbines'])
        for turbine in data['turbines']:

            # Check that each turbine has the expected keys
            self.assertIn('turbine', turbine)
            self.assertIn('company_id', turbine)
            self.assertIn('region_id', turbine)
            self.assertIn('park_id', turbine)

            # Check that the turbine has the expected values
            self.assertIn(turbine['turbine'], ['Turbine1', 'Turbine2'])
            self.assertEqual(turbine['company_id'], 1) 
            self.assertEqual(turbine['region_id'], 1) 
            # could change if default entries are changed 

    # Test 2: testing for park filter
    def test_park(self):

        # Define the parameters for the test request
        filters = {
            'company': 'Company1',
            'region': ' ',
            'park': 'Park1',
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('turbines', data)
        self.assertIsInstance(data['turbines'], list)
        self.assertTrue(data['turbines'])
        for turbine in data['turbines']:

            # Check that each image has the expected keys
            self.assertIn('turbine', turbine)
            self.assertIn('company_id', turbine)
            self.assertIn('region_id', turbine)
            self.assertIn('park_id', turbine)

            # Check that the image has the expected values
            self.assertEqual(turbine['turbine'], 'Turbine1')
            self.assertEqual(turbine['company_id'], 1)
            self.assertEqual(turbine['park_id'], 1)

    # Test 3: testing for park and region filters
    def test_parkAndRegion(self):

        # Define the parameters for the test request
        filters = {
            'company': 'Company1',
            'region': 'Region1',
            'park': 'Park1'
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('turbines', data)
        self.assertIsInstance(data['turbines'], list)
        self.assertTrue(data['turbines'])
        for turbine in data['turbines']:

            # Check that each image has the expected keys
            self.assertIn('company_id', turbine)
            self.assertIn('region_id', turbine)
            self.assertIn('park_id', turbine)
            self.assertIn('turbine', turbine)

            # Check that the image has the expected values
            self.assertEqual(turbine['turbine'], 'Turbine1')
            self.assertEqual(turbine['company_id'], 1)
            self.assertEqual(turbine['park_id'], 1)
            self.assertEqual(turbine['region_id'], 1) 

    # Test 4: testing for no filters
    def test_noFilters(self):

        # Define the parameters for the test request
        filters = {
            'company': 'Company1',
            'region': ' ',
            'park': ' '
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('turbines', data)
        self.assertIsInstance(data['turbines'], list)
        self.assertTrue(data['turbines'])
        for turbine in data['turbines']:

            # Check that each image has the expected keys
            self.assertIn('company_id', turbine)
            self.assertIn('region_id', turbine)
            self.assertIn('park_id', turbine)
            self.assertIn('turbine', turbine)

if __name__ == '__main__':
    unittest.main()