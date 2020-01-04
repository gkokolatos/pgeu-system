# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-01-04 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0015_pendingbanktransaction_longer_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('parsedrows', models.IntegerField()),
                ('newtrans', models.IntegerField()),
                ('newpending', models.IntegerField()),
                ('uploadby', models.CharField(max_length=50)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('textcontents', models.TextField(max_length=100000)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.InvoicePaymentMethod')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bankfileupload',
            unique_together=set([('method', 'created')]),
        ),
    ]
