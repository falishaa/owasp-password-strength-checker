# OWASP Password Strength Checker

A Python program to check a password's strength based on OWASP authentication guidelines. 

## Features

* <strong>Length Validator:</strong> OWASP recommends minimum 8 characters, preferably 12+
* <strong>Composition Check:</strong> Ensure presence of upper/lowercase letters, numbers, and symbols
* <strong>Blocklist Reference:</strong> Reject top common/breached passwords by querying the "Have I Been Pwned" passwords API using k-anonymity
* <strong>Discourage Abritrary Rules:</strong> Explicitly not enforcing arbitrary rules such as "must contain a special character" as a <em>hard</em> requirement, since OWASP actively discourages this
* <strong>Score Output:</strong> e.g., Weak, Moderate, Strong, Excellent, with feedback
