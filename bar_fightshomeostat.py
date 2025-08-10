'''
Bar Fight Homeostat Simulation by Grok4
This code simulates a homeostat for managing bar fights, using rules to control aggression levels.
'''
import random
import re

class BarHomeostat:
    def __init__(self, initial_state, setpoint, rules, max_iterations=100, perturbation_chance=0.3):
        """
        Initialize the bar homeostat.
        - initial_state: dict e.g., {'aggression level': 8}.
        - setpoint: dict e.g., {'aggression level': 0}.
        - rules: list of sentence-rules.
        - max_iterations: Max steps.
        - perturbation_chance: Chance of random aggression spike (e.g., rowdy patron).
        """
        self.state = initial_state.copy()
        self.setpoint = setpoint
        self.rules = rules
        self.max_iterations = max_iterations
        self.perturbation_chance = perturbation_chance
        self.history = []

    def parse_rule(self, rule):
        """
        Parse the extended rule.
        Returns: (variable, comparison, adjustment, amount, bar_action) or None.
        """
        match = re.match(r"If the ([\w\s]+) is (\w+ \w+|\w+) the setpoint, then (\w+) the ([\w\s]+) by (\d+) using ([\w\s]+).", rule)
        if match:
            var_condition = match.group(1)
            comparison = match.group(2)
            adjustment = match.group(3)
            var_action = match.group(4)
            amount = int(match.group(5))
            bar_action = match.group(6).strip('.')
            if var_condition != var_action:
                return None
            return var_condition, comparison, adjustment, amount, bar_action
        return None

    def apply_perturbation(self):
        """Simulate bar disturbances (e.g., argument starts)."""
        for var in self.state:
            if random.random() < self.perturbation_chance:
                noise = random.uniform(0, 2)  # Positive noise to simulate increasing tension
                self.state[var] += noise
                print(f"Disturbance: Aggression spiked by {noise:.2f} (rowdy patrons).")

    def run(self):
        """Run the loop to control fights."""
        iteration = 0
        while iteration < self.max_iterations:
            self.history.append(self.state.copy())
            stable = all(abs(self.state[var] - self.setpoint[var]) < 0.01 for var in self.state)
            if stable:
                print("Bar is peaceful and stabilized.")
                break

            self.apply_perturbation()

            applied = False
            for rule in self.rules:
                parsed = self.parse_rule(rule)
                if parsed:
                    var, comparison, adjustment, amount, bar_action = parsed
                    if var not in self.state:
                        continue
                    current = self.state[var]
                    target = self.setpoint[var]

                    if (comparison == "above" and current > target) or \
                       (comparison == "below" and current < target) or \
                       (comparison == "equal to" and abs(current - target) < 0.01):
                        if adjustment == "decrease":
                            self.state[var] -= amount
                        elif adjustment == "increase":
                            self.state[var] += amount
                        elif adjustment == "maintain":
                            pass
                        # Ensure non-negative aggression
                        self.state[var] = max(0, self.state[var])
                        print(f"Applied rule: {rule} | Action: {bar_action} | New {var}: {self.state[var]}")
                        applied = True
                        break

            if not applied:
                print("No applicable rule found; bar tension unmanaged.")

            iteration += 1
            print(f"Iteration {iteration}: State = {self.state}")

        if iteration == self.max_iterations:
            print("Max iterations reached; fights may persist.")
        return self.state, self.history

# Example usage with bar-themed rules
rules = [
    "If the aggression level is above the setpoint, then decrease the aggression level by 2 using calming music.",
    "If the aggression level is below the setpoint, then increase the aggression level by 1 using upbeat tunes.",  # Optional; could remove if only decreasing makes sense
    "If the aggression level is equal to the setpoint, then maintain the aggression level by 0 using standard service."
]

bar_homeostat = BarHomeostat(initial_state={'aggression level': 8.0}, setpoint={'aggression level': 0.0}, rules=rules)
final_state, history = bar_homeostat.run()

print("\nFinal state:", final_state)
print("History of states:", history)