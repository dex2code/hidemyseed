from seed import Seed
from tools import deobfs

seed_phrase = "near appear sure fix basket direct fat riot stone vapor sugar tip"
seed_obj = Seed(list_words=seed_phrase)

print(f"Init Seed: {seed_obj.seed_list_words}")
print(f"Obfuscated Seed: {seed_obj.seed_list_obfs}")

deobfs_seed = deobfs(list_words=seed_obj.seed_list_obfs)
print(f"Deobfuscated Seed: {deobfs_seed}")