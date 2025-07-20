from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_remove_post_image_postimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.PositiveIntegerField(default=0, verbose_name='좋아요 수'),
        ),
    ]
