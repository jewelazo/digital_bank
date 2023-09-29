# Generated by Django 4.2.5 on 2023-09-29 22:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(16)], verbose_name='account_number')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='balance')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='accounts', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]