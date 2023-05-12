import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)

csv_model_dict = {
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genre,
    'static/data/titles.csv': Title,
    'static/data/genre_title.csv': GenreTitle,
    'static/data/users.csv': User,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    """Команда загрузки данных из csv-файла в базу данных проекта.

    Запуск командой python manage.py loadcsv.
    """

    help = 'Производит загрузку данных из CVS файлов в таблицы БД'

    def correct_fields(self, row):
        """Замена полей на объекты модели."""
        try:
            if row.get('author'):
                row['author'] = User.objects.get(pk=row['author'])
            if row.get('category'):
                row['category'] = Category.objects.get(pk=row['category'])
            if row.get('genre'):
                row['genre'] = Genre.objects.get(pk=row['genre'])
            if row.get('review_id'):
                row['review'] = Review.objects.get(pk=row['review_id'])
            if row.get('title_id'):
                row['title'] = Title.objects.get(pk=row['title_id'])
        except Exception as error:
            print(f'Ошибка в строке {row.get("id")}: {error}')
        return row

    def handle(self, *args, **options):
        for csv_file, model in csv_model_dict.items():
            print(f'Импортируем данные в модель {model.__name__}')
            with open(csv_file, encoding='utf-8', mode='r') as file:
                csv_read = csv.DictReader(file)
                for row in csv_read:
                    row = self.correct_fields(row)
                    try:
                        model.objects.get_or_create(**row)
                    except Exception as error:
                        print(f'Ошибка в строке {row.get("id")}: {error}')
                    print('.', end='', flush=True)
            print(f'Данные в модель {model.__name__} импортированы.')
