import random

from django.shortcuts import render, redirect
from django.urls import reverse

from game.forms import NumberForm
from game.models import Game, PlayerGameInfo, Player


def show_home(request):
    player_session = request.session.get('player_id')
    game_session = request.session.get('game_id')

    if player_session and game_session:
        game = Game.objects.get(game_id=game_session)
        current_player = Player.objects.get(player_id=player_session)
        if game.is_finished:
            if Game.objects.filter(is_finished=False).count() == 0:
                game = Game.objects.create(game_id=random.randint(1, 100000), number=random.randint(0, 100))
                PlayerGameInfo.objects.create(player=current_player, game=game, author=True)
            else:
                game = Game.objects.filter(is_finished=False).order_by('pk').first()
                game.player.add(current_player)

            request.session['game_id'] = str(game.game_id)
            return redirect(reverse('home'))

        else:
            if PlayerGameInfo.objects.all().filter(game_id=game).get(player_id=current_player).author:
                return redirect(reverse('author_page'))
            else:
                return redirect(reverse('game'))

    else:
        current_player = Player.objects.create(player_id=random.randint(1, 100000))
        if Game.objects.filter(is_finished=False).count() == 0:
            game = Game.objects.create(game_id=random.randint(1, 100000), number=random.randint(0, 100))
            PlayerGameInfo.objects.create(player=current_player, game=game, author=True)

        else:
            game = Game.objects.filter(is_finished=False).order_by('pk').first()
            game.player.add(current_player)

        request.session['player_id'] = str(current_player.player_id)
        request.session['game_id'] = str(game.game_id)
        return redirect('/')


def show_author_page(request):
    game = Game.objects.get(game_id=request.session.get('game_id'))
    current_player = Player.objects.get(player_id=request.session.get('player_id'))
    context = {'game_info': PlayerGameInfo.objects.filter(game_id=game).get(player_id=current_player)}

    return render(
        request,
        'author_page.html',
        context
    )


def show_game(request):
    game = Game.objects.get(game_id=request.session.get('game_id'))
    current_player = Player.objects.get(player_id=request.session.get('player_id'))
    counter = PlayerGameInfo.objects.filter(game_id=game).get(player_id=current_player)
    form = NumberForm(request.POST or None)
    context = {}

    if form.is_valid():
        answer = int(request.POST.get('number'))
        counter.number_of_attempts += 1
        counter.save()
        if answer == game.number:
            game.is_finished = True
            game.save()
            context['text'] = f'Вы угадали число! C {counter.number_of_attempts} попыток'
        elif answer < game.number:
            context['text'] = f'Загаданное число больше числа {answer}'
        elif answer > game.number:
            context['text'] = f'Загаданное число меньше числа {answer}'
        context['form'] = form
        return render(request, 'game.html', context)
    else:
        context['form'] = form
        return render(request, 'game.html', context)
