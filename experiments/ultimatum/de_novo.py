import numpy as np
import random
import math


def default():
    sys_kwargs = {'player1': 'AI system',
                  'player2': 'AI system'}
    random.seed(42)
    experiment_kwargs = {'game': 'ultimatum',
                         'experimental_var': 'temperature',
                         'independent_var': 'pool',
                         'temperature': 1,
                         'pool': list(np.arange(1, 11)[::-1]),
                         'offer': list(np.arange(0, 11)[::-1]),
                         'sys_player1': sys_player1(),
                         'sys_player2': sys_player2()}
    return experiment_kwargs, sys_kwargs


def de_novo():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    return experiment_kwargs, experiment_key


def de_novo_player1_greedy():
    experiment_kwargs, sys_kwargs = default()
    experiment_kwargs['temperature'] = 0
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['pool'] = random.sample(experiment_kwargs['pool'],
                                              math.floor(len(experiment_kwargs['pool']) / 2))
    return experiment_kwargs, experiment_key


def de_novo_player2_greedy():
    experiment_kwargs, sys_kwargs = default()
    experiment_kwargs['temperature'] = 0
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['offer'] = random.sample(experiment_kwargs['offer'],
                                              math.floor(len(experiment_kwargs['offer']) / 2))
    return experiment_kwargs, experiment_key


def de_novo_player1_competence():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
        {'prefix': sys_player1_competence()}
    ]
    return experiment_kwargs, experiment_key


def de_novo_player2_competence():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player2'
    experiment_kwargs[experiment_key] = [
        {'prefix': sys_player2_competence()}
    ]
    return experiment_kwargs, experiment_key


def de_novo_player1_format_ablation():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
        {'prefix': sys_player1_ablation1()},
        {'prefix': sys_player1_ablation2()},
        {'prefix': sys_player1_ablation3()}
    ]
    random.seed(42)
    experiment_kwargs['pool'] = random.sample(experiment_kwargs['pool'],
                                              math.floor(len(experiment_kwargs['pool']) / 2))
    return experiment_kwargs, experiment_key


def de_novo_player1_ablation_subset():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['pool'] = random.sample(experiment_kwargs['pool'],
                                              math.floor(len(experiment_kwargs['pool']) / 2))
    return experiment_kwargs, experiment_key


def de_novo_player2_format_ablation():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player2'
    experiment_kwargs[experiment_key] = [
        {'prefix': sys_player2_ablation1()},
        {'prefix': sys_player2_ablation2()},
        {'prefix': sys_player2_ablation3()}
    ]
    random.seed(42)
    experiment_kwargs['offer'] = random.sample(experiment_kwargs['offer'],
                                              math.floor(len(experiment_kwargs['offer']) / 2))
    return experiment_kwargs, experiment_key


def de_novo_player2_ablation_subset():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'de_novo'
    experiment_kwargs[experiment_key] = [None]
    random.seed(42)
    experiment_kwargs['offer'] = random.sample(experiment_kwargs['offer'],
                                              math.floor(len(experiment_kwargs['offer']) / 2))
    return experiment_kwargs, experiment_key


def sys_player1_premise():
    with open('./games/ultimatum/player1_premise.txt') as f:
        premise = f.read() + '\n\n'
    return premise


def sys_player1_instructions():
    with open('./games/ultimatum/player1_instructions.txt') as f:
        instructions = f.read() + '\n'
    return instructions


def sys_player1_ablation1():
    premise = sys_player1_premise()
    with open('./games/ultimatum/player1_instructions_ablation1.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_ablation2():
    premise = sys_player1_premise()
    with open('./games/ultimatum/player1_instructions_ablation2.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_ablation3():
    premise = sys_player1_premise()
    with open('./games/ultimatum/player1_instructions_ablation3.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_competence():
    premise = sys_player1_premise()
    with open('./games/ultimatum/player1_instructions_competence.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1():
    premise = sys_player1_premise()
    instructions = sys_player1_instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player2_premise():
    with open('./games/ultimatum/player2_premise.txt') as f:
        premise = f.read() + '\n\n'
    return premise


def sys_player2_instructions():
    with open('./games/ultimatum/player2_instructions.txt') as f:
        instructions = f.read() + '\n'
    return instructions


def sys_player2_ablation1():
    premise = sys_player2_premise()
    with open('./games/ultimatum/player2_instructions_ablation1.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player2_ablation2():
    premise = sys_player2_premise()
    with open('./games/ultimatum/player2_instructions_ablation2.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player2_ablation3():
    premise = sys_player2_premise()
    with open('./games/ultimatum/player2_instructions_ablation3.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player2_competence():
    premise = sys_player2_premise()
    with open('./games/ultimatum/player2_instructions_competence.txt') as f:
        instructions = f.read() + '\n'
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player2():
    premise = sys_player2_premise()
    instructions = sys_player2_instructions()
    sys_prompt = premise + instructions
    return sys_prompt

