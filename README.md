# LLM economicus? Mapping the Behavioral Biases of LLMs via Utility Theory

This is the code base for our paper accepted to COLM 2024. Please report any ambiguity or mistakes to `jillianr [at] mit [dot] edu`.

## Generate Data

All data can be generated from `run_experiments.py`. Specify:
- `--game`: game type
- `--players`: comma-separated list of players 
- `--experiment`: experiment type 
- `--experiment_var`: if you're sampling over `temperature` or over different `prompts`
- `--independent_var`: what aspect of the game you're varying. For example, in the ultimatum game, you might vary the pool which the first player can offer from 

There are several types of experiments:
- `de_novo`: baseline behavior (Section 3, Appendix D.1)
- `de_novo_greedy`: baseline behavior with greedy decoding (Appendix D.4)
- `format_ablation`: ablation on answer format (Appendix D.3)
- `mc_ablation`: ablation on multiple choice options (Appendix D.3)
- `prompting`: prompting intervention (Section 4)

To run the code, be sure to specify your API keys in `config.json` in the main directory. Also be sure to create a virtual environment with the requisite packages in `requirements.txt`:

`pip install -r requirements.txt`

### Section 3.1: Ultimatum Game

The ultimatum game is a two-player game (`player1`, `player2`). One player (`player1`) is a proposer, and the other player is a responder (`player2`). We probe the LLM as each player separately, so only one player is a LLM per experiment. The other player is `deterministic` (if the LLM is `player2`) or `empty` (if the LLM is `player1`). You need to specify the two `--players` as a comma-separated list, i.e. `--players=gpt-4-0125-preview,empty` or `--players=deterministic,gpt-4-0125-preview`. 

The proposer has `pool` dollars (independent variable for the proposer) and will choose to offer some portion {c} of those dollars to the responder. The responder is given `offer` dollars (independent variable for the responder) and will choose to accept or reject the offer. The responder has the option to either accept or reject the offer. If they reject the offer, the proposer and the other player both get nothing. If they accept the offer, the responder gets {c} dollars and the proposer gets {p - c} dollars. You can find the specific prompts for the ultimatum game in the `games/ultimatum` directory.

Example run (proposer): `python3 -m run_experiment --game=ultimatum --players=gpt-4-0125-preview,empty --experiment=de_novo --experiment_var=temperature --independent_var=pool`

Example run (responder): `python3 -m run_experiment --game=ultimatum --players=deterministic,gpt-4-0125-preview --experiment=de_novo --experiment_var=temperature --independent_var=offer
`

### Section 3.2: Gambling Game

The gambling game is a one-player game (`player1`). You can just specify one player as a string, i.e. `--players=gpt-4-preview-0125`.

The player is asked a `question` (independent variable for the player) about a series of possible gambles. You can find the specific prompts for the gambling game in the `games/gambling` directory.

Example run: `python3 -m run_experiment --game=gambling --players=gpt-4-0125-preview --experiment=de_novo --experiment_var=temperature --independent_var=question`


### Section 3.3: Waiting Game

The waiting game is a one-player game (`player1`). You can just specify one player as a string, i.e. `--players=gpt-4-0125-preview`.

The player is asked a `question` (independent variable for the player) to choose between two options. You can find the specific prompts for the ultimatum game in the `games/wait` directory.

Example run: `python3 -m run_experiment --game=wait --players=gpt-4-0125-preview --experiment=de_novo --experiment_var=temperature --independent_var=question`

## Citation

If you find our work helpful, please cite it as:

```angular2html
@article{
    title={LLM economicus? Mapping the Behavioral Biases of LLMs via Utility Theory},
    author={Ross, Jillian and Kim, Yoon and Lo, Andrew W.},
    journal={arXiv preprint arXiv:},
    year={2024}
}
```