# Vault changelog (personal)

After every vault write operation in this vault, append a line to `_os/log.md` at the vault root:

```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```

- Soul and personal content: include `requires_confirmation: true` context in the log line so a later read shows human gatekeeping happened.
- Wiki-level operations (e.g. promote): also append to `wiki/log.md`.
