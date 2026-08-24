import re

def load_blocklist(filepath: str = "common_passwords.txt") -> set:
    """Load common passwords text file into a set for fast lookup."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        return set()

def check_length(password: str) -> dict:
    """Evaluate password length per OWASP guidance (min 8, ideally 12+)."""
    length = len(password)
    if length < 8:
        return {"pass": False, "points:": 0, "error": "Password must be at least 8 characters long."}
    elif length < 12:
        return {"pass": True, "points": 1, "error": "Consider using 12 or more characters for stronger security."}
    elif length < 16:
        return {"pass": True, "points": 2, "error": None}
    else:
        return {"pass": True, "points": 3, "error": "None"}

def check_composition(password: str) -> dict:
    """Score special characters as a bonus, not hard requirement."""
    rules = {
        "lowercase": (r"[a-z]", "Password must contain at least one lowercase letter."),
        "uppercase": (r"[A-Z]", "Password must contain at least one uppercase letter."),
        "digit": (r"\d", "Password must contain at least one digit"),
        "symbol": (r"[^\w\s]", "Password must contain at least one special character."),
    }
    errors = []
    points = 0
    for pattern, message in rules.values():
        if re.search(pattern, password):
            points += 1
        else:
            errors.append(message)

    return{"points": points, "errors": errors}


def check_blocklist(password: str, blocklist: set) -> dict:
    """Reject common passwords found from list."""
    is_common = password.lower() in blocklist
    return {
        "pass": not is_common,
        "error": "Password is too common." if is_common else None,
    }

def evaluate_password(password: str, blocklist: set) -> dict:
    """Combine all checks into total score, verdict, and list of errors."""
    length_result = check_length(password)
    comp_result = check_composition(password)
    block_result = check_blocklist(password, blocklist)

    errors = []
    if length_result["error"]:
        errors.append(length_result["error"])
    errors.extend(comp_result["errors"])
    if block_result["error"]:
        errors.append(block_result["error"])

    # Auto fail conditions: below min length or found in blocklist
    if not length_result["pass"] or not block_result["pass"]:
        return {"verdict": "Weak", "score": 0, "errors": errors}

    total_points = length_result["points"] + comp_result["points"] # max 7

    if total_points <= 2:
        verdict = "Weak"
    elif total_points <= 4:
        verdict = "Moderate"
    elif total_points <= 6:
        verdict = "Strong"
    else:
        verdict = "Excellent"

    return {
        "verdict": verdict,
        "score": total_points,
        "errors": errors
    }

def print_result(password: str, result: dict) -> None:
    """Print a readable summary of password evaluation."""
    print(f"\nVerdict: {result['verdict']}")
    print(f"Score: {result['score']}/7")
    if result["errors"]:
        print("Errors:")
        for error in result["errors"]:
            print(f" - {error}")

def main():
    blocklist = load_blocklist()
    password = input("Enter a password to evaluate: ")
    result = evaluate_password(password, blocklist)
    print_result(password, result)

if __name__ == "__main__":
    while True:
        main()