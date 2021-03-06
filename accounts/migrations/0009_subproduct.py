# Generated by Django 4.0 on 2021-12-11 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_users_approval'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('cost', models.IntegerField()),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.service')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.users')),
            ],
        ),
    ]
