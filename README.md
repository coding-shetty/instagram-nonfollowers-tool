# Instagram Non-Followers Finder

A Python tool that finds Instagram accounts you follow that don't follow you back.

## Features

- Fetches your followers list
- Fetches your following list
- Compares both lists
- Displays (and counts) accounts that are not following you back

## Read-only: no actions are taken

This script only **reads** your followers/following lists and prints a report.
It never follows, unfollows, blocks, or posts anything, and it has no option
to take any action on your account. There is nothing to "dry-run" — the
report *is* the whole output.

## Disclaimer

- This project is **not affiliated with, endorsed by, or sponsored by
  Instagram or Meta**. Instagram is a trademark of Meta Platforms, Inc.
- This tool talks to Instagram through [Instaloader](https://instaloader.github.io/),
  an **unofficial** client that scrapes Instagram's internal endpoints. Using
  such endpoints may violate Instagram's
  [Terms of Use](https://help.instagram.com/519522125107875) and can lead to
  temporary rate limits or a temporary lock on your account. **Use at your own
  risk** — consider using an account you don't mind getting locked.
- Your login session gives full access to your account. Keep it private
  (see [Authentication](#authentication-one-time)).

## Requirements

- Python 3.9+
- [Instaloader](https://pypi.org/project/instaloader/) (pinned in `requirements.txt`)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # pinned dependencies
```

Installing `instaloader` also provides the `instaloader` CLI, which is used for
the one-time login.

## Authentication (one-time)

This tool authenticates using an
[Instaloader](https://instaloader.github.io/) login session. Log in once from
a terminal:

```bash
instaloader --login YOUR_USERNAME
```

Enter your password when prompted (and the 2FA code if your account uses
two-factor authentication). The session is saved to a local file:

- Linux/macOS: `~/.config/instaloader/session-YOUR_USERNAME`
- Windows: `%LOCALAPPDATA%\Instaloader\session-YOUR_USERNAME`

The script finds this file automatically. **Never commit the session file** —
it lets anyone act as you on Instagram. Re-run `instaloader --login` whenever
the session expires or Instagram rejects it.

> ⚠️ Because login goes through unofficial endpoints, Instagram may
> temporarily lock your account after repeated or aggressive use.

## Usage

```bash
python3 insta_not_following.py
```

1. Enter your Instagram username (the one you logged in with; a leading `@`
   is fine and gets stripped).
2. The script fetches both follower lists. This can take a while for large
   accounts — Instaloader deliberately sleeps between requests.
3. It prints every account that doesn't follow you back, one per line.

### Example output

```
Enter your Instagram username: myaccount
Fetching followers...
  Fetched 1234 followers.
Fetching following...
  Fetched 2345 accounts you follow.

Accounts not following you back:

some_user_a
some_user_b
ghost_account

Total: 3 accounts
```

To keep the list for later, redirect the output to a file:

```bash
python3 insta_not_following.py > nonfollowers.txt
```

## Error handling & troubleshooting

The script exits with a non-zero status and a message when something goes
wrong. Common cases:

| Message | Cause | Fix |
| --- | --- | --- |
| `Login session for '...' not found` | You haven't logged in yet | Run `instaloader --login YOUR_USERNAME` once |
| `Login session ... is missing or expired` | Saved session is stale | Log in again |
| `Instagram rejected the stored login session` | Bad credentials, or Instagram invalidated the session | Log in again |
| `Login session file for '...' is corrupted (...)` | Session file is damaged or was written by a different version of instaloader | Log in again |
| `Two-factor authentication is required` | Your account uses 2FA | Log in again and complete the 2FA prompt |
| `Instagram rate limit hit (too many requests)` | Too many requests in a short time | Wait 30–60 minutes; don't run the script in a loop |
| `Profile '...' does not exist or is not public` | Username typo (or account is private) | Check the username |
| `Network error while fetching follower lists` | Internet / proxy / DNS problem | Check your connection and retry |

Instaloader also retries transient connection errors on its own (a few times,
with a delay), so occasional network blips usually recover by themselves.

## Notes

- The tool works on **your own** account: you must log in as yourself, because
  it reads your followers/following lists.
- For accounts with very large followings, fetching can take several minutes.
  That is expected — Instaloader spaces out requests on purpose to reduce
  rate-limit risk.

## License

MIT — see [LICENSE](LICENSE).
