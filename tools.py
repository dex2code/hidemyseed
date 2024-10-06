from __future__ import annotations
from typing import Union, List
from hashlib import sha256

from bip39 import Bip39
bip39 = Bip39()

import app_config


def check_seed(list_words: Union[List[str], str]) -> bool:
   if isinstance(list_words, str):
      list_words = list_words.split()

   if not isinstance(list_words, list):
      return False
   
   if len(list_words) not in app_config.seed_words_len:
      return False

   list_words = [word.lower() for word in list_words]
   
   for word in list_words:
      if word not in bip39._dict:
         return False
   
   list_int = [bip39.get_index(word) for word in list_words]
   list_bin = [format(number, 'b').zfill(11) for number in list_int]
   str_bin = ''.join(list_bin)

   key_len = ((len(str_bin) - 1) // 8) * 8
   key_bin = str_bin[0:key_len]
   key_int = int(key_bin, 2)
   key_bytes = key_int.to_bytes(key_len // 8, "big")
   hash_bin = str_bin[key_len:]

   key_hash_hex = sha256(key_bytes).hexdigest()
   key_hash_int = int(key_hash_hex, 16)
   key_hash_bin = format(key_hash_int, 'b').zfill(len(key_hash_hex) * 4)

   return hash_bin == key_hash_bin[0:len(hash_bin)]


def obfs(list_words: List[str]) -> Union[List[str], None]:
   if not check_seed(list_words=list_words):
      return None
   
   list_int = [bip39.get_index(word) for word in list_words]
   key = list_int[-1]
   list_obfs = [(word_num ^ key) for word_num in list_int]
   list_obfs[-1] = key

   return [bip39.get_word(word_num) for word_num in list_obfs]


def deobfs(list_words: List[str]) -> Union[List[str], None]:
   for word in list_words:
      if word not in bip39._dict:
         return None

   list_int = [bip39.get_index(word) for word in list_words]
   key = list_int[-1]
   list_deobfs = [(word_num ^ key) for word_num in list_int]
   list_deobfs[-1] = key

   return [bip39.get_word(word_num) for word_num in list_deobfs]


if __name__ == "__main__":
   pass
