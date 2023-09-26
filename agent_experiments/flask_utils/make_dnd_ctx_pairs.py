model_names = ['np_generic', 'np_selfish', 'np_fair', 'sp_generic', 'sp_selfish', 'sp_fair', 'rl_supervised', 'rl_selfish', 'rl_fair']
desired_ctxs = []  # TODO

mod_ctx_pairs = []
for ctx in desired_ctxs:
    for m in model_names:
        mod_ctx_pairs.append([m, ctx])

OUT_FILE = 'GEN_mod_ctx_pairs_dnd.json'
with open(OUT_FILE, 'w') as f:
    f.write(jsom.dumps({"mod_cxt_pairs": mod_ctx_pairs}))
