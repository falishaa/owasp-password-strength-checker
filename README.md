# OWASP Password Strength Checker

A Python program to evaluate a password's strength based on OWASP authentication guidelines. Stylized with a retro Windows 95 theme.

## Gallery
<img width="950" height="434" alt="password-strength-gallery1" src="https://github.com/user-attachments/assets/eebf7a9e-8ad7-4c74-9c57-71b41a117689" />
<img width="950" height="434" alt="password-strength-gallery2" src="https://github.com/user-attachments/assets/dbfafc9a-dcb6-4060-b4d6-57cf00892d2c" />


## Features

* <strong>Length Validator:</strong> OWASP recommends minimum 8 characters, preferably 12+
* <strong>Composition Check:</strong> Ensure presence of upper/lowercase letters, numbers, and symbols
* <strong>Blocklist Reference:</strong> Reject top common/breached passwords by querying the "Have I Been Pwned" passwords API using k-anonymity
* <strong>Discourage Abritrary Rules:</strong> Explicitly not enforcing arbitrary rules such as "must contain a special character" as a <em>hard</em> requirement, since OWASP actively discourages this
* <strong>Score Output:</strong> e.g., Weak, Moderate, Strong, Excellent, with feedback

This tool implements OWASP guidance directly, and is meant to demonstrate translating a security standard into working software. This program bridges my defensive cybersecurity background with software engeering practice.

## How It Works

Each password is evaluated on three checks:

1. <strong>Length</strong> - scored on a scale, with 8 characters as an OWASP-recommended minimum and 12+ preferred
2. <strong>Composition</strong> - presence of lowercase, uppercase, digits, and symbols is scored as a <strong>bonus</strong>, not a hard requirement
3. <strong>Blocklist</strong> - checked against a list of common passwords, a match is an automatic fail regardless of score

Length and composition points combine into a score out of 7, mapped to a verdict:

| Score | Verdict |
|-------|---------|
| 0–2   | Weak |
| 3–4   | Moderate |
| 5–6   | Strong |
| 7     | Excellent |

A password that is too short or found in the blocklist is always scored <strong>weak</strong>, even if it would otherwise score higher. Length and blocklist status are treated as OWASP-mandated requirements, not just factors to check.

This tool provides the verdict, score, and a list of specific, actionable errors (e.g. `Password must contain at least one uppercase letter.`) instead of a raw dump of pass/fail flags.

## Setup

```bash
# Clone the repo
git clone https://github.com/falishaa/owasp-password-strength-checker.git
cd owasp-password-strength-checker

# (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

## Usage

```bash
python password_checker.py
```

You will be prompted to enter a password, then shown its verdict, score, and any issues found:

```
Enter a password to evaluate: password1

Verdict: Weak
Score: 0/7
Issues:
- Consider using 12 or more characters for stronger security.
- Password must contain at least one uppercase letter.
- Password must contain at least one special character.
- Password is too common.
```

## Design Decisions

- <strong>Blocklist match always overrides score.</strong> A breached password is dangerous regardless of length or character variety, so it's checked as a hard gate rather than folded into the point total.
- <strong>Composition is a bonus, not a requirement.</strong> This directly follows OWASP's stance against forced complexity rules, which research shows push users toward predictable patterns (e.g. `Password1!`) rather than genuinely stronger passwords.
- <strong>Errors are specific and actionable.</strong> Rather than providing raw pass/fail flags, the tool tells the user exactly what to fix.

## Author

Built by Falisha as a portfolio project blending a cybersecurity background with software engineering practice.
