import random
import time

# List of possible metrics to map user goals to
METRICS = [
    "cost", "error rates", "hunger", "productivity", "health metrics",
    "climate metrics", "profit", "sales", "exam results", "success",
    "visits", "yields", "stocks", "likes", "income", "pleasure/pain",
    "economic indicators", "accuracy", "power", "distance", "speed",
    "efficiency", "energy consumption"
]

def map_goal_to_metric(goal):
    """Map the user's goal to a relevant metric from the list."""
    goal = goal.lower()
    for metric in METRICS:
        if metric in goal or any(word in goal for word in metric.split()):
            return metric
    # Fallback to a default metric if no clear match
    return "success"

def get_user_inputs():
    """Collect user inputs for the homeostat-like system."""
    print("Welcome to the Homeostat-like System!")
    arrangement = input("What do you want to arrange? ")
    goal = input("What is the goal/target? ")
    observer = input("Who is the observer? ")
    actors = input("Who are the actors? ")
    guardrails = input("What are the guardrails? ")
    first_principle = input("What is the first principle/driver/summary? ")
    trigger = input("What is the trigger? ")
    history = input("What is the history of the input data? (optional) ") or "No history provided"
    dod = input("What is the Definition of Done (DoD)? (optional) ") or "Goal achieved"
    
    return {
        "arrangement": arrangement,
        "goal": goal,
        "observer": observer,
        "actors": actors,
        "guardrails": guardrails,
        "first_principle": first_principle,
        "trigger": trigger,
        "history": history,
        "dod": dod
    }

def simulate_feedback_loop(inputs, metric):
    """Simulate a homeostat-like feedback loop to steer toward the goal."""
    print("\nInitiating Homeostat-like Control System...")
    print(f"Mapped goal '{inputs['goal']}' to metric: {metric}")
    print(f"Observer: {inputs['observer']}")
    print(f"Actors: {inputs['actors']}")
    print(f"Guardrails: {inputs['guardrails']}")
    print(f"Driver: {inputs['first_principle']}")
    print(f"Trigger: {inputs['trigger']}")
    print(f"Definition of Done: {inputs['dod']}\n")

    # Simulate current state (randomized for demo purposes)
    current_state = random.uniform(0, 100)
    target_state = 100  # Arbitrary target for "optimal" state
    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        print(f"Iteration {iteration + 1}:")
        print(f"Current {metric} level: {current_state:.2f} (Target: {target_state})")
        
        # Check if trigger condition is met
        if inputs["trigger"].lower() in ["start", "begin", "now"] or iteration == 0:
            error = target_state - current_state
            if abs(error) < 5:  # Close enough to target
                print(f"Success: {metric} is within acceptable range!")
                print(f"Definition of Done met: {inputs['dod']}")
                break
            
            # Adjust based on error and first principle
            adjustment = error * 0.3  # Simple proportional control
            if "minimize" in inputs["first_principle"].lower() and "cost" in metric:
                adjustment *= -1  # Reverse for cost minimization
            elif "maximize" in inputs["first_principle"].lower():
                adjustment *= 1.2  # Amplify for maximization goals
            
            # Respect guardrails (e.g., prevent negative values or extreme adjustments)
            if "no negative" in inputs["guardrails"].lower() and current_state + adjustment < 0:
                adjustment = -current_state
            current_state += adjustment
            
            print(f"Actors ({inputs['actors']}) adjust based on {inputs['first_principle']}: {adjustment:+.2f}")
        else:
            print(f"Trigger '{inputs['trigger']}' not met. Waiting...")
            break
        
        iteration += 1
        time.sleep(1)  # Simulate processing time
        
        if iteration == max_iterations:
            print("Max iterations reached. System stabilizing.")
            print(f"Final {metric} level: {current_state:.2f}")

def main():
    # Get user inputs
    inputs = get_user_inputs()
    
    # Map goal to a metric
    metric = map_goal_to_metric(inputs["goal"])
    
    # Run the feedback loop
    simulate_feedback_loop(inputs, metric)

if __name__ == "__main__":
    main()