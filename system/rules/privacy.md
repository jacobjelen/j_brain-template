# Privacy

Keep your own brain repo private: it holds personal data. Treat it as sensitive.

## Never store
- Passwords, API keys, tokens, recovery codes
- Card numbers, bank account numbers, IBANs, crypto seed phrases
- Government IDs: passport, ID card or birth numbers
- Other people's secrets told to John in confidence, if marked as such

If an inbox item contains any of these, the digest **redacts** them in the `raw/` copy (`[REDACTED: card number]`) before committing, and logs `REDACTED`.

## Store carefully
- **Health:** factual and useful only (conditions, allergies, medication, doctors, goals). No speculation.
- **Other people:** what's relevant to John's relationship with them and to helping him. No gossip.

## Sharing
Agents never send brain content to third-party services (web APIs, forms, other people) unless John asks for that specific action.
