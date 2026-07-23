# Consent verification workflow

The API never attempts to recognize or authenticate handwriting. The signed form is stored as a protected member document, and an authorized person reviews it visually.

## Webpage states

Each signed section uses one of these values:

- `pending_review`: no human decision yet
- `verified`: the expected signature is visibly present
- `missing`: an expected signature is absent
- `unclear`: the scan cannot be assessed confidently

Changing a section from `pending_review` requires the reviewer name in the same request. The API records the review timestamp. Returning a section to `pending_review` clears its reviewer and timestamp.

The page should display the linked source document beside:

- printed signer name, place, and date
- signer role (`member` or `guardian`)
- signature status
- reviewer and review time
- whether the 14-17-year-old member co-signed the photo/video section

The reviewer confirms only that a signature is present in the expected location. This is not forensic or biometric verification.

## Withdrawal

Changing a granted consent or newsletter opt-in from `true` to `false` records a withdrawal timestamp. Changing it back to `true` clears that timestamp. An immutable consent-event history should be added before production withdrawal processing.
