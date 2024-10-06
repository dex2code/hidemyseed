from __future__ import annotations
from typing import List, Union
from hashlib import sha256
from secrets import token_bytes
from tools import check_seed, obfs

from bip39 import Bip39
bip39 = Bip39()

import app_config


class Seed():
   """
   Class for processing seed phrases.
   When initialized without parameters, generates a random seed phrase with a key length of 256 bits (24 words).
   When specifying the parameter length_bits=128, it generates a phrase of 12 words.
   When specifying the parameter list_words is initialized with the specified seed phrase.
   """

   def __init__(self, list_words: Union[List[str], str] = None, length_bits: int = 256) -> None:
      self.seed_str_bin = ""
      self.seed_list_bin = []
      self.seed_list_int = []
      self.seed_list_words = []

      if list_words is None:
         assert(
            isinstance(length_bits, int)
            and (length_bits in app_config.key_bits_len)
         ), "Wrong seed bits number!"

         num_words = (length_bits // app_config.bits_per_word) + 1
         missed_bits = (num_words * app_config.bits_per_word) - length_bits

         random_bytes = token_bytes(nbytes=length_bits // 8)
         random_int = int.from_bytes(bytes=random_bytes, byteorder="big")
         random_bin = format(random_int, 'b').zfill(length_bits)

         seed_hash_bytes = sha256(string=random_bytes).hexdigest()
         seed_hash_int = int(seed_hash_bytes, base=16)
         seed_hash_bin = format(seed_hash_int, 'b').zfill(len(seed_hash_bytes) * 4)

         self.seed_str_bin = random_bin + seed_hash_bin[0:missed_bits]
         self.seed_list_bin = [
            self.seed_str_bin[i:i+app_config.bits_per_word]
               for i in range(0, len(self.seed_str_bin), app_config.bits_per_word)
         ]
         self.seed_list_int = [int(word_bin, 2) for word_bin in self.seed_list_bin]

         self.seed_list_words = [bip39.get_word(num) for num in self.seed_list_int]
         assert check_seed(list_words=self.seed_list_words), "Generated wrong seed!"
      
      else:
         assert(
            check_seed(list_words=list_words)
         ), "Bad list_words given!"

         if isinstance(list_words, str):
            list_words = list_words.split()

         self.seed_list_words = [word.lower() for word in list_words]
         self.seed_list_int = [bip39.get_index(word) for word in self.seed_list_words]
         self.seed_list_bin = [format(word_index, 'b').zfill(app_config.bits_per_word) for word_index in self.seed_list_int]
         self.seed_str_bin = ''.join(self.seed_list_bin)

      self.seed_str_words = ' '.join(self.seed_list_words)
      self.seed_list_obfs = obfs(self.seed_list_words)
      self.seed_str_obfs = ' '.join(self.seed_list_obfs)
