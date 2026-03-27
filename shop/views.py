from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.db import models
import json
import uuid
from datetime import datetime
from django.utils.timezone import now

from .models import (
    Product, NegotiationSession, ChatMessage, PriceOffer, Cart, CartItem, Order,
    AttendanceSession, AttendanceRecord
)
from django.core.files.base import ContentFile
from decimal import Decimal
from .negotiation_engine import PriceNegotiationEngine


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('shop:product_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        # Provide a sample username placeholder for demo/testing
        form = CustomUserCreationForm(initial={'username': 'krishna7373'})
    
    context = {'form': form}
    return render(request, 'shop/register.html', context)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        next_url = request.GET.get('next', '') or request.POST.get('next', '')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect('shop:product_list')
    # Determine next (redirect) URL from GET or POST so we can return user there after login
    if request.method == 'POST':
        next_url = request.POST.get('next', '')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Only redirect to safe local URLs
                if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                    return redirect(next_url)
                return redirect('shop:product_list')
    else:
        next_url = request.GET.get('next', '')
        form = AuthenticationForm()

    context = {'form': form, 'next': next_url}
    return render(request, 'shop/login.html', context)


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def product_list(request):
    """Display all products"""
    search_query = request.GET.get('search', '').strip()
    products = Product.objects.all()
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    context = {
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'shop/product_list.html', context)


@login_required(login_url='login')
def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    # Simple heuristic rating out of 5
    rating = 4.0
    name_lower = (product.name or "").lower()
    if 'premium' in name_lower:
        rating += 0.5
    try:
        dp = float(product.discount_percentage or 0)
    except Exception:
        dp = 0.0
    if dp >= 10:
        rating += 0.3
    if (product.stock or 0) > 0:
        rating += 0.2
    rating = max(1.0, min(5.0, round(rating, 1)))
    verdict = 'Recommended' if rating >= 4.0 else ('Consider' if rating >= 3.0 else 'Not Recommended')
    context = {'product': product, 'rating': rating, 'verdict': verdict}
    return render(request, 'shop/product_detail.html', context)


@login_required(login_url='login')
def negotiation_chatbot(request, product_id):
    """Main chatbot negotiation interface"""
    product = get_object_or_404(Product, pk=product_id)
    
    # Create or get negotiation session
    session_id = request.session.get(f'negotiation_{product_id}')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session[f'negotiation_{product_id}'] = session_id
        
        # Create negotiation session
        negotiation = NegotiationSession.objects.create(
            user=request.user,
            product=product,
            session_id=session_id,
            original_price=product.original_price
        )
    else:
        negotiation = NegotiationSession.objects.get(session_id=session_id)
    
    context = {
        'product': product,
        'negotiation': negotiation,
        'session_id': session_id
    }
    return render(request, 'shop/negotiation_chatbot.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def send_text_offer(request, session_id):
    """Handle text-based price offers"""
    try:
        data = json.loads(request.body)
        offered_price = data.get('offered_price')
        user_message = data.get('message', '')
        # If offered_price is missing or falsy, try to parse from natural language message
        if not offered_price:
            # instantiate engine with session later
            session_obj = NegotiationSession.objects.get(session_id=session_id)
            engine = PriceNegotiationEngine(session_obj)
            parsed = engine.parse_price_from_text(user_message)
            if parsed is not None:
                offered_price = float(parsed)
            else:
                return JsonResponse({'status': 'error', 'message': 'No offered_price provided and could not parse price from text'}, status=400)
        else:
            offered_price = float(offered_price)
        
        # Get negotiation session
        session = NegotiationSession.objects.get(session_id=session_id)
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            message_type='user_text',
            content=user_message.replace('$', '₹'),
            offered_price=offered_price
        )
        
        # Process with negotiation engine
        engine = PriceNegotiationEngine(session)
        decision = engine.evaluate_offer(offered_price)
        
        # Save price offer
        offer = PriceOffer.objects.create(
            session=session,
            offered_price=offered_price,
            discount_percentage=decision['discount_percentage'],
            status=decision['status'],
            reason=decision['reason'],
            counter_offer_price=decision.get('counter_offer')
        )
        
        # Generate bot response
        bot_response = engine.generate_response(decision)
        
        # Save bot message
        bot_msg = ChatMessage.objects.create(
            session=session,
            message_type='bot_text',
            content=bot_response,
            bot_response=bot_response
        )
        
        # Update session if accepted
        if decision['status'] == 'accepted':
            session.status = 'accepted'
            session.final_agreed_price = offered_price
            session.discount_percentage = decision['discount_percentage']
            session.save()
        
        return JsonResponse({
            'status': 'success',
            'offer_status': decision['status'],
            'bot_response': bot_response,
            'counter_offer': decision.get('counter_offer'),
            'discount': decision['discount_percentage'],
            'reason': decision['reason']
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def send_voice_offer(request, session_id):
    """Handle voice-based price offers"""
    try:
        # Get audio file from request
        if 'audio' not in request.FILES:
            return JsonResponse({'status': 'error', 'message': 'No audio file'}, status=400)
        
        audio_file = request.FILES['audio']
        offered_price_raw = request.POST.get('offered_price', '')
        offered_price = None
        try:
            if offered_price_raw:
                offered_price = float(offered_price_raw)
        except Exception:
            offered_price = None

        # If offered_price not provided, try to parse from transcript/message fields
        if not offered_price:
            transcript = request.POST.get('transcript', '') or request.POST.get('message', '')
            session = NegotiationSession.objects.get(session_id=session_id)
            engine = PriceNegotiationEngine(session)
            parsed = engine.parse_price_from_text(transcript)
            if parsed is not None:
                offered_price = float(parsed)
            else:
                return JsonResponse({'status': 'error', 'message': 'No offered_price provided and could not parse price from voice transcription'}, status=400)
        
        # Get negotiation session
        session = NegotiationSession.objects.get(session_id=session_id)
        
        # Save user voice message
        user_msg = ChatMessage.objects.create(
            session=session,
            message_type='user_voice',
            content=f'Voice offer: ₹{offered_price}',
            audio_file=audio_file,
            offered_price=offered_price
        )
        
        # Process with negotiation engine
        engine = PriceNegotiationEngine(session)
        decision = engine.evaluate_offer(offered_price)
        
        # Save price offer
        offer = PriceOffer.objects.create(
            session=session,
            offered_price=offered_price,
            discount_percentage=decision['discount_percentage'],
            status=decision['status'],
            reason=decision['reason'],
            counter_offer_price=decision.get('counter_offer')
        )
        
        # Generate bot response
        bot_response = engine.generate_response(decision)
        
        # Save bot message with voice
        bot_msg = ChatMessage.objects.create(
            session=session,
            message_type='bot_voice',
            content=bot_response,
            bot_response=bot_response
        )
        
        # Update session if accepted
        if decision['status'] == 'accepted':
            session.status = 'accepted'
            session.final_agreed_price = offered_price
            session.discount_percentage = decision['discount_percentage']
            session.save()
        
        return JsonResponse({
            'status': 'success',
            'offer_status': decision['status'],
            'bot_response': bot_response,
            'counter_offer': decision.get('counter_offer'),
            'discount': decision['discount_percentage'],
            'message_id': bot_msg.id
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def get_chat_history(request, session_id):
    """Retrieve chat history for a session"""
    try:
        session = NegotiationSession.objects.get(session_id=session_id)
        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        
        chat_data = []
        for msg in messages:
            chat_data.append({
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.created_at.isoformat(),
                'offered_price': msg.offered_price
            })
        
        return JsonResponse({
            'status': 'success',
            'messages': chat_data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
def add_to_cart_with_negotiation(request, session_id):
    """Add negotiated product to cart"""
    try:
        session = NegotiationSession.objects.get(session_id=session_id)
        
        if session.status != 'accepted':
            return JsonResponse({'status': 'error', 'message': 'Price not agreed yet'}, status=400)
        
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Add item to cart with negotiated price
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = CartItem.objects.create(
            cart=cart,
            product=session.product,
            negotiation_session=session,
            quantity=quantity,
            negotiated_price=session.final_agreed_price,
            original_price=session.original_price
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Added to cart',
            'cart_total': float(cart.get_total())
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
def add_to_cart_negotiation_ajax(request, session_id):
    """Add negotiated product to cart via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)
    
    try:
        import json
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        
        session = NegotiationSession.objects.get(session_id=session_id)
        
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Add item to cart with negotiated price
        cart_item = CartItem.objects.create(
            cart=cart,
            product=session.product,
            negotiation_session=session,
            quantity=int(quantity),
            negotiated_price=session.final_agreed_price or session.original_price,
            original_price=session.original_price
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Added to cart successfully',
            'cart_total': float(cart.get_total()),
            'quantity': quantity
        })
    
    except NegotiationSession.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required(login_url='login')
def view_cart(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    total = cart.get_total()
    tax = float(total) * 0.1
    final_total = float(total) * 1.1
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': total,
        'tax': tax,
        'final_total': final_total
    }
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart = get_object_or_404(Cart, user=request.user)
    
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
        if request.method == 'POST':
            item.delete()
            messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        # If item is already gone, just ignore and redirect
        pass
        
    return redirect('shop:view_cart')


@login_required(login_url='login')
def checkout(request):
    """Checkout with negotiated prices"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        # Process checkout: create Order and order items, attach invoice file
        total = Decimal(cart.get_total())
        tax = (total * Decimal('0.1')).quantize(Decimal('0.01'))
        final_total = (total + tax).quantize(Decimal('0.01'))

        # Billing info from session (saved earlier via AJAX) or empty defaults
        billing = request.session.get('billing', {})
        full_name = billing.get('full_name') or request.user.get_full_name()
        email = billing.get('email') or request.user.email
        address = billing.get('address', '')
        city = billing.get('city', '')
        state = billing.get('state', '')
        zip_code = billing.get('zip_code', '')

        # Lazy import Order models to avoid circular import issues
        from .models import Order, OrderItem

        order = Order.objects.create(
            user=request.user,
            total=total,
            tax=tax,
            final_total=final_total,
            billing_full_name=full_name,
            billing_email=email,
            billing_address=address,
            billing_city=city,
            billing_state=state,
            billing_zip=zip_code,
        )

        # Create order items
        cart_items = list(cart.items.all())
        for ci in cart_items:
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                negotiated_price=ci.negotiated_price,
                original_price=ci.original_price,
            )

        # Generate a simple invoice text and save as a media file
        lines = []
        lines.append(f"Order ID: {order.id}")
        lines.append(f"User: {request.user.username} ({email})")
        lines.append(f"Full Name: {full_name}")
        lines.append(f"Address: {address}, {city}, {state} - {zip_code}")
        lines.append('')
        lines.append('Items:')
        for oi in order.order_items.all():
            lines.append(f" - {oi.product.name} x{oi.quantity} @ ₹{oi.negotiated_price} = ₹{oi.get_total_price()}")
        lines.append('')
        lines.append(f"Subtotal: ₹{total}")
        lines.append(f"Tax (10%): ₹{tax}")
        lines.append(f"Total: ₹{final_total}")
        lines.append('')
        lines.append('Thank you for your purchase!')

        invoice_text = '\n'.join(lines)
        invoice_filename = f'invoice_order_{order.id}.txt'
        order.invoice_file.save(invoice_filename, ContentFile(invoice_text.encode('utf-8')))
        order.save()

        # Store billing snapshot in session so navbar (and other pages) can show it
        request.session['billing'] = {
            'full_name': full_name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
        }

        # Clear the cart
        cart.items.all().delete()

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'final_total': final_total,
            'success': True,
            'order': order,
        }
        return render(request, 'shop/checkout_success.html', context)
    
    total = cart.get_total()
    tax = float(total) * 0.1
    final_total = float(total) * 1.1
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': total,
        'tax': tax,
        'final_total': final_total
    }
    return render(request, 'shop/checkout.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def save_billing(request):
    """AJAX endpoint to save billing address into session"""
    try:
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()

        if not full_name or not email or not address:
            return JsonResponse({'status': 'error', 'message': 'Full name, email and address are required.'}, status=400)

        request.session['billing'] = {
            'full_name': full_name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
        }

        return JsonResponse({'status': 'success', 'message': 'Billing address saved.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='login')
def order_history(request):
    """View to display user's order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'shop/order_history.html', context)


@login_required(login_url='login')
def student_profile(request, student_id):
    user = request.user
    full_name = user.get_full_name() or user.username
    attendance_marked = AttendanceRecord.objects.filter(user=user, date=now().date()).exists()
    context = {
        'student_id': student_id,
        'username': user.username,
        'full_name': full_name,
        'department': '',
        'email': user.email,
        'account_status': 'Active' if user.is_active else 'Inactive',
        'today': now().date(),
        'attendance_marked': attendance_marked,
    }
    return render(request, 'shop/student_profile.html', context)


@login_required(login_url='login')
def session_attend(request, session_id):
    try:
        session = AttendanceSession.objects.get(id=session_id)
    except AttendanceSession.DoesNotExist:
        messages.error(request, 'Invalid or inactive session QR.')
        return redirect('shop:student_profile', student_id=request.user.username)
    current = now()
    if not session.active or (session.starts_at and current < session.starts_at) or (session.ends_at and current > session.ends_at):
        messages.error(request, 'Invalid or inactive session QR.')
        return redirect('shop:student_profile', student_id=request.user.username)
    rec, created = AttendanceRecord.objects.get_or_create(
        user=request.user,
        session=session,
        date=current.date(),
    )
    if created:
        messages.success(request, f'Attendance marked for {current.date().strftime("%B %d, %Y")}.')
    else:
        messages.info(request, 'Attendance already marked today.')
    return redirect('shop:student_profile', student_id=request.user.username)

