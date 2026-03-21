# Pi local SMTP setup

Known working setup on this Raspberry Pi:

- Gmail sender: `jjfwangbot@gmail.com`
- Transport: Gmail SMTP over STARTTLS
- Host: `smtp.gmail.com`
- Port: `587`
- Tooling: `msmtp`, `msmtp-mta`, `mailutils`

Expected user config files:

- `~/.config/msmtp/config`
- `~/.config/msmtp/gmail-app-password`

Recommended config shape:

```conf
defaults
auth on
tls on
tls_starttls on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile ~/.msmtp.log

account gmail
host smtp.gmail.com
port 587
from jjfwangbot@gmail.com
user jjfwangbot@gmail.com
passwordeval "cat ~/.config/msmtp/gmail-app-password"

account default : gmail
```

Useful test command:

```bash
printf "Subject: SMTP test\n\nHello from Raspberry Pi via Gmail SMTP.\n" | msmtp recipient@example.com
```
