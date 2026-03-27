"""
Price Negotiation Engine
Implements AI decision logic for accepting/rejecting price offers
"""
from decimal import Decimal
from datetime import datetime, timedelta
from .models import PriceOffer, NegotiationSession
import re
import hashlib


_NUM_WORDS = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
    'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
    'hundred': 100, 'thousand': 1000, 'million': 1000000
}


def _words_to_num(text):
    """Convert number words in English up to millions into an integer.

    This is a small helper to support phrases like "five hundred twenty"
    or "one thousand two hundred". It returns None when no number words
    are detected.
    """
    tokens = re.findall(r"[a-z]+", text.lower())
    if not tokens:
        return None

    total = 0
    current = 0
    found = False

    i = 0
    while i < len(tokens):
        t = tokens[i]
        # skip currency words and filler words
        if t in ('rupees', 'rupee', 'rs', 'rs.', 'dollars', 'dollar', 'and'):
            i += 1
            continue

        # handle decimal point expressed as the word 'point'
        if t == 'point':
            # build fractional part from subsequent number words
            frac_str = ''
            j = i + 1
            while j < len(tokens) and tokens[j] in _NUM_WORDS:
                # map small numbers to single digits when possible
                digit = _NUM_WORDS.get(tokens[j], 0)
                # if number word > 9, append its numeric form directly
                frac_str += str(digit)
                j += 1
            try:
                if frac_str:
                    # combine current and fractional
                    return total + current + Decimal('0.' + frac_str)
            except Exception:
                pass
            break

        if t not in _NUM_WORDS:
            i += 1
            continue

        found = True
        val = _NUM_WORDS[t]
        if val == 100:
            if current == 0:
                current = 1
            current *= 100
        elif val >= 1000:
            if current == 0:
                current = 1
            total += current * val
            current = 0
        else:
            current += val

        i += 1

    if not found:
        return None

    return total + current


def parse_price_from_text(text):
    """Extract a price from free text using regex and simple word parsing.

    Returns a Decimal or None when parsing fails.
    """
    if not text or not isinstance(text, str):
        return None

    # 1) Try to find explicit numbers like "₹1,200.50" or "1200" or "$1,200"
    m = re.search(r"[₹$]?\s*([0-9]{1,3}(?:[,0-9]{0,3})*(?:\.[0-9]+)?)", text)
    if m:
        num_text = m.group(1).replace(',', '')
        try:
            return Decimal(num_text)
        except Exception:
            pass

    # 2) Try to parse number words
    wn = _words_to_num(text)
    if wn is not None:
        return Decimal(wn)

    return None


class PriceNegotiationEngine:
    """
    AI/Rule-based engine for evaluating price negotiations
    Considers multiple factors to make intelligent acceptance decisions
    """
    
    def __init__(self, session):
        self.session = session
        self.product = session.product
        self.original_price = session.original_price
        self.minimum_price = session.product.minimum_price
        self.max_discount = session.product.discount_percentage
        # Global acceptance ratio: accept any offer >= this fraction of original_price
        # Dynamic acceptance ratio based on session ID to vary between 10%, 20%, 40% discounts
        # (meaning pay 90%, 80%, 60% of original price)
        
        # Calculate a deterministic index based on session_id
        session_hash = hashlib.md5(str(session.session_id).encode('utf-8')).hexdigest()
        hash_int = int(session_hash, 16)
        
        # Options: 0.90 (10% discount), 0.80 (20% discount), 0.60 (40% discount)
        threshold_options = [Decimal('0.90'), Decimal('0.80'), Decimal('0.60')]
        
        self.global_accept_ratio = threshold_options[hash_int % len(threshold_options)]

    def parse_price_from_text(self, text):
        """Instance wrapper around module-level parse_price_from_text for convenience."""
        return parse_price_from_text(text)
        
    def evaluate_offer(self, offered_price):
        """
        Evaluate a price offer and decide acceptance
        
        Decision factors:
        - Is price above minimum acceptable price
        - Discount percentage vs maximum allowed
        - Previous offer history (learning)
        - Time spent negotiating
        - User negotiation intensity
        
        Returns: dict with decision, reason, counter offer
        """
        offered_price = Decimal(str(offered_price))
        discount = self._calculate_discount_percentage(offered_price)

        # Global acceptance short-circuit: if offered meets or exceeds the
        # global acceptance threshold, accept immediately without further DB checks.
        try:
            min_accept_price = (Decimal(self.original_price) * self.global_accept_ratio).quantize(Decimal('0.01'))
        except Exception:
            min_accept_price = None

        if min_accept_price is not None and offered_price >= min_accept_price:
            percentage_val = int(self.global_accept_ratio * 100)
            decision_data = {
                'offered_price': offered_price,
                'discount_percentage': float(discount),
                'factors': {f'meets_global_{percentage_val}_threshold': True},
                'status': 'accepted',
                'reason': f'✓ Offer accepted — meets the {percentage_val}% threshold (₹{min_accept_price:.2f}).'
            }
            return decision_data
        
        # Get decision based on multiple factors
        decision_data = {
            'offered_price': offered_price,
            'discount_percentage': float(discount),
            'factors': {}
        }
        
        # Factor 1: Price bounds checking
        if offered_price < self.minimum_price:
            decision_data['factors']['below_minimum'] = True
            decision_data['factors']['severity'] = 'critical'
        elif offered_price >= self.original_price:
            decision_data['factors']['no_discount'] = True
            decision_data['status'] = 'accepted'
            decision_data['reason'] = '✓ No discount needed - paying full price!'
            return decision_data
        
        # Factor 2: Discount percentage analysis
        if discount > self.max_discount:
            decision_data['factors']['exceeds_max_discount'] = True
        
        # Factor 3: Check negotiation history
        previous_offers = PriceOffer.objects.filter(
            session=self.session
        ).order_by('-created_at')
        
        decision_data['factors']['offer_count'] = previous_offers.count()
        decision_data['factors']['offer_trend'] = self._analyze_offer_trend(
            previous_offers, offered_price
        )
        
        # Factor 4: Session duration
        time_spent = self._get_negotiation_time()
        decision_data['factors']['time_spent_minutes'] = time_spent.total_seconds() / 60
        
        # Factor 5: Calculate confidence score
        confidence_score = self._calculate_confidence_score(decision_data, time_spent)
        decision_data['factors']['confidence_score'] = confidence_score
        
        # Make final decision
        return self._make_decision(decision_data)

    def evaluate_offer_from_text(self, text):
        """Evaluate an offer given as free text.

        Special handling: if the user explicitly sends an '85' offer (e.g. '85',
        '85%', '85 percent', 'offer 85') we interpret this as a request to pay
        85% of the original price (i.e. 15% discount) and accept that deal.
        This method falls back to normal parsing when no special token is found.
        """
        if not text or not isinstance(text, str):
            return {'status': 'error', 'reason': 'No valid text provided'}

        t = text.lower()

        # Detect explicit 85 variants (standalone 85, '85%', '85 percent', etc.)
        if re.search(r"\b85\b", t) or re.search(r"\b85%\b", t) or '85 percent' in t or 'eighty five' in t:
            # Interpret as 85% of original price (i.e., user will pay 85% of original)
            offered_price = (Decimal(self.original_price) * Decimal('0.85')).quantize(Decimal('0.01'))

            # Build a direct acceptance decision (force accept for explicit 85 requests)
            decision_data = {
                'offered_price': offered_price,
                'discount_percentage': float(self._calculate_discount_percentage(offered_price)),
                'factors': {'explicit_85_request': True},
                'status': 'accepted',
                'reason': '✓ Offer accepted at 85% as requested.'
            }
            return decision_data

        # Otherwise try to parse a price or percentage from the text
        parsed = self.parse_price_from_text(text)
        if parsed is None:
            return {'status': 'error', 'reason': 'Could not parse offer from text'}

        return self.evaluate_offer(parsed)
    
    def _calculate_discount_percentage(self, offered_price):
        """Calculate discount percentage from offered price"""
        if self.original_price == 0:
            return Decimal(0)
        discount = ((self.original_price - offered_price) / self.original_price) * 100
        return max(Decimal(0), discount)  # Don't go below 0
    
    def _analyze_offer_trend(self, previous_offers, current_price):
        """
        Analyze if user is getting closer to acceptable price or being stubborn
        Returns: 'improving', 'stable', 'regressing'
        """
        if previous_offers.count() < 2:
            return 'first_offers'
        
        last_offer = previous_offers[0].offered_price
        second_last = previous_offers[1].offered_price if previous_offers.count() > 1 else None
        
        if current_price > last_offer:
            return 'improving'
        elif current_price < last_offer and second_last and current_price < second_last:
            return 'regressing'
        else:
            return 'stable'
    
    def _get_negotiation_time(self):
        """Get how long user has been negotiating"""
        return datetime.now() - self.session.created_at.replace(tzinfo=None)
    
    def _calculate_confidence_score(self, decision_data, time_spent):
        """
        Calculate confidence in accepting the offer (0-100)
        Higher score = more likely to accept
        """
        score = 50  # Base score
        
        factors = decision_data['factors']
        
        # Positive factors (increase score)
        if factors.get('offer_trend') == 'improving':
            score += 15
        if factors.get('offer_count', 0) > 2:
            score += 10
        if time_spent.total_seconds() / 60 > 5:  # More than 5 minutes
            score += 10
        
        # Negative factors (decrease score)
        if factors.get('below_minimum'):
            score -= 40
        if factors.get('exceeds_max_discount'):
            score -= 20
        if factors.get('offer_trend') == 'regressing':
            score -= 15
        
        return max(0, min(100, score))  # Clamp between 0-100
    
    def _make_decision(self, decision_data):
        """Make the final accept/reject/counter decision"""
        confidence = decision_data['factors']['confidence_score']
        discount = decision_data['discount_percentage']
        # Decision thresholds
        # Compute global minimum acceptable price to use for counter/reject messages
        try:
            global_min_price = (Decimal(self.original_price) * self.global_accept_ratio).quantize(Decimal('0.01'))
        except Exception:
            global_min_price = None

        if discount <= self.max_discount and confidence >= 70:
            decision_data['status'] = 'accepted'
            decision_data['reason'] = f'✓ Deal Accepted! You saved {discount:.1f}%'
            
        elif discount > self.max_discount and confidence >= 60:
            # Make counter offer
            counter_price = self.original_price * (1 - Decimal(self.max_discount) / 100)
            counter_discount = self._calculate_discount_percentage(counter_price)
            decision_data['status'] = 'counter'
            decision_data['counter_offer'] = float(counter_price)
            decision_data['reason'] = f'Counter offer: ₹{counter_price:.2f} ({counter_discount:.1f}% off)'
            
        else:
            decision_data['status'] = 'rejected'
            # Prefer to show the global 85% minimum when available, otherwise fall back
            if global_min_price is not None:
                decision_data['reason'] = f'✗ Price too low. Minimum acceptable: ₹{global_min_price:.2f}'
                # Offer the global minimum as a counter if confidence is reasonable
                if confidence >= 50:
                    decision_data['counter_offer'] = float(global_min_price)
            else:
                min_acceptable = self.original_price * (1 - Decimal(self.max_discount) / 100)
                decision_data['reason'] = f'✗ Price too low. Minimum acceptable: ₹{min_acceptable:.2f}'
                if confidence >= 50:
                    decision_data['counter_offer'] = float(min_acceptable)
            # append friendly suffix when counter offered
            if decision_data.get('counter_offer'):
                decision_data['reason'] += ' - I can offer this instead'
        
        return decision_data
    
    def generate_response(self, decision):
        """Generate friendly chatbot response"""
        status = decision['status']
        reason = decision['reason']
        
        if status == 'accepted':
            response = f"🎉 {reason}\n\nYou've secured a great deal! Would you like to add this to your cart?"
            
        elif status == 'counter':
            counter = decision.get('counter_offer', 0)
            response = f"{reason}\n\nWould you like to accept this counter offer instead?"
            
        else:  # rejected
            response = f"{reason}\n\nThat's below my cost-effective range. Would you like to negotiate further or try a different product?"
        
        return response
    
    def generate_voice_response(self, decision):
        """Generate text for text-to-speech voice response"""
        status = decision['status']
        
        if status == 'accepted':
            return f"Great! I accept your offer of ₹{decision['offered_price']:.2f}. That's a {decision['discount_percentage']:.0f} percent discount. Shall I add this to your cart?"
        
        elif status == 'counter':
            counter = decision.get('counter_offer', 0)
            return f"I can't go that low. But I can offer you {decision['discount_percentage']:.0f} percent off at ₹{counter:.2f}. Does that work for you?"
        
        else:
            return f"I'm sorry, that price is below what I can offer. The lowest I can go is ₹{decision.get('counter_offer', self.minimum_price):.2f}. Can you meet me there?"

    def parse_price_from_text(self, text):
        """Attempt to extract a numeric price from natural language text.

        Handles:
        - explicit amounts like '500', '₹500', '$500'
        - percentages like '50%', 'fifty percent' -> converted to price from original_price
        - relative phrases like 'half', 'quarter'
        - simple word numbers (one, two, hundred, thousand) for common cases
        Returns Decimal price or None if not found.
        """
        if not text:
            return None

        import re
        from decimal import Decimal

        t = text.lower()

        # Direct percentage (e.g., '50%')
        pct_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", t)
        if pct_match:
            try:
                pct = Decimal(pct_match.group(1))
                price = Decimal(self.original_price) * (Decimal(1) - pct / Decimal(100))
                return price.quantize(Decimal('0.01'))
            except Exception:
                pass

        # Words for half/quarter
        if 'half' in t:
            try:
                price = Decimal(self.original_price) / Decimal(2)
                return price.quantize(Decimal('0.01'))
            except Exception:
                pass
        if 'quarter' in t:
            try:
                price = Decimal(self.original_price) / Decimal(4)
                return price.quantize(Decimal('0.01'))
            except Exception:
                pass

        # Try to find currency-style numbers (with optional commas, decimals)
        num_match = re.search(r"[₹$€]?\s*([0-9]{1,3}(?:[\,\s][0-9]{3})*(?:\.[0-9]+)?|[0-9]+(?:\.[0-9]+)?)", t)
        if num_match:
            num_str = num_match.group(1).replace(',', '').replace(' ', '')
            try:
                return Decimal(num_str).quantize(Decimal('0.01'))
            except Exception:
                pass

        # Try simple word->number conversion for small numbers (e.g., 'five hundred')
        word_map = {
            'zero': 0, 'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6,
            'seven':7, 'eight':8, 'nine':9, 'ten':10, 'eleven':11, 'twelve':12,
            'thirteen':13, 'fourteen':14, 'fifteen':15, 'sixteen':16, 'seventeen':17,
            'eighteen':18, 'nineteen':19, 'twenty':20, 'thirty':30, 'forty':40,
            'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90,
            'hundred':100, 'thousand':1000
        }

        tokens = re.findall(r"[a-z]+", t)
        if tokens:
            total = 0
            current = 0
            found_word = False
            for tok in tokens:
                if tok in word_map:
                    found_word = True
                    val = word_map[tok]
                    if val == 100:
                        if current == 0:
                            current = 1
                        current *= 100
                    elif val == 1000:
                        if current == 0:
                            current = 1
                        current *= 1000
                        total += current
                        current = 0
                    else:
                        current += val
                else:
                    # reset on unknown word to avoid mixing unrelated words
                    continue
            total += current
            if found_word and total > 0:
                try:
                    return Decimal(total).quantize(Decimal('0.01'))
                except Exception:
                    pass

        return None
