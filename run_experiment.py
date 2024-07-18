import json
import torch
import openai
import argparse
import os
from tqdm import tqdm
import gc
import time

from games import Ultimatum, Gambling, Wait
from players import Llama2Player, MistralPlayer, GPTPlayer, GeminiPlayer, ClaudePlayer, DeterministicProposalPlayer, EmptyPlayer
import experiments.ultimatum.de_novo as ultimatum_de_novo
import experiments.gambling.de_novo as gambling_de_novo
import experiments.gambling.prompts as gambling_prompts
import experiments.wait.de_novo as wait_de_novo


parser = argparse.ArgumentParser()
# Core
parser.add_argument('--game', help='Game to play: ultimatum, gambling, wait', type=str, default='ultimatum')
parser.add_argument('--players', help='Comma-separated list of players: random, gpt-4, gpt-3.5-turbo', type=str, default='gpt-3.5-turbo,gpt-3.5-turbo')
parser.add_argument('--experiment', type=str, default='de_novo')
parser.add_argument('--experiment_var', help='temperature, prompts', type=str, default='temperature')
parser.add_argument('--independent_var', type=str, default='pool')
# Settings
parser.add_argument('--num_trials', help='Number of times to run game', type=int, default=1)
parser.add_argument('--start_idx', help='Not 0,0 if adding more data to existing experiment', type=str, default='0,0')
parser.add_argument('--regenerate_all', help='Regenerate', type=bool, default=False)
parser.add_argument('--regenerate_bad', help='Regenerate', type=bool, default=False)
args = parser.parse_args()


def main():
    # Set API keys
    set_keys()

    # Create directory for this game
    experiment_path = "./results/%s_%s/%s" % (args.game, args.players.strip().replace(',', '-'), args.experiment)
    os.makedirs(experiment_path, exist_ok=True)
    
    # Run experiment
    run_experiment(args.game, args.players, args.experiment, args.num_trials, args.start_idx, args.regenerate_all, args.regenerate_bad, args.experiment_var, args.independent_var, experiment_path)
    return


def run_experiment(game_type, players, experiment, num_trials, start_idx, regenerate_all, regenerate_bad, experiment_var, independent_var, experiment_path):
    """
    Each experiment is over two variables:
        1. Experimental parameter (e.g., temperature) - measures the effect of the experimental intervention
        2. Independent variable (e.g., pool) - measures strategic consistency
    """
    experiment_kwargs, experiment_key = get_experiment(game_type, experiment)
    start_idx = [int(i) for i in start_idx.split(',')]

    game = create_game(game_type, players, **experiment_kwargs)
    
    # Iterate over experimental parameter
    for e_idx, e in enumerate(experiment_kwargs[experiment_key]):
        # Checkpointing if need to restart
        if e_idx < start_idx[0]:
            continue
        elif e_idx == start_idx[0]+1:
            start_idx[1] = 0
        
        # Make directory for this parameter
        if len(experiment_kwargs[experiment_key]) > 1:
            param_path = os.path.join(experiment_path, "%d" % e_idx)
        else:
            param_path = experiment_path
        os.makedirs(param_path, exist_ok=True)

        # Set kwargs for this iteration
        e_kwargs = experiment_kwargs.copy()
        e_kwargs[experiment_key] = e
        
        # Set all other independent variables to default
        other_vars = [key for key in e_kwargs.keys() if isinstance(e_kwargs[key], list)]
        for v in other_vars:
            if v != independent_var:
                # Default is first value
                e_kwargs[v] = e_kwargs[v][0]

        # Run the game for this experimental parameter over the independent variable
        run_independent(experiment_var, independent_var, game, game_type, players, num_trials, param_path, start_idx, regenerate_all, regenerate_bad, experiment_key, e_kwargs)
    return


def run_independent(experiment_var, independent_var, game, game_type, players, num_trials, param_path, start_idx, regenerate_all, regenerate_bad, experiment_key, e_kwargs):
    r_kwargs = e_kwargs.copy()
    var_path = os.path.join(param_path, '%s' % independent_var)

    # Iterate over possible values of independent variable
    for r_idx, r in enumerate(e_kwargs[independent_var]):
        if r_idx < start_idx[1]:
            continue

        # Make directory for this value
        r_path = os.path.join(var_path, os.path.basename(str(r)))
        os.makedirs(r_path, exist_ok=True)

        # Set kwargs for this iteration
        r_kwargs[independent_var] = r 
        game.set_param(r_kwargs)

        # Run repeat trials over independent variable to get confidence interval
        for i in tqdm(range(num_trials)):
            file_name = set_file_name(experiment_var, i)
            # Check if file already exists
            if os.path.exists(os.path.join(r_path, file_name)):
                if not regenerate_all and not regenerate_bad:
                    continue
                if regenerate_bad and check_game(game_type, game, os.path.join(r_path, file_name)):
                    continue
            if 'sys' in experiment_key:
                game = load_example(game, experiment_var, experiment_key, e_kwargs, i)

            # If sampling at temperature > 0, just run again
            game.play()
            game.save(os.path.join(r_path, file_name))
            time.sleep(1.01)
        
        gc.collect()
        torch.cuda.empty_cache()
    return


def set_file_name(experiment_var, i):
    if experiment_var == 'prompts':
        file_name = "%d-prompt.json" % i
    elif experiment_var == 'temperature':
        file_name = "%d-temp.json" % i
    return file_name


def check_game(game_type, game, file_path):
    ans = None
    with open(file_path) as f:    
        r = json.load(f)
    if game_type == 'ultimatum':
        ans = game.get_offer(r['player-res'])
    elif 'gambling' in game_type:
        ans = game.get_choice(r['player-prompt'], r['player-res'])
    return ans


def load_example(game, experiment_var, experiment_key, e_kwargs, i):
    if experiment_var == 'temperature':
        i = 0
    sys_prompt = e_kwargs[experiment_key]['prefix']
    if 'context' in e_kwargs[experiment_key].keys():
        with open(e_kwargs[experiment_key]['context'] % i) as f:
            context = f.read()
        sys_prompt = sys_prompt + "\n" + context
    elif 'example' in e_kwargs[experiment_key].keys():
        # If experiment is over examples, reset player sys prompts
        with open(e_kwargs[experiment_key]['example'] % i) as f:
            example = f.read()
        sys_prompt = sys_prompt + "\nHere's an example:\n" + example + "\n"
    game.player1.set_sys(sys_prompt)
    game.game_kwargs[experiment_key] = sys_prompt
    return game


def get_experiment(game_type, experiment):
    experiment_kwargs = {}
    experiment_key = ''
    if game_type == 'ultimatum':
        if experiment == 'de_novo':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo()
        elif experiment == 'de_novo_player1_greedy':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player1_greedy()
        elif experiment == 'de_novo_player1_ablation_subset':   # Need to compare format ablation to same subset
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player1_ablation_subset()
        elif experiment == 'de_novo_player1_format_ablation':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player1_format_ablation()
        elif experiment == 'de_novo_player2_greedy':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player2_greedy()
        elif experiment == 'de_novo_player2_ablation_subset':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player2_ablation_subset()
        elif experiment == 'de_novo_player2_format_ablation':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player2_format_ablation()
        elif experiment == 'de_novo_player1_competence':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player1_competence()
        elif experiment == 'de_novo_player2_competence':
            experiment_kwargs, experiment_key = ultimatum_de_novo.de_novo_player2_competence()
    elif game_type == 'gambling':
        if experiment == 'de_novo':
            experiment_kwargs, experiment_key = gambling_de_novo.de_novo()
        elif experiment == 'de_novo_mixed':
            experiment_kwargs, experiment_key = gambling_de_novo.de_novo_mixed()
        elif experiment == 'de_novo_greedy':
            experiment_kwargs, experiment_key = gambling_de_novo.de_novo_greedy()
        elif experiment == 'de_novo_player1_ablation_subset':
            experiment_kwargs, experiment_key = gambling_de_novo.de_novo_player1_ablation_subset()
        elif experiment == 'de_novo_player1_format_ablation':
            experiment_kwargs, experiment_key = gambling_de_novo.de_novo_player1_format_ablation()
        elif experiment == 'de_novo_player1_choice_ablation':
            experiment_kwargs, experiment_key = gambling_de_novo.de_novo_player1_choice_ablation()
        elif experiment in ['prompting', 'prompting_mixed', 'prompting_one_shot', 'prompting_one_shot_mixed',
                            'prompting_two_shot', 'prompting_self', 'prompting_self_mixed', 'prompting_other',
                            'prompting_other_mixed', 'prompting_zero_shot_cot', 'prompting_zero_shot_cot_mixed']:
            experiment_kwargs, experiment_key = get_prompt_experiment(experiment, gambling_prompts)
    elif game_type == 'wait':
        if experiment == 'de_novo':
            experiment_kwargs, experiment_key = wait_de_novo.de_novo()
        elif experiment == 'de_novo_greedy':
            experiment_kwargs, experiment_key = wait_de_novo.de_novo_greedy()
        elif experiment == 'de_novo_player1_format_ablation':
            experiment_kwargs, experiment_key = wait_de_novo.de_novo_player1_format_ablation()
        elif experiment == 'de_novo_player1_mc_ablation':
            experiment_kwargs, experiment_key = wait_de_novo.de_novo_player1_mc_ablation()
    return experiment_kwargs, experiment_key


def get_prompt_experiment(experiment, prompt_package):
    experiment_kwargs = {}
    experiment_key = ''
    if experiment == 'prompting':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1()
    elif experiment == 'prompting_one_shot':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_one_shot()
    elif experiment == 'prompting_one_shot_mixed':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_one_shot_mixed()
    elif experiment == 'prompting_two_shot':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_two_shot()
    elif experiment == 'prompting_mixed':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_mixed()
    elif experiment == 'prompting_self':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_self()
    elif experiment == 'prompting_self_mixed':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_self_mixed()
    elif experiment == 'prompting_other':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_other()
    elif experiment == 'prompting_other_mixed':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_other_mixed()
    elif experiment == 'prompting_greedy':
        experiment_kwargs, experiment_key = prompt_package.prompting_player1_greedy()
    elif experiment == 'prompting_zero_shot_cot':
        experiment_kwargs, experiment_key = prompt_package.zero_shot_cot_player1()
    elif experiment == 'prompting_zero_shot_cot_mixed':
        experiment_kwargs, experiment_key = prompt_package.zero_shot_cot_player1_mixed()
    return experiment_kwargs, experiment_key


def create_game(game_type, players_type, **experiment_kwargs):
    players_type = players_type.strip().split(',')
    if game_type == 'ultimatum':
        assert(len(players_type) == 2)
        players = []
        for i, player_type in enumerate(players_type):
            sys_key = 'sys_player%d' % (i+1)
            players.append(create_player(player_type, sys_key, **experiment_kwargs))
        game = Ultimatum(players[0], players[1], **experiment_kwargs)
    elif game_type == 'gambling':
        assert(len(players_type) == 1)
        player = create_player(players_type[0], 'sys_player1', **experiment_kwargs)
        game = Gambling(player, **experiment_kwargs)
    elif game_type == 'wait':
        assert(len(players_type) == 1)
        player = create_player(players_type[0], 'sys_player1', **experiment_kwargs)
        game = Wait(player, **experiment_kwargs)
    return game


def create_player(player_type, sys_key, **experiment_kwargs):
    if 'Llama-2' in player_type:
        player = Llama2Player(player_type, sys_key, **experiment_kwargs)
    elif 'Llama-3' in player_type:
        player = Llama3Player(player_type, sys_key, **experiment_kwargs)
    elif 'Mistral' in player_type:
        player = MistralPlayer(player_type, sys_key, **experiment_kwargs)
    elif 'gemini' in player_type:
        player = GeminiPlayer(player_type, sys_key, **experiment_kwargs)
    elif 'gpt' in player_type:
        player = GPTPlayer(player_type, sys_key, **experiment_kwargs)
    elif 'claude' in player_type:
        player = ClaudePlayer(player_type, sys_key, **experiment_kwargs)
    elif player_type == 'deterministic':
        if experiment_kwargs['game'] == 'ultimatum':
            player = DeterministicProposalPlayer(**experiment_kwargs)
    elif player_type == 'empty':
        player = EmptyPlayer()
    return player


def set_keys():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    openai.api_key = config_data.get("openai_api_key")
    hf_token = config_data.get("hf_key")
    google_key = config_data.get("google_key")
    anthropic_key = config_data.get("anthropic_key")
    os.environ["OPENAI_API_KEY"] = openai.api_key
    os.environ["HF_KEY"] = hf_token
    os.environ["GOOGLE_KEY"] = google_key
    os.environ["ANTHROPIC_KEY"] = anthropic_key
    return


if __name__ == "__main__":
    main()

