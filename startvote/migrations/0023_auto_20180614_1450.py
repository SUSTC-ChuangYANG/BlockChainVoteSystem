# Generated by Django 2.0.5 on 2018-06-14 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startvote', '0022_auto_20180614_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='vote_img',
            field=models.ImageField(default='default/2.png', upload_to='pic_folder/'),
        ),
    ]
