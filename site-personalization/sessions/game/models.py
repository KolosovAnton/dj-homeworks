from django.db import models


class Player(models.Model):
    player_id = models.CharField(
        max_length=50,
        verbose_name='ID игрока'
    )


class Game(models.Model):
    game_id = models.CharField(
        max_length=50,
        verbose_name='ID игры'
    )
    player = models.ManyToManyField(
        'Player',
        related_name='games',
        through='PlayerGameInfo'
    )
    number = models.IntegerField(
        null=True,
        verbose_name='Загаданное число'
    )
    is_finished = models.BooleanField(
        default=False,
        verbose_name='Игра завершена'
    )


class PlayerGameInfo(models.Model):
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    author = models.BooleanField(
        default=False,
        verbose_name='Автор'
    )
    number_of_attempts = models.IntegerField(
        default=0,
        verbose_name='Количество попыток'
    )
