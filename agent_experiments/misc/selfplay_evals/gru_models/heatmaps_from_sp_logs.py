import os
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sn 

DIR_PATH = 'gru_fixed_data_selfplay_logs' # || 'gru_selfplay_logs'
AGENT_TYPES = [
    'sup',
    'fair',
    'selfvself',
    'selfish',
]


def main():
    all_files = os.listdir(DIR_PATH)
    files = []
    for f in all_files:
        if f.endswith('.log'):
            files.append(f)
    files = [f.replace('.log', '') for f in files]

    conf_mat = np.zeros((len(AGENT_TYPES), len(AGENT_TYPES)))

    for f in files:
        f_splt = f.split('_')
        alice_type = f_splt[-3]
        bob_type = f_splt[-1]

        # Get line with statistics (last line so final stats)
        f_path = '/'.join([DIR_PATH, f+'.log'])
        f_lines = open(f_path, 'r').readlines()
        stats_line = ''
        for l in reversed(f_lines):
            if l.startswith('dialog_len='):
                stats_line = l
                break
        stats = {s.split('=')[0]:float(s.split('=')[1].rstrip('s%\n')) for s in stats_line.split(' ')}
        
        at_index = AGENT_TYPES.index(alice_type)
        bt_index = AGENT_TYPES.index(bob_type)

        if at_index != bt_index:
            # 2nd index on conf matrix is bob
            conf_mat[at_index, bt_index] = stats['alice_rew']
            conf_mat[bt_index, at_index] = stats['bob_rew']
        else:
            conf_mat[at_index, bt_index] = (stats['alice_rew'] + stats['bob_rew']) / 2

        # conf_mat[at_index, bt_index] = (stats['alice_rew'] + stats['bob_rew'])
        # conf_mat[bt_index, at_index] = (stats['alice_rew'] + stats['bob_rew'])

    plot = sn.heatmap(conf_mat, annot=True, fmt='.2f', xticklabels=AGENT_TYPES, yticklabels=AGENT_TYPES)  #, cmap="crest"
    plt.title(f'Heatmap for {DIR_PATH} (Alice Points)')
    plt.xlabel('Bob GRU Type')
    plt.ylabel('Alice GRU Type')
    plt.savefig(f'{DIR_PATH}/heatmap_alice_points.png')


if __name__ == '__main__':
    main()