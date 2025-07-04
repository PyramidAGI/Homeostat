import random
import time

class Homeostat:
    def __init__(self, setpoint_sickness_per_month):
        self.setpoint = setpoint_sickness_per_month
        self.current_sickness_rate = random.uniform(0.5, 2.0)  # initial random rate
        self.adjustment_factor = 0.1  # how aggressively we adjust per iteration

    def measure(self):
        # Simulate measurement (could be from data in real life)
        fluctuation = random.uniform(-0.1, 0.1)
        self.current_sickness_rate += fluctuation
        # Avoid negative rates
        if self.current_sickness_rate < 0:
            self.current_sickness_rate = 0

    def adjust(self):
        # Adjust toward setpoint
        if self.current_sickness_rate > self.setpoint:
            self.current_sickness_rate -= self.adjustment_factor
            action = "Reducing workload or increasing rest"
        else:
            action = "Maintaining current settings"
        return action

    def status(self):
        return f"Sickness rate: {self.current_sickness_rate:.2f} per month (setpoint: {self.setpoint})"

def main():
    # Plan from your prompt
    what_to_arrange = "sick leave"
    guardrails = ["less than 1 sickness per month", "health metrics: less than 1 sickness per month"]
    observer = "team lead"
    
    print("Plan:")
    print(f"  What to arrange: {what_to_arrange}")
    print(f"  Guardrails: {', '.join(guardrails)}")
    print(f"  Observer: {observer}")
    print("\nStarting homeostat control loop...\n")

    # Use setpoint from guardrail
    setpoint_value = 1.0

    homeostat = Homeostat(setpoint_sickness_per_month=setpoint_value)

    # Simulate control loop
    for step in range(20):
        homeostat.measure()
        action = homeostat.adjust()
        print(f"Step {step+1}: {homeostat.status()} | Action: {action}")
        time.sleep(0.2)  # Pause to simulate time passing

    print("\nTarget sickness rate reached or maintained.")

if __name__ == "__main__":
    main()
