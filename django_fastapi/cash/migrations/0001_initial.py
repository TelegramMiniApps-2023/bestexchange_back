# Generated by Django 4.2.7 on 2023-12-29 03:45

from django.db import migrations, models
import django.db.models.deletion
import general_models.utils.model_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('valute_from', models.CharField(max_length=10, verbose_name='Отдаём')),
                ('valute_to', models.CharField(max_length=10, verbose_name='Получаем')),
            ],
            options={
                'verbose_name': 'Элемент чёрного списка',
                'verbose_name_plural': 'Элементы чёрного списка',
                'ordering': ['city', 'valute_from', 'valute_to'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название страны')),
                ('icon_url', models.FileField(blank=True, null=True, upload_to='icons/country/', verbose_name='Флаг страны')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Название обменника')),
                ('xml_url', models.CharField(max_length=50, verbose_name='Ссылка на XML файл')),
                ('partner_link', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Партнёрская ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус обменника')),
                ('period_for_create', models.IntegerField(blank=True, default=90, help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических добавлений', null=True, validators=[general_models.utils.model_validators.is_positive_validate], verbose_name='Частота добавления в секундах')),
                ('period_for_update', models.IntegerField(blank=True, default=60, help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических обновлений', null=True, validators=[general_models.utils.model_validators.is_positive_validate], verbose_name='Частота обновлений в секундах')),
                ('period_for_parse_black_list', models.IntegerField(blank=True, default=24, help_text='Рекомендуемое значение - 24 часа.\nЗначение - положительное целое число.При установлении в 0, останавливает задачу переодического парсинга чёрного списка', null=True, validators=[general_models.utils.model_validators.is_positive_validate], verbose_name='Частота парсинга чёрного списка в часах')),
                ('direction_black_list', models.ManyToManyField(to='cash.blacklistelement', verbose_name='Чёрный список')),
            ],
            options={
                'verbose_name': 'Обменник',
                'verbose_name_plural': 'Обменники',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('time_create', models.DateTimeField(blank=True, default=None, help_text='Если оставить поля пустыми, время установится автоматически по московскому часовому поясу', null=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('Опубликован', 'Опубликован'), ('Модерация', 'Модерация'), ('Отклонён', 'Отклонён')], default='Модерация', help_text='При выборе статуса "Отклонён" попадает в очередь на удаление', max_length=20, verbose_name='Статус модерации')),
                ('moderation', models.BooleanField(default=False, verbose_name='Прошел модерацию?')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cash.exchange', verbose_name='Наличный обменник')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-time_create', 'status', 'exchange'),
            },
        ),
        migrations.CreateModel(
            name='ExchangeDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valute_from', models.CharField(max_length=10, verbose_name='Отдаём')),
                ('valute_to', models.CharField(max_length=10, verbose_name='Получаем')),
                ('in_count', models.FloatField(verbose_name='Сколько отдаём')),
                ('out_count', models.FloatField(verbose_name='Сколько получаем')),
                ('min_amount', models.CharField(max_length=50, verbose_name='Минимальное количество')),
                ('max_amount', models.CharField(max_length=50, verbose_name='Максимальное количество')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('fromfee', models.FloatField(blank=True, null=True, verbose_name='Процент')),
                ('params', models.CharField(blank=True, max_length=100, null=True, verbose_name='Параметры')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directions', to='cash.exchange', verbose_name='Обменник')),
            ],
            options={
                'verbose_name': 'Готовое направление',
                'verbose_name_plural': 'Готовые направления',
                'ordering': ['-is_active', 'exchange', 'city', 'valute_from', 'valute_to'],
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valute_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_valutes_from', to='general_models.valute', to_field='code_name', verbose_name='Отдаём')),
                ('valute_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_valutes_to', to='general_models.valute', to_field='code_name', verbose_name='Получаем')),
            ],
            options={
                'verbose_name': 'Направление для обмена',
                'verbose_name_plural': 'Направления для обмена',
                'ordering': ['valute_from', 'valute_to'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('time_create', models.DateTimeField(blank=True, default=None, help_text='Если оставить поля пустыми, время установится автоматически по московскому часовому поясу', null=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('Опубликован', 'Опубликован'), ('Модерация', 'Модерация'), ('Отклонён', 'Отклонён')], default='Модерация', help_text='При выборе статуса "Отклонён" попадает в очередь на удаление', max_length=20, verbose_name='Статус модерации')),
                ('moderation', models.BooleanField(default=False, verbose_name='Прошел модерацию?')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cash.review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-time_create', 'status', 'review'),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название города')),
                ('code_name', models.CharField(max_length=10, unique=True, verbose_name='Кодовое имя')),
                ('is_parse', models.BooleanField(default=False, verbose_name='Статус парсинга')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='cash.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['is_parse', 'name'],
            },
        ),
        migrations.AddIndex(
            model_name='blacklistelement',
            index=models.Index(fields=['city', 'valute_from', 'valute_to'], name='cash_blackl_city_4c3c37_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='blacklistelement',
            unique_together={('city', 'valute_from', 'valute_to')},
        ),
        migrations.AddIndex(
            model_name='exchangedirection',
            index=models.Index(fields=['city', 'valute_from', 'valute_to'], name='cash_exchan_city_643452_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='exchangedirection',
            unique_together={('exchange', 'city', 'valute_from', 'valute_to')},
        ),
        migrations.AddIndex(
            model_name='direction',
            index=models.Index(fields=['valute_from', 'valute_to'], name='cash_direct_valute__7db9f5_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='direction',
            unique_together={('valute_from', 'valute_to')},
        ),
        migrations.AddIndex(
            model_name='city',
            index=models.Index(fields=['code_name'], name='cash_city_code_na_f76bcc_idx'),
        ),
    ]
