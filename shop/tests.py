from django.test import TestCase, Client, SimpleTestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from decimal import Decimal

from .models import Product, NegotiationSession, Cart, CartItem
from .models import Order
from .negotiation_engine import _words_to_num


class VoiceOfferTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='tester', password='testpass')
        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            original_price=100.00,
            minimum_price=10.00,
            discount_percentage=20,
            stock=5
        )
        # Create negotiation session
        self.session = NegotiationSession.objects.create(
            user=self.user,
            product=self.product,
            session_id='testsession',
            original_price=self.product.original_price
        )
        self.client = Client()

    def test_send_voice_offer(self):
        # Login required by view that creates negotiation (negotiation_chatbot) but send_voice_offer is csrf_exempt
        self.client.login(username='tester', password='testpass')

        # Prepare a small dummy audio file
        audio_bytes = b"RIFF....WAVEfmt "
        uploaded = SimpleUploadedFile('voice_offer.wav', audio_bytes, content_type='audio/wav')

        url = reverse('shop:send_voice_offer', args=[self.session.session_id])
        response = self.client.post(url, {'audio': uploaded, 'offered_price': '19.99'})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertIn(data['status'], ['success', 'error'])


class AddToCartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.product = Product.objects.create(
            name='Test Product',
            description='A product for testing',
            original_price=100.00,
            minimum_price=10.00,
            discount_percentage=20,
            stock=5
        )
        # Create a negotiation with accepted status
        self.session = NegotiationSession.objects.create(
            user=self.user,
            product=self.product,
            session_id='testsession',
            original_price=self.product.original_price,
            status='accepted',
            final_agreed_price=75.00,
            discount_percentage=25.0
        )
        self.client = Client()

    def test_add_to_cart_with_negotiation(self):
        """Test adding negotiated product to cart"""
        self.client.login(username='tester', password='testpass')

        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        response = self.client.post(url, {'quantity': 2})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('cart_total', data)

    def test_cart_total_calculation(self):
        """Test cart total with negotiated prices"""
        self.client.login(username='tester', password='testpass')

        # Add negotiated product to cart
        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        response = self.client.post(url, {'quantity': 2})
        self.assertEqual(response.status_code, 200)

        # Check cart page
        cart_url = reverse('shop:view_cart')
        response = self.client.get(cart_url)
        self.assertEqual(response.status_code, 200)

        # Verify context has correct total (2 * 75.00 = 150.00)
        expected_total = 150.0
        context_total = float(response.context['total'])
        self.assertAlmostEqual(context_total, expected_total, places=2)

    def test_tax_calculation(self):
        """Test 10% tax calculation"""
        self.client.login(username='tester', password='testpass')

        # Add negotiated product to cart
        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        self.client.post(url, {'quantity': 2})

        # Check cart page
        cart_url = reverse('shop:view_cart')
        response = self.client.get(cart_url)

        # Verify tax is 10% of total
        total = float(response.context['total'])
        tax = float(response.context['tax'])
        expected_tax = total * 0.1
        self.assertAlmostEqual(tax, expected_tax, places=2)

    def test_final_total_calculation(self):
        """Test final total = total + 10% tax"""
        self.client.login(username='tester', password='testpass')

        # Add negotiated product to cart
        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        self.client.post(url, {'quantity': 2})

        # Check cart page
        cart_url = reverse('shop:view_cart')
        response = self.client.get(cart_url)

        # Verify final_total = total * 1.1
        total = float(response.context['total'])
        final_total = float(response.context['final_total'])
        expected_final = total * 1.1
        self.assertAlmostEqual(final_total, expected_final, places=2)

    def test_checkout_view_calculations(self):
        """Test checkout view calculates tax and final_total"""
        self.client.login(username='tester', password='testpass')

        # Add negotiated product to cart
        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        self.client.post(url, {'quantity': 1})

        # Check checkout page (GET)
        checkout_url = reverse('shop:checkout')
        response = self.client.get(checkout_url)
        self.assertEqual(response.status_code, 200)

        # Verify context has tax and final_total
        self.assertIn('tax', response.context)
        self.assertIn('final_total', response.context)
        
        total = float(response.context['total'])
        tax = float(response.context['tax'])
        final_total = float(response.context['final_total'])

        self.assertAlmostEqual(tax, total * 0.1, places=2)
        self.assertAlmostEqual(final_total, total * 1.1, places=2)

    def test_checkout_post_and_success_page(self):
        """Test checkout POST and success page with final_total"""
        self.client.login(username='tester', password='testpass')

        # Add negotiated product to cart
        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        self.client.post(url, {'quantity': 1})

        # POST to checkout
        checkout_url = reverse('shop:checkout')
        response = self.client.post(checkout_url)
        self.assertEqual(response.status_code, 200)

        # Verify we get success page with final_total
        self.assertIn('final_total', response.context)
        self.assertIn('success', response.context)
        self.assertTrue(response.context['success'])

    def test_order_created_and_invoice_saved(self):
        """Ensure checkout creates an Order and saves an invoice file"""
        self.client.login(username='tester', password='testpass')

        # Add negotiated product to cart
        url = reverse('shop:add_to_cart_with_negotiation', args=[self.session.session_id])
        self.client.post(url, {'quantity': 1})

        # POST to checkout
        checkout_url = reverse('shop:checkout')
        response = self.client.post(checkout_url)
        self.assertEqual(response.status_code, 200)

        # Check an order was created
        orders = Order.objects.filter(user=self.user)
        self.assertTrue(orders.exists())
        order = orders.first()

        # Invoice file should be present and have a filename
        self.assertIsNotNone(order.invoice_file)
        self.assertTrue(bool(order.invoice_file.name))


class WordsToNumTestCase(SimpleTestCase):
    def test_fractional_zero_handling(self):
        """Test that fractional parts with leading zeros are parsed correctly"""
        # "point zero five" -> 0.05
        result = _words_to_num("point zero five")
        self.assertEqual(result, Decimal('0.05'), "Should parse 'point zero five' as 0.05")

    def test_fractional_simple(self):
        # "point five" -> 0.5
        result = _words_to_num("point five")
        self.assertEqual(result, Decimal('0.5'))
        
    def test_fractional_two_digits(self):
        # "point five zero" -> 0.50
        result = _words_to_num("point five zero")
        self.assertEqual(result, Decimal('0.50'))
