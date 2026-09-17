"""Find Instagram accounts you follow that don't follow you back.

Read-only: this script only reads your followers/following lists and
prints a report. It never follows, unfollows, or changes anything.
"""

import pickle
import sys

import instaloader
from instaloader import (
    BadCredentialsException,
    ConnectionException,
    InstaloaderException,
    LoginRequiredException,
    Profile,
    ProfileNotExistsException,
    TooManyRequestsException,
    TwoFactorAuthRequiredException,
)


def fetch_lists(L, username):
    """Return (followers, following) username sets for the given profile."""
    profile = Profile.from_username(L.context, username)

    print("Fetching followers...")
    followers = {f.username for f in profile.get_followers()}
    print(f"  Fetched {len(followers)} followers.")

    print("Fetching following...")
    following = {f.username for f in profile.get_followees()}
    print(f"  Fetched {len(following)} accounts you follow.")

    return followers, following


def get_not_following_back(username):
    L = instaloader.Instaloader()

    try:
        L.load_session_from_file(username)
    except FileNotFoundError:
        sys.exit(
            f"Login session for '{username}' not found.\n"
            f"Log in once first:  instaloader --login {username}"
        )
    except (pickle.UnpicklingError, EOFError, KeyError, UnicodeDecodeError) as err:
        sys.exit(
            f"Login session file for '{username}' is corrupted "
            f"({err.__class__.__name__}).\n"
            f"Log in again:  instaloader --login {username}"
        )

    try:
        followers, following = fetch_lists(L, username)
    except LoginRequiredException:
        sys.exit(
            f"Login session for '{username}' is missing or expired.\n"
            f"Log in again:  instaloader --login {username}"
        )
    except BadCredentialsException:
        sys.exit(
            "Instagram rejected the stored login session.\n"
            f"Log in again:  instaloader --login {username}"
        )
    except TwoFactorAuthRequiredException:
        sys.exit(
            "Two-factor authentication is required for this account.\n"
            f"Run  instaloader --login {username}  and complete the 2FA prompt."
        )
    except ProfileNotExistsException:
        sys.exit(
            f"Profile '{username}' does not exist or is not public.\n"
            "Check the username (no leading '@') and try again."
        )
    except TooManyRequestsException:
        sys.exit(
            "Instagram rate limit hit (too many requests).\n"
            "Wait 30-60 minutes and try again. Avoid running this in a loop."
        )
    except ConnectionException:
        sys.exit(
            "Network error while fetching follower lists.\n"
            "Check your internet connection and try again."
        )
    except InstaloaderException as err:
        sys.exit(f"Instagram request failed: {err}")

    not_following_back = following - followers

    print("\nAccounts not following you back:\n")
    if not_following_back:
        for user in sorted(not_following_back):
            print(user)
    else:
        print("(none - everyone you follow follows you back)")

    print(f"\nTotal: {len(not_following_back)} accounts")


if __name__ == "__main__":
    username = input("Enter your Instagram username: ").strip().lstrip("@")
    if not username:
        sys.exit("No username entered.")
    get_not_following_back(username)
