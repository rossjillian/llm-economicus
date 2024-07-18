import random
import re
import json
import numpy as np


class Ultimatum:
    def __init__(self, player1, player2, **game_kwargs):
        self.game_kwargs = game_kwargs
        self.player1 = player1
        self.player2 = player2
        self.log = {}

    def set_param(self, r_kwargs):
        for k, v in r_kwargs.items():
            if k in self.game_kwargs:
                self.game_kwargs[k] = v

    def play(self, max_attempts=10):
        self.player1.update(player_id='player1', **self.game_kwargs)
        self.player2.update(player_id='player2', **self.game_kwargs)
        print("SYSTEM PROMPT")
        print(self.player1.sys_prompt)
        self.log['player1-sys'] = self.player1.sys_prompt
        player1_prompt = self.write_player1_prompt()
        # Error handling if model does not return in parsable format
        self.log['player1-retries'] = 0
        for attempt in range(1, max_attempts + 1):
            self.log['player1-prompt'] = player1_prompt
            print("USER PROMPT")
            print(player1_prompt)
            player1_res = self.player1.decide(player1_prompt)
            self.log['player1-res'] = player1_res
            print("PROPOSER RESPONSE")
            print(player1_res)
            offer = self.get_offer(player1_res)
            if offer is not None:
                break
            elif offer is None and attempt == max_attempts:
                raise ValueError("Failed to obtain a valid offer")
            self.log['player1-retries'] += 1
        print("SYSTEM PROMPT")
        print(self.player2.sys_prompt)
        self.log['player2-sys'] = self.player2.sys_prompt
        player2_prompt = self.write_player2_prompt(offer)
        self.log['player2-retries'] = 0
        for attempt in range(1, max_attempts + 1):
            self.log['player2-prompt'] = player2_prompt
            print("USER PROMPT")
            print(player2_prompt)
            player2_res = self.player2.decide(player2_prompt)
            self.log['player2-res'] = player2_res
            print("RESPONDER RESPONSE")
            print(player2_res)
            decision = self.get_decision(player2_res)
            if decision is not None:
                break
            elif decision is None and attempt == max_attempts:
                raise ValueError("Failed to obtain a valid offer")
            self.log['player2-retries'] += 1
        return self.log

    def write_player1_prompt(self):
        player1_prompt = ("You have %d dollars. "
                          "How much do you offer?") % self.game_kwargs['pool']
        return player1_prompt

    def write_player2_prompt(self, offer):
        player2_prompt = ("The other player has %d dollars. "
                          "They offer you %d dollars. "
                          "Do you accept or reject the offer?") % (self.game_kwargs['pool'], offer)
        return player2_prompt

    def get_offer(self, response):
        pattern = r"Offer:\s*[\$]?([0-9]+(?:\.[0-9]+)?)"
        match = re.search(pattern, response, re.IGNORECASE)
        # Check if a match is found
        if match:
            try:
                offer = int(match.group(1))
            except ValueError:
                # Conversion to int failed
                offer = None
        else:
            offer = None
        return offer

    def get_decision(self, response):
        try:
            pattern = r"Decision:\s*(accept|reject)"
            match = re.search(pattern, response, re.IGNORECASE)
            # Check if a match is found
            if match:
                decision = match.group(1)
            elif 'accept' in response.split("Decision:")[1] and 'reject' not in response.split("Decision:")[1]:
                decision = 'accept'
            elif 'reject' in response.split("Decision:")[1] and 'accept' not in response.split("Decision:")[1]:
                decision = 'reject'
            else:
                decision = None
            return decision
        except:
            return None

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.log, f)
        return


class Gambling:
    def __init__(self, player, **game_kwargs):
        self.game_kwargs = game_kwargs
        self.player1 = player
        self.ablate = game_kwargs['ablate']
        self.log = {}

    def set_param(self, r_kwargs):
        for k, v in r_kwargs.items():
            if k in self.game_kwargs:
                self.game_kwargs[k] = v

    def play(self, max_attempts=1):
        self.player1.update(**self.game_kwargs)
        self.question = self.game_kwargs['question']
        print("SYSTEM PROMPT")
        print(self.player1.sys_prompt)
        self.log['player-sys'] = self.player1.sys_prompt
        if self.game_kwargs['mixed'] is False:
            expected_val = (self.question[1] * self.question[0]) + (self.question[3] * self.question[2])
            # Generate logarithmically spaced points between 0 and 1
            log_spaced_points = np.logspace(0, 1, 7, endpoint=True)
            # Scale these points to the range between min_outcome and max_outcome
            scaled_points = self.question[0] + (self.question[2] - self.question[0]) * (log_spaced_points - 1) / (
                        10 - 1)
            # Round the outcomes to two decimal places
            sure_outcomes = [round(outcome, 2) for outcome in scaled_points]
            sure_outcomes.sort(reverse=True)
            player_prompt = self.write_player_prompt(expected_val, sure_outcomes)
        else:
            log_spaced_points = np.logspace(0, 1, 7, endpoint=True)
            breakeven = (self.question[0] * self.question[1]) / (1 - self.question[1])
            # Scale these points to the range between min_outcome and max_outcome
            min_gamble = breakeven - (breakeven * 0.25)
            max_gamble = breakeven + (breakeven * 0.75)
            scaled_points = min_gamble + (max_gamble - min_gamble) * (log_spaced_points - 1) / (10 - 1)
            # Round the outcomes to two decimal places
            gambles = [-1 * round(outcome, 2) for outcome in scaled_points]
            gambles.sort(reverse=True)
            player_prompt = self.write_mixed_player_prompt(gambles)

        # Error handling if model does not return in parsable format
        for attempt in range(1, max_attempts + 1):
            self.log['player-prompt'] = player_prompt
            print("USER PROMPT")
            print(player_prompt)
            player_res = self.player1.decide(player_prompt)
            self.log['player-res'] = player_res
            print("RESPONSE")
            print(player_res)
            lowest, highest = self.get_choice(player_prompt, player_res)
            print("LOWEST")
            print(lowest)
            print("HIGHEST")
            print(highest)
            # if lowest is not None and highest is not None:
            #    break
            # elif lowest is not None and highest is not None and attempt == max_attempts:
            #    raise ValueError("Failed to obtain a valid answer")
        return self.log

    def write_player_prompt(self, expected_val, sure_outcomes):
        player_prompt = (
                "The prospect is %.2f dollars with %d%% probability and %.2f dollars with %d%% probability. "
                "The expected value of the prospect is %.2f dollars.\n" %
                (self.question[0], self.question[1] * 100, self.question[2], self.question[3] * 100,
                 expected_val))

        player_prompt += "Below are the alternative sure outcomes.\n"
        if self.ablate:
            random.shuffle(sure_outcomes)
        for i, outcome in enumerate(sure_outcomes):
            player_prompt = player_prompt + ("%.2f dollars with 100%% probability\n" % outcome)
        if self.player1.model_type == 'base':
            player_prompt = player_prompt + "\nI choose: "
        return player_prompt

    def write_mixed_player_prompt(self, gambles):
        player_prompt = ("The prospect is %.2f dollars with %d%% probability.") % (
            self.question[0], self.question[1] * 100)
        player_prompt += "\nBelow are the gambles.\n"
        for i, gamble in enumerate(gambles):
            expected_val = (gamble * (1 - self.question[1])) + (self.question[0] * self.question[1])
            player_prompt = player_prompt + ("%.2f dollars with %d%% probability. The expected value is"
                                             " %2.f dollars.\n") % (
                                gamble, (1 - self.question[1]) * 100, expected_val)
        if self.player1.model_type == 'base':
            player_prompt = player_prompt + "I choose: "
        return player_prompt

    def get_choice(self, prompt, text):
        lowest, highest = None, None
        count = 0
        try:
            amts = [p.split(' ')[0] for p in prompt.rstrip().split('\n')[2:]]
            sure_options = {i + 1: a for i, a in enumerate(amts)}
            i = 1
            for res in text.split('\n'):
                if len(res.split(':')) == 1:
                    continue
                clean_res = res.split(':')[1].strip().replace('{', '').replace('}', '').lower()
                clean_num = \
                res.split(':')[0].strip().replace('{', '').replace('}', '').replace('$', '').replace('(', '').replace(
                    ')', '').split(' ')[0]
                clean_num = re.sub(r'[^\x00-\x7F]+', '-', clean_num)
                if ('100%' not in res.split(':')[0] and 'sure option' not in res.split(':')[
                    0].lower() and clean_num not in amts):
                    continue
                print(res.split(':')[0].lower())
                if 'sure option' in res.split(':')[0].lower():
                    clean_num = sure_options[i]
                    i += 1
                if clean_res == 'reject':
                    new_highest = float(clean_num)
                    count += 1
                    if highest is None:
                        highest = new_highest
                    elif new_highest > highest:
                        highest = new_highest
                elif clean_res == 'accept':
                    new_lowest = float(clean_num)
                    count += 1
                    if lowest is None:
                        lowest = new_lowest
                    elif new_lowest < lowest:
                        lowest = new_lowest
        except:
            print("Exception (likely parsing)...")
            count = 0
            lowest = None
            highest = None
        if count != 7:
            print("Fail: count does not equal 7")
            lowest = None
            highest = None
        else:
            if lowest is None:
                lowest = float('-inf')
            if highest is None:
                highest = float('inf')
        return lowest, highest

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.log, f)
        return


class Wait:
    def __init__(self, player, **game_kwargs):
        self.game_kwargs = game_kwargs
        self.ablate = game_kwargs['ablate']
        self.question = None
        self.player1 = player
        self.log = {}

    def set_param(self, r_kwargs):
        for k, v in r_kwargs.items():
            if k in self.game_kwargs:
                self.game_kwargs[k] = v
                if k == 'question':
                    self.question = v

    def play(self, max_attempts=20):
        self.player1.update(**self.game_kwargs)
        print("SYSTEM PROMPT")
        print(self.player1.sys_prompt)
        self.log['player-sys'] = self.player1.sys_prompt
        question_ans = [self.question[0], self.question[1]]
        if self.ablate:
            random.shuffle(question_ans)
        player_prompt = self.write_player_prompt(question_ans)
        for attempt in range(1, max_attempts + 1):
            self.log['player-prompt'] = player_prompt
            print("USER PROMPT")
            print(player_prompt)
            player_res = self.player1.decide(player_prompt)
            self.log['player-res'] = player_res
            print("RESPONSE")
            print(player_res)
            ans = self.get_choice(player_prompt, player_res)
            if ans is not None:
                break
            elif ans is None and attempt == max_attempts:
                raise ValueError("Failed to obtain a valid answer")
        return self.log

    def write_player_prompt(self, question_ans):
        player_prompt = ("You can either choose:\n"
                         "A. %s\n"
                         "B. %s") % (question_ans[0], question_ans[1])
        return player_prompt

    def get_choice(self, prompt, text):
        # Define the regular expression pattern
        pattern = r'Answer:\s*(.+)'
        # Extract question choices from prompt
        first = prompt.split('\n')[1]
        second = prompt.split('\n')[2]
        # Search for the pattern in the text
        match = re.search(pattern, text)
        options = [first, second, first.replace('A. ', ''), second.replace('B. ', '')]
        if match:
            # Extract the expression after "Answer:"
            ans = match.group(1).strip()
            valid = False
            for o in options:
                if ans.startswith(o):
                    valid = True
            if not valid:
                ans = None
        else:
            ans = None
        return ans

    def save(self, file_name):
        with open(file_name, 'w') as f:
            json.dump(self.log, f)
        return
