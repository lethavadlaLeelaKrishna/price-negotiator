from shop.negotiation_engine import parse_price_from_text

examples = [
    "I can pay five hundred rupees",
    "₹1,299.50 please",
    "I'll do 2000",
    "one thousand two hundred thirty four",
    "no number here"
]

for e in examples:
    print(f"{e} -> {parse_price_from_text(e)}")
