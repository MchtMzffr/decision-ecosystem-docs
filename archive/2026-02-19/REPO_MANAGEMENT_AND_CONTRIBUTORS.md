# Repo Management and Contributors

## 1. Two Different Concepts

### Contributors
- GitHub’s **Contributors** list shows accounts that have **committed** to the repo.
- This list is **automatic**, based on the `author` field in commits.
- This list **does not grant or revoke permissions**. It only indicates “who made these commits”.

### Who Can Change the Repo? (Access / Permissions)
- People who **can change** the repo (push) are defined under **Settings → Collaborators / Manage access**.
- Only accounts **with write permission there** can push.
- So: “Only I manage it” means **Collaborators** should list only your account (and any accounts you trust).

**Summary:**  
- If **tsgal** appears in the list = some past commits used the `tsgal` username/email.  
- **tsgal being able to change the repo** = only if the `tsgal` account was explicitly given **write permission as a Collaborator**.  
- Without write permission, tsgal only appears as “has committed in the past”; they cannot push anymore.

---

## 2. Managing the Repo Only With Your Account

1. Open the repo on GitHub (e.g. `MeetlyTR/decision-schema`).
2. Go to **Settings** → **Collaborators** (or **Manage access**).
3. If **tsgal** or anyone else has **Write** or **Admin** and you no longer want them to have access:
   - **Remove** that user.
4. Keep only **your account** (and organization roles if needed).

Then **only you (and accounts you granted access) can change the repo**. The Contributors list does not control this.

---

## 3. “Removing” Someone From the Contributors List

- GitHub **does not offer** a way to “remove” a name from the Contributors list.
- The list is **generated automatically** from commit history author information.

Two options:

### Option A: Do Nothing (recommended)
- tsgal may have been used on **your machine** (e.g. `C:\Users\tsgal\...`) for commits made with Cursor.
- So “tsgal” may actually be your work; only the Git user name was different at the time.
- Future commits will use **M.Muzaffer / mucahit.muzaffer@gmail.com**; new contributions will appear under your name.
- Old commits stay as tsgal; this is fine as long as you do not change **permissions**.

### Option B: Change the Author of Past Commits (advanced)
- To set **author** to `M.Muzaffer <mucahit.muzaffer@gmail.com>` for all commits, you need a **git history rewrite**.
- This is done with `git filter-branch` or `git filter-repo`,
- Requires a **force push**,
- And means “history changed” for everyone who has cloned the repo.
- Only do this if you use the repo alone and want a single name to appear; **back up first** and apply only if necessary.

---

## 4. Short Answers

| Question | Answer |
|----------|--------|
| Can someone else change this repo right now? | Only accounts with write permission under **Collaborators / Manage access** can. Check: Settings → Collaborators. |
| What is needed for only my account to manage it? | Have only your (and optionally org) account with write permission under Collaborators. |
| Can I remove tsgal? | **From the permission list:** Yes (Remove from Collaborators). **From the Contributors list:** There is no “remove” option; the list can only change if you rewrite past commit authors. |
| What do I need for my own account? | 1) Git `user.name` / `user.email` = M.Muzaffer / mucahit.muzaffer@gmail.com (already set). 2) Only your (and trusted) accounts have write access to the repo. |

---

## 5. Summary

- **Permission to change** = GitHub **Settings → Collaborators / Manage access**. If only you (and accounts you added) can write, you are the only one managing the repo.
- **Contributors** = Automatic list from commit history. tsgal appears because some commits used that name; you cannot “delete” it from the list, but you can change the list over time by rewriting past commit authors if you wish.
- If you make all future commits as **M.Muzaffer**, new contributions will already appear under your name.
