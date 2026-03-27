from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='product_images/', null=True, blank=True),
        ),
    ]
