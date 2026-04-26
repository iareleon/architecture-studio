# Vault changelog (social-media)

After every vault write operation in this vault, append a line to `_os/log.md` at the vault root:

```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```

- Wiki-level operations (promote, calendar): also append to `wiki/log.md`.
