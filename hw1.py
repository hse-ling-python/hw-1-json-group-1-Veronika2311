"""# -*- coding: utf-8 -*- Created on Mon Sep 30 15:17:43 2019 @author: M"""

import collections
import json
import re
from string import punctuation as punct

def readjson():
    '''прочитать файл и преобразовать из json'''
    twitter = []
    for line in open('hw_3_twitter.json'):
        twitter.append(json.loads(line))

    return twitter


def howtweets(twitter):
    '''считает длину списка - количество кластеров с информацией твитов'''
    print('Количество твитов в коллекции:' + str(len(twitter)))


def delete_tweets(twitter):
    '''считает процент удалённых твитов через ключ delete'''
    number_of_delete = 0
    for tweet in twitter:
        for keys in tweet:
            if 'delete' in keys:
                number_of_delete = number_of_delete + 1

    percent_of_delete = number_of_delete/(len(twitter)/100)

    return percent_of_delete


def langs_of_tweets(twitter):
    '''составляет список языков и считает из частотность'''
    langs = []
    for tweet in twitter:
        for keys in tweet:
            if 'lang' in keys:
                langs.append(tweet['lang'])
    counter_langs = dict(collections.Counter(langs))

    return counter_langs


def one_user(twitter):
    '''повторяются ли id, выведет id всех, кто написал >1 твита'''
    ids = []
    for tweet in twitter:
        if 'user' in tweet:
            user_of_tw = tweet['user']
            if 'id_str' in user_of_tw:
                ids.append(user_of_tw['id_str'])

        if 'delete' in tweet:
            deleted_status = tweet['delete']
            if 'status' in deleted_status:
                status_of_tw = deleted_status['status']
                if 'user_id_str' in status_of_tw:
                    ids.append(status_of_tw['user_id_str'])

    counter_ids = dict(collections.Counter(ids))

    active_users = {}
    for tweet_users, num_tweets in counter_ids.items():
        if num_tweets > 1:
            active_users[tweet_users] = num_tweets

    return len(active_users)


def top_hashtags(twitter):
    '''список всех хэштегов, Counter, топ-20'''
    tags = []

    for tweet in twitter:
        if 'entities' in tweet:
            entities = tweet['entities']
            if 'hashtags' in entities:
                hashtags = entities['hashtags']
                for htag in hashtags:
                    if 'text' in htag:
                        tags.append(htag['text'])

    counter_tags = dict(collections.Counter(tags))
    top_tags = []
    for key in sorted(counter_tags, key=counter_tags.get, reverse=True):
        top_tags.append((key, counter_tags[key]))

    return top_tags[0:20:]


def freg_en_tweets(twitter):
    '''частотный словарь оригинальных твитов на английском языке'''
    words = []

    for tweet in twitter:
        if 'lang' in tweet:
            if tweet['lang'] == 'en':
                if 'text' in tweet:
                    text = tweet['text']
                    if not text.startswith('RT @'):
                        if 'extended_tweet' in tweet:
                            if 'full_text' in tweet['extended_tweet']:
                                text = tweet['extended_tweet']['full_text']

                        spl_tweet = text.split(' ')
                        for word in spl_tweet:
                            word = word.strip(punct)
                            word = word.lower()
                            if word:
                                words.append(word)

    top_words = []
    freq_words = dict(collections.Counter(words))
    for key in sorted(freq_words, key=freq_words.get, reverse=True):
        top_words.append((key, freq_words[key]))

    return top_words[0:20:]


def count_of_followers(twitter):
    '''словарь id - количество фолловеров'''
    follow_count = {}
    for tweet in twitter:
        if 'user' in tweet:
            user_of_tw = tweet['user']
            if 'id_str' in user_of_tw:
                user_id = user_of_tw['id_str']
                if 'followers_count' in user_of_tw:
                    follow_count[user_id] = user_of_tw['followers_count']

    top_users = []
    for key in sorted(follow_count, key=follow_count.get, reverse=True):
        top_users.append((key, follow_count[key]))

    return top_users[0:10:]


def apps_of_tweet(twitter):
    'ищет названия прложений'
    apps = []
    for tweet in twitter:
        if 'source' in tweet:
            app = (re.search('<a href.+?>(.+?)</a>', tweet['source'])).group(1)
            apps.append(app)

    top_of_apps = []
    freq_apps = dict(collections.Counter(apps))
    for key in sorted(freq_apps, key=freq_apps.get, reverse=True):
        top_of_apps.append((key, freq_apps[key]))

    return top_of_apps[0:20]


def main():
    '''запуск функций поочерёдно'''
    twitter = readjson()
    #Задание 1, количество твитов
    howtweets(twitter)
    #Задание 2, процент удалённых твитов
    print ('Процент удалённых твитов: ' + str(delete_tweets(twitter)) + '%')
    #Задание 3, частые языки твитов
    print('Частотный словарь языков неудалённых твитов: ')
    print(langs_of_tweets(twitter))
    #Задание 4, пользователи, написавшие больше одного твита
    print('Количество пользователей (с удалёнными), написавших больше одного твита: ')
    print(one_user(twitter))
    #Задание 5, топ хештэгов
    print('Топ хештэгов, первые 20: ')
    print(top_hashtags(twitter))
    #Задание 6, топ фолловеров
    print('Топ фолловеров, первые 10: ')
    print(count_of_followers(twitter))
    #Задание 7, частотный словарь твитов
    print('Частотный словарь из неудалённых твитов, первые 20: ')
    print(freg_en_tweets(twitter))
    #Задание 8, частотность приложений
    print('Частотность приложений, первые 20:')
    print(apps_of_tweet(twitter))

if __name__ == "__main__":
    main()
