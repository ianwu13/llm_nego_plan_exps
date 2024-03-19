import json
import os
import re
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sn 

DIR_PATH = 'agent_sp_2_22_24/json_w_deal' # || 'gru_selfplay_logs'
AGENT_TYPES = [
    'generic_llm_no',
    'generic_llm_self',
    'generic_rl_fair',
    'generic_rl_self',
    'generic_rl_ss',
]


def process_deal(deal_str):
    items = ['firewood', 'water', 'food']

    # "final_deal": "alice firewood=5 water=12 food=15 bob firewood=5 water=12 food=15",
    pattern = re.compile("alice firewood=[0-9] water=[0-9] food=[0-9] bob firewood=[0-9] water=[0-9] food=[0-9]")
    if not pattern.match(deal_str):
        return {i: 0 for i in items}, {i: 0 for i in items}, 0 

    adeal = {}
    bdeal = {}
    ic = {i: 3 for i in items}

    for i_data in deal_str.split(' bob ')[0].split(' ')[1:]:
        for i in items:
            if i_data.startswith(i):
                adeal[i] = int(i_data.split('=')[1].rstrip(')\n'))
                if adeal[i] == 15:
                    adeal[i] = 1.5

    for i_data in deal_str.split(' bob ')[1].split(' '):
        for i in items:
            if i_data.startswith(i):
                bdeal[i] = int(i_data.split('=')[1].rstrip(')\n'))
                if bdeal[i] == 15:
                    bdeal[i] = 1.5

    agree = 1
    for k in adeal.keys():
        if adeal[k] + bdeal[k] != 3:
            agree = 0
            break

    return adeal, bdeal, agree 


def process_prefs(alice_pref, bob_pref):
    # Alice : firewood=(count:3 value:3) water=(count:3 value:5) food=(count:3 value:4)
    # Bob   : firewood=(count:3 value:3) water=(count:3 value:5) food=(count:3 value:4)
    items = ['firewood', 'water', 'food']
    ap = {}
    bp = {}
    ic = {i: 3 for i in items}

    for i_data in alice_pref.split(': ')[1].split(') '):
        for i in items:
            if i_data.startswith(i):
                ap[i] = int(i_data.split(':')[-1].rstrip(')\n'))

    for i_data in bob_pref.split(': ')[1].split(') '):
        for i in items:
            if i_data.startswith(i):
                bp[i] = int(i_data.split(':')[-1].rstrip(')\n'))

    return ap, bp, ic


def get_sp_stats(f_path):
    convos = json.load(open(f_path, 'r'))
    ap_total = 0
    bp_total = 0
    agree_total = 0
    n_conv = len(convos)

    for c  in convos:
        apref, bpref, ic = process_prefs(c['alice_pref'], c['bob_pref'])

        adeal, bdeal, agree = process_deal(c['final_deal'])
        if len(c['convo']) >= 20:
            agree = 0

        ap_inst = sum([apref[k]*adeal[k] for k in apref.keys()])
        bp_inst = sum([bpref[k]*bdeal[k] for k in bpref.keys()])

        ap_total += ap_inst
        bp_total += bp_inst
        agree_total += agree

    return {
        'alice_rew': ap_total / n_conv,
        'bob_rew': bp_total / n_conv,
        'agree': 100 * (agree_total / n_conv)
    }


def main():
    all_files = os.listdir(DIR_PATH)
    files = []
    for f in all_files:
        if f.endswith('.json'):
            files.append(f)
    files = [f.replace('.json', '') for f in files]

    conf_mat = np.zeros((len(AGENT_TYPES), len(AGENT_TYPES)))
    conf_mat_jp = np.zeros((len(AGENT_TYPES), len(AGENT_TYPES)))

    for f in files:
        # Get line with statistics (last line so final stats)
        f_path = '/'.join([DIR_PATH, f+'.json'])
        
        stats = get_sp_stats(f_path)

        # Get info for agent types
        f_splt = f.split('_vs_')
        alice_type = f_splt[0]
        bob_type = f_splt[1]
        at_index = AGENT_TYPES.index(alice_type)
        bt_index = AGENT_TYPES.index(bob_type)

        if at_index != bt_index:
            # 2nd index on conf matrix is bob
            conf_mat[at_index, bt_index] = stats['alice_rew']
            conf_mat[bt_index, at_index] = stats['bob_rew']
        else:
            conf_mat[at_index, bt_index] = (stats['alice_rew'] + stats['bob_rew']) / 2

        conf_mat_jp[at_index, bt_index] = (stats['alice_rew'] + stats['bob_rew'])
        conf_mat_jp[bt_index, at_index] = (stats['alice_rew'] + stats['bob_rew'])

        # agreement_factor = 1 if stats['agree'] == 0 else 100/stats['agree']
        # conf_mat[at_index, bt_index] *= agreement_factor
        # conf_mat_jp[at_index, bt_index] *= agreement_factor
        # if at_index != bt_index:
        #     conf_mat[bt_index, at_index] *= agreement_factor
        #     conf_mat_jp[bt_index, at_index] *= agreement_factor

    plot = sn.heatmap(conf_mat, annot=True, fmt='.2f', xticklabels=AGENT_TYPES, yticklabels=AGENT_TYPES)  #, cmap="crest"
    plt.title(f'Heatmap for {DIR_PATH} (Alice Points)')
    plt.xlabel('Bob GRU Type')
    plt.ylabel('Alice GRU Type')
    # plt.margins(x=25, y=25)
    plt.savefig(f'{DIR_PATH}/heatmap_alice_points.png')

    plt.clf()

    plot = sn.heatmap(conf_mat_jp, annot=True, fmt='.2f', xticklabels=AGENT_TYPES, yticklabels=AGENT_TYPES)  #, cmap="crest"
    plt.title(f'Heatmap for {DIR_PATH} (Joint Points)')
    plt.xlabel('Bob GRU Type')
    plt.ylabel('Alice GRU Type')
    # plt.margins(x=5, y=5)
    plt.savefig(f'{DIR_PATH}/heatmap_joint_points.png')


if __name__ == '__main__':
    main()