import os
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sn 

DIR_PATH = 'agent_sp_2_22_24' # || 'gru_selfplay_logs'
AGENT_TYPES = [
    'generic_llm_no',
    'generic_llm_self',
    'generic_rl_fair',
    'generic_rl_self',
    'generic_rl_ss',
]


def main():
    all_files = os.listdir(DIR_PATH)
    files = []
    for f in all_files:
        if f.endswith('.log'):
            files.append(f)
    files = [f.replace('.log', '') for f in files]

    conf_mat = np.zeros((len(AGENT_TYPES), len(AGENT_TYPES)))
    conf_mat_jp = np.zeros((len(AGENT_TYPES), len(AGENT_TYPES)))

    for f in files:
        # Get line with statistics (last line so final stats)
        f_path = '/'.join([DIR_PATH, f+'.log'])
        f_lines = open(f_path, 'r').readlines()
        stats_start = 0
        for i, l in enumerate(reversed(f_lines)):
            if l.startswith('\tfull_match='):
                stats_start = -(i+1)
                break
        
        stats = {}
        for i in range(12):
            sl = f_lines[(stats_start - i)]
            sl_splt = sl.split('=')
            stats[sl_splt[0].lstrip('\t')] = float(sl_splt[1].rstrip(' s%\n'))

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

        agreement_factor = 1 if stats['agree'] == 0 else 100/stats['agree']
        conf_mat[at_index, bt_index] *= agreement_factor
        conf_mat_jp[at_index, bt_index] *= agreement_factor
        if at_index != bt_index:
            conf_mat[bt_index, at_index] *= agreement_factor
            conf_mat_jp[bt_index, at_index] *= agreement_factor

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