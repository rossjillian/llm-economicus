import random
import math


def default():
    sys_kwargs = {'player': ''}
    experiment_kwargs = {'game': 'prospect',
                         'experimental_var': 'temperature',
                         'independent_var': 'question',
                         'temperature': 1,
                         'ablate': False,
                         'question': comps(),
                         'sys_player1': sys_player1()}
    return experiment_kwargs, sys_kwargs


def de_novo():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    return experiment_kwargs, experiment_key


def de_novo_greedy():
    experiment_kwargs, sys_kwargs = default()
    experiment_kwargs['temperature'] = 0
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                                  math.floor(len(experiment_kwargs['question']) / 4))
    return experiment_kwargs, experiment_key


def comps():
    comps = []
    # Iterate over time delays
    for d in ["1 month", "6 months", "1 year", "5 years", "10 years", "25 years", "50 years"]:
        # Iterate over current values
        for v in [1000, 990, 980, 960, 940, 920, 900,
                  850, 800, 750, 700, 650, 600, 550, 500,
                  450, 400, 350, 300, 250, 200, 150, 100,
                  80, 60, 40, 20, 10, 5, 1, 0]:
            comps.append(["$1000 in %s" % d, "$%d now" % v])
    return comps


def de_novo_player1_ablation_subset():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                              math.floor(len(experiment_kwargs['question']) / 4))
    return experiment_kwargs, experiment_key


def de_novo_player1_format_ablation():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
        {'prefix': sys_player1_ablation1()}
    ]
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                              math.floor(len(experiment_kwargs['question']) / 4))
    print(experiment_kwargs['question'])
    return experiment_kwargs, experiment_key


def de_novo_player1_mc_ablation():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    experiment_kwargs['ablate'] = True
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                                  math.floor(len(experiment_kwargs['question']) / 4))
    return experiment_kwargs, experiment_key


def sys_player1_ablation1():
    premise = sys_player1_premise()
    with open('./games/wait/instructions_ablation1.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1():
    premise = sys_player1_premise()
    instructions = sys_player1_instructions()
    return premise + instructions


def sys_player1_premise():
    with open('./games/wait/premise.txt') as f:
        premise = f.read() + '\n\n'
    return premise


def sys_player1_instructions():
    with open('./games/wait/instructions.txt') as f:
        instructions = f.read() + '\n'
    return instructions
