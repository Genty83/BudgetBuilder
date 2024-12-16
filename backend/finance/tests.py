from rest_framework.test import APITestCase

class IncomeAPITestCase(APITestCase):
    def test_income_list(self):
        response = self.client.get('/api/incomes/')
        self.assertEqual(response.status_code, 200)
