import random
import MeCab
import numpy as np

from makeTweetSentences import make_tweet_sentences
from timelineTweets import get_tweets, fetch_timeline_tweets
from filters import normalize_text
import re

# MeCab
mecab = MeCab.Tagger(f"-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

def omikuji(screen_name):
    return "@{} {}なん！".format(screen_name, random.choice(("凶", "大凶", "末吉", "吉", "小吉", "中吉", "大吉")))

def janken(screen_name, text):
    result = random.choice(("グー", "チョキ", "パー"))
    text = text.replace("ぐー", "グー").replace("ちょき", "チョキ").replace("ぱー", "パー")
    janken = ""
    # あいこ
    if result in text: 
        janken = "@{} {}なん！あいこなん！".format(screen_name, result)
    # 勝ちパターン
    if result == "グー" and "チョキ" in text or result == "チョキ" and "パー" in text or result == "パー" and "グー" in text:
        janken = "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
    # 負けパターン
    if result == "グー" and "パー" in text or result == "チョキ" and "グー" in text or result == "パー" and "チョキ" in text:
        janken = "@{} {}なん！うちの負けなん！".format(screen_name, result)
    return janken

def make_reply_sentence(status):
    screen_name = status.user.screen_name
    text = normalize_text(status.text)
    text = text.replace(",", "").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。").replace('@nyanpassnanon', "")
    # 占い
    if re.compile(r"(?:(?:うらな|占)って|おみくじ)").search(text):
        return omikuji(screen_name)
    # じゃんけん
    if re.compile(r"(?:[ぐぱグパ]ー|ちょき|チョキ)").search(text):
        return janken(screen_name, text)
    if text:
        if not get_tweets():
            fetch_timeline_tweets()
        sentence_1, sentence_2 = make_tweet_sentences() 
        return "@{} {}".format(screen_name, sentence_1)
    return None