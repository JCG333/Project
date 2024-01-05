'''
Filename: api-test.py

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
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('images', data)
        self.assertIsInstance(data['images'], list)
        self.assertTrue(data['images'])
        for image in data['images']:

            # Check that each image has the expected keys
            self.assertIn('url', image)
            self.assertIn('company', image)
            self.assertIn('region', image)
            self.assertIn('park', image)
            self.assertIn('turbine', image)

            # Check that the image has the expected values
            self.assertEqual(image['company'], 'Company1')
            self.assertEqual(image['region'], 'Region1')

    # Test 2: testing for park filter
    def test_park(self):

        # Define the parameters for the test request
        filters = {
            'company': 'Company1',
            'park': 'Park1',
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('images', data)
        self.assertIsInstance(data['images'], list)
        self.assertTrue(data['images'])
        for image in data['images']:

            # Check that each image has the expected keys
            self.assertIn('url', image)
            self.assertIn('company', image)
            self.assertIn('region', image)
            self.assertIn('park', image)
            self.assertIn('turbine', image)

            # Check that the image has the expected values
            self.assertEqual(image['company'], 'Company1')
            self.assertEqual(image['park'], 'Park1')

    # Test 3: testing for park and region filters
    def test_parkAndRegion(self):

        # Define the parameters for the test request
        filters = {
            'company': 'Company1',
            'region': 'Region1',
            'park': 'Park3'
        }

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('images', data)
        self.assertIsInstance(data['images'], list)
        self.assertTrue(data['images'])
        for image in data['images']:

            # Check that each image has the expected keys
            self.assertIn('url', image)
            self.assertIn('company', image)
            self.assertIn('region', image)
            self.assertIn('park', image)
            self.assertIn('turbine', image)

            # Check that the image has the expected values
            self.assertEqual(image['company'], 'Company1')
            self.assertEqual(image['region'], 'Region1')
            self.assertEqual(image['park'], 'Park3')

    # Test 4: testing for no filters
    def test_noFilters(self):

        # Define the parameters for the test request
        filters = {}

        # Send a GET request to the /search endpoint
        response = requests.post(f'{self.BASE_URL}/search', json=filters)

        # Check that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Parse the response body as JSON
        data = response.json()

        # Check that the response contains the expected data
        self.assertIn('images', data)
        self.assertIsInstance(data['images'], list)
        self.assertTrue(data['images'])
        for image in data['images']:

            # Check that each image has the expected keys
            self.assertIn('url', image)
            self.assertIn('company', image)
            self.assertIn('region', image)
            self.assertIn('park', image)
            self.assertIn('turbine', image)

if __name__ == '__main__':
    unittest.main()