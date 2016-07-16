import json

from random import choice

from devbot import chat


def call(message, name, protocol, cfg, commands):
    with open('music.json', 'r') as songfile:
        music = json.load(songfile)
        if message == '':
            chat.say('/msg {} Use `music list` to list all genres.'.format(name))
            allsongs = []
            for genre in music.items():
                for song in genre[1]:
                    allsongs.append((song, genre[0]))
            song = choice(allsongs)
            chat.say('/msg {} {} -- {}'.format(name, song[0], song[1]))
            return

        if message == 'list':
            genrelist = ''
            for genre in music.keys():
                genrelist = genrelist + genre + ', '
            chat.say_wrap('/msg {} '.format(name), genrelist)
            return

        try:
            songs = music[message]
            chat.say('/msg {} {}'.format(name, choice(songs)))
        except KeyError:
            chat.say('/msg {} Sorry, there were no songs under that genre.'.format(name))

