from experiments.gambling.de_novo import default, de_novo_mixed


def prompting_player1():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse()},
            {'prefix': sys_player1_riskaverse()},
            {'prefix': sys_player1_notlossaverse()},
            {'prefix': sys_player1_lossaverse()},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_greedy():
    experiment_kwargs, sys_kwargs = default()
    experiment_kwargs['temperature'] = 0
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse()},
            {'prefix': sys_player1_riskaverse()},
            {'prefix': sys_player1_notlossaverse()},
            {'prefix': sys_player1_lossaverse()},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_mixed():
    experiment_kwargs, sys_kwargs = de_novo_mixed()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed')},
            {'prefix': sys_player1_riskaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed')},
            {'prefix': sys_player1_notlossaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed')},
            {'prefix': sys_player1_lossaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed')},
    ]
    return experiment_kwargs, experiment_key


def zero_shot_cot_player1():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse() + zero_shot_cot()},
            {'prefix': sys_player1_riskaverse() + zero_shot_cot()},
            {'prefix': sys_player1_notlossaverse() + zero_shot_cot()},
            {'prefix': sys_player1_lossaverse() + zero_shot_cot()},
    ]
    return experiment_kwargs, experiment_key


def zero_shot_cot_player1_mixed():
    experiment_kwargs, sys_kwargs = de_novo_mixed()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed') + zero_shot_cot()},
            {'prefix': sys_player1_riskaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed') + zero_shot_cot()},
            {'prefix': sys_player1_notlossaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed') + zero_shot_cot()},
            {'prefix': sys_player1_lossaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed') + zero_shot_cot()},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_one_shot():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs['ablate'] = True
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse(),
            'example': notriskaverse_example(example_dir='one_side')},
            {'prefix': sys_player1_riskaverse(),
            'example': riskaverse_example(example_dir='one_side')},
            {'prefix': sys_player1_notlossaverse(),
             'example': notlossaverse_example(example_dir='one_side')},
            {'prefix': sys_player1_lossaverse(),
             'example': lossaverse_example(example_dir='one_side')},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_one_shot_mixed():
    experiment_kwargs, sys_kwargs = de_novo_mixed()
    experiment_key = 'sys_player1'
    experiment_kwargs['ablate'] = True
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed'),
            'example': notriskaverse_example(example_dir='one_side_mixed')},
            {'prefix': sys_player1_riskaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed'),
            'example': riskaverse_example(example_dir='one_side_mixed')},
            {'prefix': sys_player1_notlossaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed'),
             'example': notlossaverse_example(example_dir='one_side_mixed')},
            {'prefix': sys_player1_lossaverse(instructions=sys_player1_instructions_mixed, premise_dir='baseline_mixed'),
             'example': lossaverse_example(example_dir='one_side_mixed')},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_two_shot():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs['ablate'] = True
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_notriskaverse(),
            'example': notriskaverse_example(example_dir='both_sides')},
            {'prefix': sys_player1_riskaverse(),
            'example': riskaverse_example(example_dir='both_sides')},
            {'prefix': sys_player1_notlossaverse(),
             'example': notlossaverse_example(example_dir='both_sides')},
            {'prefix': sys_player1_lossaverse(),
             'example': lossaverse_example(example_dir='both_sides')},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_self():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_teenager()},
            {'prefix': sys_player1_middle()},
            {'prefix': sys_player1_senior()},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_self_mixed():
    experiment_kwargs, sys_kwargs = de_novo_mixed()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_teenager(instructions=sys_player1_instructions_mixed, premise_dir='age_self_mixed')},
            {'prefix': sys_player1_middle(instructions=sys_player1_instructions_mixed, premise_dir='age_self_mixed')},
            {'prefix': sys_player1_senior(instructions=sys_player1_instructions_mixed, premise_dir='age_self_mixed')},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_other():
    experiment_kwargs, sys_kwargs = default()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_teenager(premise_dir='age_other')},
            {'prefix': sys_player1_middle(premise_dir='age_other')},
            {'prefix': sys_player1_senior(premise_dir='age_other')},
    ]
    return experiment_kwargs, experiment_key


def prompting_player1_other_mixed():
    experiment_kwargs, sys_kwargs = de_novo_mixed()
    experiment_key = 'sys_player1'
    experiment_kwargs[experiment_key] = [
            {'prefix': sys_player1_teenager(instructions=sys_player1_instructions_mixed, premise_dir='age_other_mixed')},
            {'prefix': sys_player1_middle(instructions=sys_player1_instructions_mixed, premise_dir='age_other_mixed')},
            {'prefix': sys_player1_senior(instructions=sys_player1_instructions_mixed, premise_dir='age_other_mixed')},
    ]
    return experiment_kwargs, experiment_key


def insert_example(text, after_phrase, example):
    text = text.replace(after_phrase, after_phrase + example)
    return text


def zero_shot_cot():
    return "\nLet's think step-by-step.\n"


def sys_player1_instructions_prompting():
    with open('./games/gambling/instructions_ablation1.txt') as f:
        instructions = f.read() + '\n'
    return instructions


def sys_player1_instructions_mixed():
    with open('./games/gambling/mixed_instructions.txt') as f:
        instructions = f.read() + '\n'
    return instructions


def sys_player1_notriskaverse(instructions=sys_player1_instructions_prompting, premise_dir='baseline'):
    premise = notriskaverse_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_notlossaverse(instructions=sys_player1_instructions_prompting, premise_dir='baseline'):
    premise = notlossaverse_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_riskaverse(instructions=sys_player1_instructions_prompting, premise_dir='baseline'):
    premise = riskaverse_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_lossaverse(instructions=sys_player1_instructions_prompting, premise_dir='baseline'):
    premise = lossaverse_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_teenager(instructions=sys_player1_instructions_prompting, premise_dir='age_self'):
    premise = teenager_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_middle(instructions=sys_player1_instructions_prompting, premise_dir='age_self'):
    premise = middle_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


def sys_player1_senior(instructions=sys_player1_instructions_prompting, premise_dir='age_self'):
    premise = senior_premise(premise_dir=premise_dir)
    instructions = instructions()
    sys_prompt = premise + instructions
    return sys_prompt


# Premise


def notriskaverse_premise(premise_dir='baseline'):
    with open('./games/gambling/%s/player1_premise_notriskaverse.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


def notlossaverse_premise(premise_dir='baseline'):
    with open('./games/gambling/%s/player1_premise_notlossaverse.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


def riskaverse_premise(premise_dir='baseline'):
    with open('./games/gambling/%s/player1_premise_riskaverse.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


def lossaverse_premise(premise_dir='baseline'):
    with open('./games/gambling/%s/player1_premise_lossaverse.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


def teenager_premise(premise_dir='age_self'):
    with open('./games/gambling/%s/player1_premise_teenager.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


def middle_premise(premise_dir='age_self'):
    with open('./games/gambling/%s/player1_premise_middle.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


def senior_premise(premise_dir='age_self'):
    with open('./games/gambling/%s/player1_premise_senior.txt' % premise_dir) as f:
        premise = f.read() + '\n'
    return premise


# Examples


def notriskaverse_example(example_dir='both_sides'):
    return './examples/notriskaverse/{example_dir}/%d.txt'.format(example_dir=example_dir)


def notlossaverse_example(example_dir='both_sides'):
    return './examples/notlossaverse/{example_dir}/%d.txt'.format(example_dir=example_dir)


def riskaverse_example(example_dir='both_sides'):
    return './examples/riskaverse/{example_dir}/%d.txt'.format(example_dir=example_dir)


def lossaverse_example(example_dir='both_sides'):
    return './examples/lossaverse/{example_dir}/%d.txt'.format(example_dir=example_dir)
