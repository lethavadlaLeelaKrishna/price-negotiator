# API Documentation

## Price Negotiating Chatbot API

Complete API reference for integrating with the chatbot system.

---

## Base URL

```
http://localhost:8000
```

---

## Authentication

The API uses Django session-based authentication. Users must be logged in to access most endpoints.

---

## Endpoints

### 1. Product List

**Endpoint:** `GET /`

**Description:** Get all available products

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Premium Laptop",
      "description": "High-performance laptop...",
      "original_price": 1299.99,
      "minimum_price": 899.99,
      "discount_percentage": 30,
      "stock": 5
    }
  ]
}
```

---

### 2. Product Details

**Endpoint:** `GET /product/<id>/`

**Description:** Get details for a specific product

**URL Parameters:**
- `id` (integer, required) - Product ID

**Response:**
```json
{
  "id": 1,
  "name": "Premium Laptop",
  "description": "...",
  "original_price": 1299.99,
  "minimum_price": 899.99,
  "discount_percentage": 30,
  "stock": 5
}
```

---

### 3. Start Negotiation

**Endpoint:** `GET /negotiate/<product_id>/`

**Description:** Start a price negotiation session for a product

**URL Parameters:**
- `product_id` (integer, required) - Product ID

**Requirements:** User must be logged in

**Response:** HTML page with chat interface

---

### 4. Send Text Offer

**Endpoint:** `POST /shop/send-text-offer/<session_id>/`

**Description:** Send a text-based price offer

**URL Parameters:**
- `session_id` (string, required) - Negotiation session ID

**Headers:**
```
Content-Type: application/json
X-CSRFToken: <csrf_token>
```

**Request Body:**
```json
{
  "offered_price": 950.00,
  "message": "This is my best offer"
}
```

**Request Fields:**
- `offered_price` (number, required) - Price offer in INR (Indian Rupees)
- `message` (string, optional) - Additional message

**Response:**
```json
{
  "status": "success",
  "offer_status": "accepted|rejected|counter",
  "bot_response": "Great! I accept your offer at ₹950.00. You saved 27%!",
  "counter_offer": 1100.00,
  "discount": 26.8,
  "reason": "Offer accepted"
}
```

**Response Fields:**
- `status` (string) - "success" or "error"
- `offer_status` (string) - Decision: accepted, rejected, or counter
- `bot_response` (string) - Friendly bot message
- `counter_offer` (number, optional) - Counter offer price if applicable
- `discount` (number) - Discount percentage
- `reason` (string) - Explanation of decision

---

### 5. Send Voice Offer

**Endpoint:** `POST /shop/send-voice-offer/<session_id>/`

**Description:** Send a voice-based price offer

**URL Parameters:**
- `session_id` (string, required) - Negotiation session ID

**Headers:**
```
Content-Type: multipart/form-data
X-CSRFToken: <csrf_token>
```

**Form Data:**
```
audio: [WAV/MP3 file]
offered_price: 950.00
```

**Form Fields:**
- `audio` (file, required) - Audio file (WAV or MP3)
- `offered_price` (number, required) - Price offer in INR (Indian Rupees)

**Response:**
```json
{
  "status": "success",
  "offer_status": "accepted|rejected|counter",
  "bot_response": "Your message here",
  "counter_offer": 1100.00,
  "discount": 26.8,
  "message_id": 42
}
```

---

### 6. Get Chat History

**Endpoint:** `GET /shop/chat-history/<session_id>/`

**Description:** Retrieve chat history for a negotiation session

**URL Parameters:**
- `session_id` (string, required) - Negotiation session ID

**Response:**
```json
{
  "status": "success",
  "messages": [
    {
      "type": "user_text",
  "content": "My offer: ₹950.00",
      "timestamp": "2025-12-09T10:30:00Z",
      "offered_price": 950.00
    },
    {
      "type": "bot_text",
      "content": "I accept your offer!",
      "timestamp": "2025-12-09T10:30:05Z",
      "offered_price": null
    }
  ]
}
```

**Message Types:**
- `user_text` - Text message from user
- `user_voice` - Voice message from user
- `bot_text` - Text response from bot
- `bot_voice` - Voice response from bot

---

### 7. Add to Cart

**Endpoint:** `POST /shop/add-to-cart/<session_id>/`

**Description:** Add negotiated product to shopping cart

**URL Parameters:**
- `session_id` (string, required) - Negotiation session ID

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: <csrf_token>
```

**Form Data:**
```
quantity: 1
```

**Requirements:** 
- User must be logged in
- Negotiation must have status "accepted"

**Response:**
```json
{
  "status": "success",
  "message": "Added to cart",
  "cart_total": 1850.50
}
```

---

### 8. View Cart

**Endpoint:** `GET /cart/`

**Description:** View shopping cart

**Requirements:** User must be logged in

**Response:** HTML page with cart contents

---

### 9. Checkout

**Endpoint:** `GET /checkout/`

**Description:** View checkout page

**Requirements:** User must be logged in and cart must have items

**Response:** HTML page with checkout form

**POST** - Process checkout:

```
POST /checkout/
```

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-CSRFToken: <csrf_token>
```

**Response:** Success page with order summary

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "status": "error",
  "message": "Description of what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request successful
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Not logged in
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Example Workflow

### Complete Negotiation Flow

```
1. GET /                                  → Browse products
2. GET /product/1/                        → View product details
3. GET /negotiate/1/                      → Start negotiation (creates session)
4. POST /shop/send-text-offer/abc123/     → Offer ₹900
5. GET /shop/chat-history/abc123/         → View conversation
6. POST /shop/send-text-offer/abc123/     → Offer ₹950
7. POST /shop/add-to-cart/abc123/         → Add to cart (if accepted)
8. GET /cart/                             → View cart
9. POST /checkout/                        → Complete purchase
```

---

## Rate Limiting

Currently no rate limiting is enforced. For production, consider implementing:
- Request throttling per IP
- Session-based limits
- API key limits

---

## CORS Settings

CORS is enabled for:
- `http://localhost:8000`
- `http://127.0.0.1:8000`

To add more origins, edit `chatbot/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://yourdomain.com',
]
```

---

## Pagination

Not currently implemented. All products are returned without pagination.

For large datasets, consider adding pagination:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

---

## Filtering

Not currently implemented through API. Use Django admin for now.

---

## Webhook Events

Future enhancement: Notify external services of negotiation events

```
Events:
- negotiation.started
- negotiation.offer_made
- negotiation.accepted
- negotiation.rejected
- purchase.completed
```

---

## SDKs

Currently only JavaScript/HTML is available. Future SDKs:
- Python
- JavaScript/Node.js
- PHP
- Ruby

---

## Changelog

### v1.0 (2025-12-09)
- Initial release
- Text and voice negotiation
- Cart and checkout integration
- Admin dashboard

---

## Support

For API issues:
1. Check the error message
2. Verify authentication
3. Confirm session exists
4. Check database is running
5. Review logs for details

---

**Last Updated:** 2025-12-09
