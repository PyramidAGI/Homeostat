import random
import re

class Homeostat:
    def __init__(self, initial_state, setpoint, rules, max_iterations=100, perturbation_chance=0.2):
        """
        Initialize the homeostat.
        - initial_state: dict of variable names to their starting values (e.g., {'temperature': 10}).
        - setpoint: dict of variable names to target values (e.g., {'temperature': 5}).
        - rules: list of English sentence-rules as strings.
        - max_iterations: Max steps to prevent infinite loops.
        - perturbation_chance: Probability (0-1) of random perturbation per step.
        """
        self.state = initial_state.copy()
        self.setpoint = setpoint
        self.rules = rules
        self.max_iterations = max_iterations
        self.perturbation_chance = perturbation_chance
        self.history = []  # Track state changes

    def parse_rule(self, rule):
        """
        Parse a rule string into components.
        Returns: (variable, comparison, adjustment, amount) or None if invalid.
        """
        # Use regex to extract parts; assumes the format is followed
        match = re.match(r"If the (\w+) is (\w+ \w+|\w+) the setpoint, then (\w+) the (\w+) by (\d+).", rule)
        if match:
            var_condition = match.group(1)
            comparison = match.group(2)
            adjustment = match.group(3)
            var_action = match.group(4)
            amount = int(match.group(5))
            if var_condition != var_action:
                return None  # Variables must match for simplicity
            return var_condition, comparison, adjustment, amount
        return None

    def apply_perturbation(self):
        """Apply random noise to simulate disturbances."""
        for var in self.state:
            if random.random() < self.perturbation_chance:
                noise = random.uniform(-1, 1)  # Small random change
                self.state[var] += noise
                print(f"Perturbation applied to {var}: +{noise:.2f}")

    def run(self):
        """Run the homeostat loop until stable or max iterations."""
        iteration = 0
        while iteration < self.max_iterations:
            self.history.append(self.state.copy())
            stable = all(abs(self.state[var] - self.setpoint[var]) < 0.01 for var in self.state)  # Tolerance for floating-point
            if stable:
                print("System stabilized.")
                break

            self.apply_perturbation()

            applied = False
            for rule in self.rules:
                parsed = self.parse_rule(rule)
                if parsed:
                    var, comparison, adjustment, amount = parsed
                    if var not in self.state:
                        continue
                    current = self.state[var]
                    target = self.setpoint[var]

                    # Check condition
                    if (comparison == "above" and current > target) or \
                       (comparison == "below" and current < target) or \
                       (comparison == "equal to" and abs(current - target) < 0.01):
                        # Apply action
                        if adjustment == "decrease":
                            self.state[var] -= amount
                        elif adjustment == "increase":
                            self.state[var] += amount
                        elif adjustment == "maintain":
                            pass  # No change
                        print(f"Applied rule: {rule} | New {var}: {self.state[var]}")
                        applied = True
                        break  # Apply one rule per iteration for simplicity

            if not applied:
                print("No applicable rule found.")

            iteration += 1
            print(f"Iteration {iteration}: State = {self.state}")

        if iteration == self.max_iterations:
            print("Max iterations reached; system may not have stabilized.")
        return self.state, self.history

# Example usage
rules = [
    "If the temperature is above the setpoint, then decrease the temperature by 2.",
    "If the temperature is below the setpoint, then increase the temperature by 1.",
    "If the temperature is equal to the setpoint, then maintain the temperature by 0."
]

homeostat = Homeostat(initial_state={'temperature': 10.0}, setpoint={'temperature': 5.0}, rules=rules)
final_state, history = homeostat.run()

print("\nFinal state:", final_state)
print("History of states:", history)