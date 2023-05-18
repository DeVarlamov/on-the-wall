
import django.core.validators
import django.db.models.deletion



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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='имя категории')),
                ('slug', models.SlugField(unique=True, verbose_name='слаг категории')),

            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
               ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='имя жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='cлаг жанра')),

            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[

                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=256, verbose_name='имя жанра'),
                ),
                (
                    'slug',
                    models.SlugField(unique=True, verbose_name='cлаг жанра'),
                ),

                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='название')),
                ('year', models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=2023, message='год выпуска не может превышать текущий год')], verbose_name='год')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='категория')),
                ('genre', models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='жанр')),

            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[

            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[

