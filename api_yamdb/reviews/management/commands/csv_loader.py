import csv

from django.apps import apps
from django.core.management import BaseCommand
from django.db.models import Count
from reviews.models import Title

from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    path = BASE_DIR.joinpath('static', 'data')
    sequence = {  # последовательность чтения файлов
        'users': 'User',
        'category': 'Category',
        'genre': 'Genre',
        'titles': 'Title',
        'genre_title': 'Title',
        'review': 'Review',
        'comments': 'Comment',
    }
    help = 'Импорт из csv файлов в базу данных'
    records_counter = 0

    def handle(self, *args, **kwargs):
        for filename, model_name in self.sequence.items():
            objects_to_import = []
            model = apps.get_model('reviews', model_name)
            with open(f'{self.path}/{filename}.csv') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.records_counter += 1
                    self.collect_list_to_bulk_create(
                        filename,
                        objects_to_import,
                        row,
                        model,
                    )
            self.import_objects_to_db(
                filename,
                model,
                objects_to_import,
            )
        self.final_report()

    def collect_list_to_bulk_create(
        self,
        filename,
        objects_to_import,
        row,
        model,
    ):
        """Наполняет лист объектами моделей
        для последующего импорта в базу данных."""

        if filename == 'genre_title':
            objects_to_import.append(
                model.genre.through(**row),
            )
        elif filename == 'titles':
            objects_to_import.append(
                model(category_id=row.pop('category'), **row),
            )
        elif filename == 'review':
            objects_to_import.append(
                model(author_id=row.pop('author'), **row),
            )
        elif filename == 'comments':
            objects_to_import.append(
                model(author_id=row.pop('author'), **row),
            )
        else:
            objects_to_import.append(model(**row))

    def import_objects_to_db(self, filename, model, objects_to_import):
        """Импорт в базу данных."""

        if filename == 'genre_title':
            model.genre.through.objects.bulk_create(
                objects_to_import,
                ignore_conflicts=True,
            )
        else:
            model.objects.bulk_create(
                objects_to_import,
                ignore_conflicts=True,
            )

    def final_report(self):
        """Выводит отчёт о количестве созданных
        объектов в базе данных."""

        self.stdout.write(
            f'-----------------------------\n'
            f'Всего записей обработано: {self.records_counter}\n'
            f'-----------------------------\n',
        )
        for model_name in set(self.sequence.values()):
            model = apps.get_model('reviews', model_name)
            self.stdout.write(
                f'Объектов {model_name} создано: '
                f'{model.objects.all().count()}\n',
            )
        self.stdout.write(
            f'Объектов Title_Genre создано: '
            f'{Title.objects.aggregate(count=Count("genre"))["count"]}\n\n',
        )
