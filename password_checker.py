import re

def check_length(password: str) -> dict:
    """Evaluate password length per OWASP guidance (min 8, ideally 12+)."""
    length = len(password)
    if length < 8:
        return {"pass": False, "points:": 0, "note": "Below OWASP minimum of 8 characters"}
    elif length < 12:
        return {"pass": True, "points": 1, "note": "Meets minimum length, but 12+ characters recommended"}
    elif length < 16:
        return {"pass": True, "points": 2, "note": "Good length"}
    else:
        return {"pass": True, "points": 3, "note": "Excellent length"}

def check_composition(password: str) -> dict:
    """Score special characters as a bonus, not hard requirement."""
    checks = {
        "lowercase": bool(re.search(r"[a-z]", password)),
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "symbol": bool(re.search(r"[^\w\s]", password)),
    }
    points = sum(checks.values()) # 0-4
    return{"points": points, "details": checks}

def load_blocklist(filepath: str = "common_passwords.txt") -> set:
    """Load common passwords text file into a set for fast lookup."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        return set()

def check_blocklist(password: str, blocklist: set) -> dict:
    """Reject common passwords found from list."""
    is_common = password.lower() in blocklist
    return {
        "pass": not is_common,
        "note": "Found in common passwords list" if is_common else "Not in blocklist",
    }

def evaluate_password(password: str, blocklist: set) -> dict:
    """Combine all checks into total score and verdict."""
    length_result = check_length(password)
    comp_result = check_composition(password)
    block_result = check_blocklist(password, blocklist)

    # Auto fail conditions
    if not length_result["pass"]:
        return {"verdict": "Weak", "reason": length_result["note"], "score": 0}
    if not block_result["pass"]:
        return {"verdict": "Weak", "reason": length_result["note"], "score": 0}

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
        "length_note": length_result["note"],
        "composition": comp_result["details"],
    }

def main():
    blocklist = load_blocklist()
    password = input("Enter a password to evaluate: ")
    result = evaluate_password(password, blocklist)

    print(f"\nVerdict: {result['verdict']}")
    if "score" in result and result["verdict"] != "Weak":
        print(f"Score: {result['score']}/7")
        print(f"Length: {result['length_note']}")
        print(f"Character variety: {result['composition']}")
    elif "reason" in result:
        print(f"Reason: {result['reason']}")


if __name__ == "__main__":
    main()