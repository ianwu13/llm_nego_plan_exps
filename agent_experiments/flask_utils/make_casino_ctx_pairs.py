import json

model_names = ['np_generic', 'np_selfish', 'np_fair', 'sp_generic', 'sp_selfish', 'sp_fair', 'rl_supervised', 'rl_selfish', 'rl_fair']

desired_ctxs = []
tmp = [  
    [3, 4, 5],
    [3, 5, 4],
    [4, 3, 5],
    [4, 5, 3],
    [5, 3, 4],
    [5, 4, 3],
]
ctx_getter = lambda x: f'3 {x[0]} 3 {x[1]} 3 {x[2]}'
for c in tmp:
    for d in tmp:
        desired_ctxs.append(' '.join([ctx_getter(c), ctx_getter(d)]))

mod_ctx_pairs = []
for ctx in desired_ctxs:
    for m in model_names:
        mod_ctx_pairs.append([m, ctx])

OUT_FILE = 'GEN_mod_ctx_pairs_casino_cust.json'
with open(OUT_FILE, 'w') as f:
    f.write(json.dumps({"mod_cxt_pairs": mod_ctx_pairs}))
