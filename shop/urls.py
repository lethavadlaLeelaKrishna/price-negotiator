from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('negotiate/<int:product_id>/', views.negotiation_chatbot, name='negotiation_chatbot'),
    path('send-text-offer/<str:session_id>/', views.send_text_offer, name='send_text_offer'),
    path('send-voice-offer/<str:session_id>/', views.send_voice_offer, name='send_voice_offer'),
    path('chat-history/<str:session_id>/', views.get_chat_history, name='get_chat_history'),
    path('add-to-cart/<str:session_id>/', views.add_to_cart_with_negotiation, name='add_to_cart_with_negotiation'),
    path('add-to-cart-negotiation/<str:session_id>/', views.add_to_cart_negotiation_ajax, name='add_to_cart_negotiation_ajax'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
    path('save-billing/', views.save_billing, name='save_billing'),
    path('student/<str:student_id>/', views.student_profile, name='student_profile'),
    path('session/attend/<uuid:session_id>/', views.session_attend, name='session_attend'),
]
