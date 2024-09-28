from seed import Seed

seed = Seed()

print(
   seed.seed_str_bin,
   seed.seed_list_bin,
   seed.seed_list_int,
   seed.seed_list_words,
   ' '.join(seed.seed_list_words),
   sep='\n'
)