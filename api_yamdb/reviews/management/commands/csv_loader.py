import csv

from django.apps import apps
from django.core.management import BaseCommand
from django.db.models import Count
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title, User

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
                    self.prepare_data(row)
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

    def prepare_data(self, row):
        """
        Viewset для обработки операций CRUD по тайтлам.
        """
        if 'category' in row:
            row['category'] = get_object_or_404(
                Category,
                pk=row['category'],
            )
        if 'author' in row:
            row['author'] = get_object_or_404(
                User,
                pk=row['author'],
            )
        if 'title_id' in row:
            row['title'] = get_object_or_404(
                Title,
                pk=row['title_id'],
            )
        if 'genre_id' in row:
            row['genre'] = get_object_or_404(
                Genre,
                pk=row['genre_id'],
            )
        return row

    def collect_list_to_bulk_create(
        self,
        filename,
        objects_to_import,
        row,
        model,
    ):
        if filename == 'genre_title':
            objects_to_import.append(
                Title.genre.through(
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                ),
            )
        else:
            objects_to_import.append(model(**row))

    def import_objects_to_db(self, filename, model, objects_to_import):
        if filename == 'genre_title':
            Title.genre.through.objects.bulk_create(
                objects_to_import,
                ignore_conflicts=True,
            )
        else:
            model.objects.bulk_create(
                objects_to_import,
                ignore_conflicts=True,
            )

    def final_report(self):
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


""" def prepare_counters(self):
        self.imported_counter = defaultdict(int)
        self.records_counter = 0
        # self.imported_counter = 0
        self.skipped_counter = 0 """
""" sequence = {
    'users': 'User',
    'category': 'Category',
    'genre': 'Genre',
    'titles': 'Title',
    'genre_title': 'User',
    'review': 'Review',
    'comments': 'Comment',
}
path = BASE_DIR.joinpath('static', 'data')

for name, model_name in sequence.items():
    with open(f'{path}/{name}.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row) """

""" if filename == 'genre_title':
                        # row['title'].genre.add(row['genre'])
                        ls.append(
                            Title.genre.through(
                                title_id=row['title_id'],
                                genre_id=row['genre_id'],
                            ),
                        )
                    else:
                        ls.append(model(**row)) """
""" try:
    model.objects.get_or_create(**row)
except IntegrityError:
    self.skipped_counter += 1
    # print(row)
self.imported_counter[model_name] += 1 """
