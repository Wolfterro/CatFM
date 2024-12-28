# Generated by Django 4.2.17 on 2024-12-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0012_downloadrequest_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_list', models.TextField(blank=True, default=None, null=True)),
                ('link_list_file', models.FileField(blank=True, default=None, null=True, upload_to='admin_requests/')),
                ('status', models.CharField(choices=[('pending', 'Pendente'), ('done', 'Finalizado'), ('in_process', 'Em Processo')], default='pending', max_length=255)),
                ('link_status_description', models.TextField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]