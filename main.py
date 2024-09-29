from seed import Seed
from tools import deobfs

seed = Seed()
print(seed.seed_str_words)
print(seed.seed_str_obfs)

seed_deobfs = deobfs(list_words=seed.seed_list_obfs)

seed = Seed(list_words=seed_deobfs)
print(seed.seed_str_words)
