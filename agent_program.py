"""
agent_program.py

This script implements a simple command‑line program exposing four modules:

1. MapReduce (MapReduceWordCount):
   A demonstration of the MapReduce paradigm for counting word frequencies in
   a given input string. The `map` function tokenizes the input into words
   and emits (word, 1) pairs. The `reduce` function aggregates these pairs
   into a frequency dictionary. The `process` method orchestrates the
   workflow by mapping and reducing a given text.

2. LkpAdd (LookupTable):
   A basic lookup table implementation that allows you to add key‑value
   pairs, retrieve values by key, and list all current entries. It uses
   a Python dictionary internally.

3. Homeostat:
   A simple homeostatic controller that converges a value toward a target
   (setpoint) using proportional adjustment. Each iteration moves the
   current value a fixed fraction of the difference between the current
   value and the setpoint. The `converge` method performs repeated
   updates until the value is within a specified tolerance of the
   setpoint or a maximum number of iterations has been reached.

4. PromptBook:
   An in‑memory database of prompts identified by unique names. It can add
   new prompts, retrieve prompts, list available prompts, and optionally
   save to or load from a JSON file on disk.

To run the program, execute this file with Python. You will be presented
with a menu to choose which module to use. Follow the on‑screen prompts
for input and observe the corresponding output.
"""

import json
import os
from collections import Counter
from typing import Dict, List, Tuple, Optional


class MapReduceWordCount:
    """Simple MapReduce‑style word count implementation."""

    @staticmethod
    def map(text: str) -> List[Tuple[str, int]]:
        """Map step: tokenize text and emit (word, 1) pairs.

        Args:
            text: The input string to analyze.

        Returns:
            A list of (word, 1) tuples for each tokenized word.
        """
        # Split on whitespace and remove punctuation from ends of words
        tokens = text.strip().split()
        pairs = []
        for token in tokens:
            # Normalize to lowercase and strip punctuation characters from both ends
            word = token.lower().strip("\"'.,!?;:-()[]{}")
            if word:
                pairs.append((word, 1))
        return pairs

    @staticmethod
    def reduce(mapped_pairs: List[Tuple[str, int]]) -> Dict[str, int]:
        """Reduce step: aggregate counts for each word.

        Args:
            mapped_pairs: A list of (word, count) tuples.

        Returns:
            A dictionary mapping words to their aggregated counts.
        """
        counts = Counter()
        for word, count in mapped_pairs:
            counts[word] += count
        return dict(counts)

    def process(self, text: str) -> Dict[str, int]:
        """Perform map and reduce on the input text to count word frequencies.

        Args:
            text: The input string to analyze.

        Returns:
            A dictionary of word frequencies.
        """
        mapped = self.map(text)
        reduced = self.reduce(mapped)
        return reduced


class LookupTable:
    """A simple in‑memory lookup table for storing key‑value pairs."""

    def __init__(self) -> None:
        self.table: Dict[str, str] = {}

    def add(self, key: str, value: str) -> None:
        """Add or update a key‑value pair in the table."""
        self.table[key] = value

    def get(self, key: str) -> Optional[str]:
        """Retrieve a value by key.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key, or None if not found.
        """
        return self.table.get(key)

    def list_all(self) -> Dict[str, str]:
        """Return the entire lookup table as a dictionary."""
        return dict(self.table)


class Homeostat:
    """A simple controller that drives a value toward a setpoint using feedback."""

    def __init__(self, setpoint: float, step: float = 0.1) -> None:
        """Initialize the Homeostat.

        Args:
            setpoint: The target value to converge toward.
            step: The fraction of the error added to the current value each iteration.
                   A smaller step yields slower but smoother convergence. Must be
                   between 0 and 1 for stability.
        """
        if not 0 < step <= 1:
            raise ValueError("step must be in the interval (0, 1]")
        self.setpoint = setpoint
        self.step = step
        self.current: Optional[float] = None

    def initialize(self, initial_value: float) -> None:
        """Set the initial value from which to start the convergence process."""
        self.current = initial_value

    def iterate(self) -> float:
        """Perform one iteration of convergence.

        Returns:
            The updated current value after one iteration.
        """
        if self.current is None:
            raise RuntimeError("Homeostat must be initialized with an initial value before iterating")
        # Compute error and apply proportional adjustment
        error = self.setpoint - self.current
        self.current += self.step * error
        return self.current

    def converge(self, tolerance: float = 1e-3, max_iterations: int = 1000) -> List[float]:
        """Iterate until the value is within tolerance of the setpoint or
        until max_iterations have been performed. Returns a list of values
        generated during the convergence process.

        Args:
            tolerance: The acceptable absolute difference between the current value and the setpoint.
            max_iterations: The maximum number of iterations to perform.

        Returns:
            A list of the successive values produced during the convergence.
        """
        if self.current is None:
            raise RuntimeError("Homeostat must be initialized before convergence")
        history = []
        for _ in range(max_iterations):
            value = self.iterate()
            history.append(value)
            if abs(self.setpoint - value) <= tolerance:
                break
        return history


class PromptBook:
    """A collection of named prompts that can be stored in memory and optionally persisted."""

    def __init__(self) -> None:
        self.prompts: Dict[str, str] = {}

    def add_prompt(self, name: str, text: str) -> None:
        """Add or replace a prompt with the given name."""
        self.prompts[name] = text

    def get_prompt(self, name: str) -> Optional[str]:
        """Retrieve a prompt by name, or return None if it doesn't exist."""
        return self.prompts.get(name)

    def list_prompts(self) -> List[str]:
        """Return a list of available prompt names."""
        return list(self.prompts.keys())

    def save(self, filepath: str) -> None:
        """Persist the prompt collection to a JSON file."""
        with open(filepath, 'w', encoding='utf‑8') as f:
            json.dump(self.prompts, f, indent=2)

    def load(self, filepath: str) -> None:
        """Load prompts from a JSON file, replacing any existing ones."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The file '{filepath}' does not exist.")
        with open(filepath, 'r', encoding='utf‑8') as f:
            self.prompts = json.load(f)


# Command‑line interface

def main() -> None:
    """Top‑level function that provides a menu for users to interact with the modules."""
    lookup_table = LookupTable()
    prompt_book = PromptBook()

    print("Welcome to the Agent Modules Program!\n")
    while True:
        print("Please choose an option:")
        print("1) MapReduce Word Count")
        print("2) Lookup Table (LkpAdd)")
        print("3) Homeostat")
        print("4) PromptBook")
        print("q) Quit")
        choice = input("Enter your choice: ").strip().lower()

        if choice in ('q', 'quit', 'exit'):
            print("Exiting. Goodbye!")
            break
        elif choice == '1':
            text = input("Enter text to analyze: ")
            mr = MapReduceWordCount()
            counts = mr.process(text)
            print("\nWord counts:")
            for word, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
                print(f"{word}: {count}")
            print()
        elif choice == '2':
            print("\nLookup Table Options:")
            print("  a) Add or update a key‑value pair")
            print("  g) Get a value by key")
            print("  l) List all entries")
            subchoice = input("Choose an action: ").strip().lower()
            if subchoice == 'a':
                key = input("Enter key: ")
                value = input("Enter value: ")
                lookup_table.add(key, value)
                print(f"Added/Updated key '{key}'.\n")
            elif subchoice == 'g':
                key = input("Enter key to retrieve: ")
                value = lookup_table.get(key)
                if value is not None:
                    print(f"Value for '{key}': {value}\n")
                else:
                    print(f"Key '{key}' not found.\n")
            elif subchoice == 'l':
                table = lookup_table.list_all()
                if table:
                    print("\nLookup Table Contents:")
                    for k, v in table.items():
                        print(f"{k}: {v}")
                else:
                    print("Lookup table is empty.")
                print()
            else:
                print("Invalid option.\n")
        elif choice == '3':
            try:
                setpoint = float(input("Enter the target value (setpoint): "))
                initial = float(input("Enter the initial value: "))
                step_str = input("Enter the adjustment step (0 < step ≤ 1) [default 0.1]: ").strip()
                step = float(step_str) if step_str else 0.1
                tolerance_str = input("Enter the tolerance for convergence [default 0.001]: ").strip()
                tolerance = float(tolerance_str) if tolerance_str else 0.001
            except ValueError:
                print("Invalid numerical input. Please try again.\n")
                continue
            try:
                homeostat = Homeostat(setpoint=setpoint, step=step)
                homeostat.initialize(initial)
                history = homeostat.converge(tolerance=tolerance)
                print("\nConvergence history:")
                for i, value in enumerate(history, start=1):
                    print(f"Iteration {i}: {value}")
                print(f"Final value: {history[-1] if history else initial}\n")
            except Exception as e:
                print(f"Error: {e}\n")
        elif choice == '4':
            print("\nPromptBook Options:")
            print("  a) Add or update a prompt")
            print("  g) Get a prompt by name")
            print("  l) List prompt names")
            print("  s) Save prompts to a file")
            print("  r) Load prompts from a file")
            subchoice = input("Choose an action: ").strip().lower()
            if subchoice == 'a':
                name = input("Enter prompt name: ")
                text = input("Enter prompt text: ")
                prompt_book.add_prompt(name, text)
                print(f"Added/Updated prompt '{name}'.\n")
            elif subchoice == 'g':
                name = input("Enter prompt name to retrieve: ")
                prompt = prompt_book.get_prompt(name)
                if prompt is not None:
                    print(f"Prompt '{name}': {prompt}\n")
                else:
                    print(f"Prompt '{name}' not found.\n")
            elif subchoice == 'l':
                names = prompt_book.list_prompts()
                if names:
                    print("\nAvailable prompts:")
                    for n in names:
                        print(n)
                else:
                    print("No prompts available.")
                print()
            elif subchoice == 's':
                filepath = input("Enter the file path to save prompts: ")
                try:
                    prompt_book.save(filepath)
                    print(f"Prompts saved to '{filepath}'.\n")
                except Exception as e:
                    print(f"Error saving prompts: {e}\n")
            elif subchoice == 'r':
                filepath = input("Enter the file path to load prompts from: ")
                try:
                    prompt_book.load(filepath)
                    print(f"Prompts loaded from '{filepath}'.\n")
                except Exception as e:
                    print(f"Error loading prompts: {e}\n")
            else:
                print("Invalid option.\n")
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == '__main__':
    main()
