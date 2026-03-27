from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal

from .negotiation_engine import parse_price_from_text
from .models import Product, NegotiationSession


class NLPParserTests(TestCase):
    def test_parse_numbers(self):
        cases = {
            'I can pay five hundred rupees': Decimal(500),
            '₹1,299.50 please': Decimal('1299.50'),
            'I will give one thousand two hundred': Decimal(1200),
            'one point five': Decimal('1.5'),
            'twenty-five': Decimal(25),
            'no number here': None,
        }

        for text, expected in cases.items():
            parsed = parse_price_from_text(text)
            if expected is None:
                self.assertIsNone(parsed, msg=text)
            else:
                # parsed may be Decimal
                self.assertIsNotNone(parsed, msg=text)
                self.assertAlmostEqual(parsed, expected, places=2, msg=text)


class SendTextOfferNLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='nlpuser', password='nlppass')
        self.product = Product.objects.create(
            name='NLP Product', description='Test', original_price=1000.0,
            minimum_price=100.0, discount_percentage=30, stock=5
        )
        # create negotiation session for this user
        self.session = NegotiationSession.objects.create(
            user=self.user, product=self.product, session_id='nlpsession', original_price=self.product.original_price
        )
        self.client = Client()

    def test_send_text_offer_with_words(self):
        self.client.login(username='nlpuser', password='nlppass')
        url = reverse('shop:send_text_offer', args=[self.session.session_id])  
        payload = {'message': 'I can offer five hundred rupees'}
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertIn(response.status_code, (200, 201))
        data = response.json()
        self.assertIn('status', data)
        self.assertIn(data['status'], ('success', 'error'))
