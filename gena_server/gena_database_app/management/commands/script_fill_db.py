from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from gena_database_app.models import *

from faker import Faker
import random


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        fake = Faker()

        # создание пользователей
        self.stdout.write('Создание пользователей')
        users = []
        for i in range(5):
            user = User.objects.create(
                email=fake.ascii_free_email(),
                password=fake.password(length=10),
                userName=fake.name()
            )
            users.append(user)
            self.stdout.write(f'    Создан пользователь c email: {user.email}, паролем: {user.password}, именем: {user.userName}')

        # создание изображений
        self.stdout.write('Создание изображений')
        images = []
        
        for i in range(10):
            image = Image.objects.create(
                link_to_image=fake.uri(),
                rating=random.randint(1, 5)
            )
            images.append(image)
            self.stdout.write(f'    Создано изображение: {image.link_to_image} с рейтингом {image.rating}')

        # создание записей истории использования
        self.stdout.write('Создание истории использования')
        statuses = ['Success', 'Pending', 'Failed', 'Processing', 'Cancelled']
        prompts = [
            'Красивый закат на пляже',
            'Портрет девушки в стиле ренессанс',
            'Городской пейзаж ночью',
            'Горы и озеро в туманное утро',
            'Кот, играющий с клубком',
            'Абстрактная композиция в синих тонах',
            'Космический корабль на орбите Марса',
            'Цветущий сад весной',
            'Старинный замок в лесу',
            'Футуристический интерьер'
        ]

        for i in range(20):
            user = random.choice(users)
            image = random.choice(images)
            prompt = random.choice(prompts)
            status = random.choice(statuses)

            # Создаем запись истории
            usage = Usage_history.objects.create(
                userID=user,
                imageID=image,
                prompt=prompt,
                status=status
            )
            self.stdout.write(f'    Создана запись истории: пользователь - {user.userID}, изображение - {image.imageID}, статус - {status}')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
        self.stdout.write(f'Добавлено: {len(users)} пользователей, {len(images)} изображений, {Usage_history.objects.count()} записей истории')
