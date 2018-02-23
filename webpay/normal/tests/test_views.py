from django.core.urlresolvers import reverse
from django.test import TestCase


class ViewsTest(TestCase):

    def test_verificacion(self):
        """
        Test para la vista que verifica los datos.
        """
        # No hay token debera responder un bad request
        response = self.client.post(reverse('webpay_normal_verificacion'), {})
        self.assertEqual(400, response.status_code)
