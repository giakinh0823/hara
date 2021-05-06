# Generated by Django 3.0 on 2021-05-06 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_product_percent'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('slug', models.SlugField(max_length=2000)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='groupCategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.GroupCategory'),
        ),
    ]