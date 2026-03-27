"""
URL configuration for chatbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views as shop_views

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('admin/', admin.site.urls),
    # Include shop app URLs under the 'shop' namespace. This registers the
    # 'shop' namespace so templates can use names like 'shop:product_detail'.
    # Register both namespaced and non-namespaced includes so legacy
    # reverse() calls (tests or external code) that rely on un-namespaced
    # URL names keep working.
    path('', include('shop.urls')),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    # Legacy non-namespaced routes (explicitly declared) to support tests and
    # any code that expects these names without the 'shop:' namespace.
    path('shop/send-text-offer/<str:session_id>/', shop_views.send_text_offer, name='send_text_offer'),
    path('shop/send-voice-offer/<str:session_id>/', shop_views.send_voice_offer, name='send_voice_offer'),
    path('shop/add-to-cart/<str:session_id>/', shop_views.add_to_cart_with_negotiation, name='add_to_cart_with_negotiation'),
    path('shop/add-to-cart-negotiation/<str:session_id>/', shop_views.add_to_cart_negotiation_ajax, name='add_to_cart_negotiation_ajax'),
    path('shop/cart/', shop_views.view_cart, name='view_cart'),
    path('shop/checkout/', shop_views.checkout, name='checkout'),
    path('shop/order-history/', shop_views.order_history, name='order_history'),
    path('shop/save-billing/', shop_views.save_billing, name='save_billing'),
    # Non-namespaced auth routes for legacy reverse('login') / reverse('logout') calls
    path('login/', shop_views.login_view, name='login'),
    path('logout/', shop_views.logout_view, name='logout'),
    path('register/', shop_views.register, name='register'),
]
