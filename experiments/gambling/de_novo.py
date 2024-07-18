import random
import math


def default():
    sys_kwargs = {'player': ''}
    experiment_kwargs = {'game': 'prospect',
                         'experimental_var': 'temperature',
                         'independent_var': 'question',
                         'temperature': 1,
                         'ablate': False,
                         'mixed': False,
                         'question': prospects(),
                         'sys_player1': sys_player1()}
    return experiment_kwargs, sys_kwargs


def de_novo():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    return experiment_kwargs, experiment_key


def de_novo_mixed():
    experiment_kwargs, sys_kwargs = default()
    experiment_kwargs['mixed'] = True
    experiment_kwargs['sys_player1'] = sys_player1_mixed()
    experiment_kwargs['question'] = [[-50, 0.25],
                                     [-50, 0.50],
                                     [-50, 0.75],
                                     [-50, 0.90],
                                     [-100, 0.25],
                                     [-100, 0.50],
                                     [-100, 0.75],
                                     [-100, 0.90],
                                     [-150, 0.25],
                                     [-150, 0.50],
                                     [-150, 0.75],
                                     [-150, 0.90],
                                     [-200, 0.25],
                                     [-200, 0.50],
                                     [-200, 0.75],
                                     [-200, 0.90],
                                     [-400, 0.25],
                                     [-400, 0.50],
                                     [-400, 0.75],
                                     [-400, 0.90]]
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


def prospects():
    prospects = [[0, 0.9, 50, 0.1],
     [0, 0.5, 50, 0.5],
     [0, 0.1, 50, 0.9],
     [0, 0.95, 100, 0.05],
     [0, 0.75, 100, 0.25],
     [0, 0.5, 100, 0.5],
     [0, 0.25, 100, 0.75],
     [0, 0.05, 100, 0.95],
     [0, 0.99, 200, 0.01],
     [0, 0.9, 200, 0.1],
     [0, 0.5, 200, 0.5],
     [0, 0.1, 200, 0.9],
     [0, 0.01, 200, 0.99],
     [0, 0.99, 400, 0.01],
     [0, 0.9, 400, 0.1],
     [0, 0.5, 400, 0.5],
     [0, 0.01, 400, 0.99],
     [50, 0.9, 100, 0.1],
     [50, 0.5, 100, 0.5],
     [50, 0.1, 100, 0.9],
     [50, 0.95, 150, 0.05],
     [50, 0.75, 150, 0.25],
     [50, 0.5, 150, 0.75],
     [50, 0.25, 150, 0.75],
     [50, 0.05, 150, 0.95],
     [100, 0.95, 200, 0.05],
     [100, 0.75, 200, 0.25],
     [100, 0.5, 200, 0.5],
     [100, 0.25, 200, 0.75],
     [100, 0.05, 200, 0.95],
     [200, 0.5, 400, 0.5],
     [200, 0.75, 400, 0.25],
     [200, 0.9, 400, 0.1],
     [200, 0.95, 400, 0.05]]
    neg_prospects = [[-1*a, b, -1*c, d] for a, b, c, d in prospects]
    return prospects + neg_prospects


def de_novo_player1_choice_ablation():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    experiment_kwargs['ablate'] = True
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                                  math.floor(len(experiment_kwargs['question']) / 4))
    return experiment_kwargs, experiment_key


def de_novo_player1_format_ablation():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
        {'prefix': sys_player1_ablation1()},
    ]
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                              math.floor(len(experiment_kwargs['question']) / 4))
    return experiment_kwargs, experiment_key


def de_novo_player1_ablation_subset():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['question'] = random.sample(experiment_kwargs['question'],
                                              math.floor(len(experiment_kwargs['question']) / 4))
    return experiment_kwargs, experiment_key


def sys_player1():
    premise = sys_player1_premise()
    instructions = sys_player1_instructions()
    return premise + instructions


def sys_player1_ablation1():
    premise = sys_player1_premise()
    with open('./games/gambling/instructions_ablation1.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_premise():
    with open('./games/gambling/premise.txt') as f:
        premise = f.read() + '\n\n'
    return premise


def sys_player1_instructions():
    with open('./games/gambling/instructions.txt') as f:
        instructions = f.read() + '\n'
    return instructions


def sys_player1_mixed():
    premise = sys_player1_premise_mixed()
    instructions = sys_player1_instructions_mixed()
    return premise + instructions


def sys_player1_premise_mixed():
    with open('./games/gambling/mixed_premise.txt') as f:
        premise = f.read() + '\n\n'
    return premise


def sys_player1_instructions_mixed():
    with open('./games/gambling/mixed_instructions.txt') as f:
        instructions = f.read() + '\n'
    return instructions
