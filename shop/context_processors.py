def billing_info(request):
    """Context processor to expose billing information to templates.

    Priority:
    - If billing saved in session (from save_billing or checkout), use that.
    - Else, if user is authenticated, attempt to read the most recent Order's billing snapshot.
    """
    billing = request.session.get('billing')
    if billing:
        return {'billing_info': billing}

    # Fallback: latest order billing for authenticated users
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        try:
            from .models import Order
            latest = Order.objects.filter(user=user).order_by('-created_at').first()
            if latest:
                return {'billing_info': {
                    'full_name': latest.billing_full_name,
                    'email': latest.billing_email,
                    'address': latest.billing_address,
                    'city': latest.billing_city,
                    'state': latest.billing_state,
                    'zip_code': latest.billing_zip,
                }}
        except Exception:
            pass

    return {'billing_info': None}
