import json

from random import choice

from devbot import chat


def call(message, name, protocol, cfg, commands):
    with open('music.json', 'r') as songfile:
        music = json.load(songfile)
        if message == '':
            chat.say('/msg {} Use `music list` to list all genres.'.format(name))
            allsongs = []
            for genre in music.values():
                for song in genre:
                    allsongs.append(song)
            chat.say('/msg {} {}'.format(name, choice(allsongs)))
            return

        if message == 'list':
            genrelist = ''
            for genre in music.keys():
                genrelist = genrelist + genre + ', '
            chat.say_wrap('/msg {} '.format(name), genrelist)
            return

        songs = music[message]
        if songs is None:
            chat.say('/msg {} Sorry, there were no songs under that genre.'.format(name))
            return
        chat.say('/msg {} {}'.format(name, choice(songs)))
