"""Forward chaining and inheritance in a semantic network."""

from pathlib import Path
from time import perf_counter


def infer_facts(seed_facts, rule_book):
    known_facts = set(seed_facts)
    while True:
        fresh_facts = {conclusion for premises, conclusion in rule_book
                       if set(premises) <= known_facts} - known_facts
        if not fresh_facts:
            return known_facts
        known_facts.update(fresh_facts)


def inherits(child_name, parent_name, family_links):
    if child_name not in family_links or parent_name not in family_links:
        raise ValueError("Unknown concept.")
    pending_names, visited_names = [child_name], set()
    while pending_names:
        current_name = pending_names.pop()
        if current_name == parent_name:
            return True
        if current_name not in visited_names:
            visited_names.add(current_name)
            pending_names.extend(family_links.get(current_name, []))
    return False


def main():
    logic_clock = perf_counter()
    rule_book = [({"has_feathers"}, "bird"), ({"bird"}, "animal"),
                 ({"animal"}, "needs_food")]
    family_links = {"sparrow": ["bird"], "bird": ["animal"], "animal": []}
    logic_result = sorted(infer_facts({"has_feathers"}, rule_book))
    animal_link = inherits("sparrow", "animal", family_links)
    logic_note = (f"Facts: {logic_result}\n"
                  f"Sparrow is animal: {animal_link}\n"
                  f"Seconds: {perf_counter() - logic_clock:.6f}\n")
    try:
        logic_out = Path(__file__).resolve().parent / "outputs"
        logic_out.mkdir(exist_ok=True)
        (logic_out / "results.txt").write_text(logic_note)
        print(logic_note)
    except OSError as error:
        print(f"Cannot save results: {error}")


if __name__ == "__main__":
    main()
