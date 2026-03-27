from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('final_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('billing_full_name', models.CharField(max_length=255, null=True, blank=True)),
                ('billing_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('billing_address', models.TextField(null=True, blank=True)),
                ('billing_city', models.CharField(max_length=100, null=True, blank=True)),
                ('billing_state', models.CharField(max_length=100, null=True, blank=True)),
                ('billing_zip', models.CharField(max_length=20, null=True, blank=True)),
                ('status', models.CharField(default='pending', max_length=20, choices=[('pending','Pending'),('paid','Paid'),('shipped','Shipped'),('cancelled','Cancelled')])),
                ('invoice_file', models.FileField(upload_to='invoices/', null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('negotiated_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
