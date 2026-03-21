---
name: send-email-smtp
description: Send outbound email from this Raspberry Pi using Gmail SMTP through msmtp/mailutils. Use when the user wants to send an email, test outbound mail delivery, verify SMTP setup, or troubleshoot simple email sending on this machine. Not for Gmail inbox watching/webhooks/PubSub; that uses gog + gcloud instead.
---

# Send Email via Gmail SMTP

Use the local `msmtp` setup for outbound email on this machine.

## Local assumptions

- SMTP relay is Gmail via `smtp.gmail.com:587`
- Sender account is `jjfwangbot@gmail.com`
- `msmtp`, `msmtp-mta`, and `mailutils` are installed
- User-level config lives at `~/.config/msmtp/config`
- App password file lives at `~/.config/msmtp/gmail-app-password`

## Preferred workflow

1. Confirm `msmtp` exists.
2. If needed, inspect `~/.config/msmtp/config` and `~/.msmtp.log`.
3. Send mail with `msmtp` directly unless the user specifically wants `mail`.
4. For tests, send a minimal plain-text message first.
5. If delivery fails, check `~/.msmtp.log` before guessing.

## Commands

### Verify installation

```bash
command -v msmtp
msmtp --version
```

### Verify Gmail reachability/TLS

```bash
msmtp --serverinfo --tls --host=smtp.gmail.com --port=587
```

### Send a simple message

```bash
printf "Subject: Test subject\n\nHello from Raspberry Pi.\n" | msmtp recipient@example.com
```

### Send with explicit From header

```bash
printf "From: jjfwangbot@gmail.com\nTo: recipient@example.com\nSubject: Test subject\n\nHello from Raspberry Pi.\n" | msmtp recipient@example.com
```

### Check logs

```bash
cat ~/.msmtp.log
```

## Troubleshooting

- `authentication failed`: app password wrong, revoked, or account email mismatch
- TLS/certificate problems: verify `/etc/ssl/certs/ca-certificates.crt` exists
- mail sent but not received: check spam and Gmail sent mail, then inspect log
- `msmtp: account default not found`: config file missing or malformed

## Boundaries

- Do not claim OpenClaw has a generic built-in SMTP sender config unless verified.
- For inbox watching or Gmail-triggered hooks, switch to the Gmail Pub/Sub flow (`openclaw webhooks gmail setup`) instead of this skill.
