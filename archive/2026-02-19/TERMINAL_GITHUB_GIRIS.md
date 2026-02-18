# GitHub Login from the Terminal

## Method 1: GitHub CLI (recommended)

If GitHub CLI is installed, you sign in via browser or token.

### Install (if missing)
```powershell
winget install GitHub.cli
```
Or: https://cli.github.com/

### Sign in (when gh is installed)
```powershell
gh auth login
```
**If `gh` is not recognized:** GitHub CLI is not installed. Install it first: `winget install GitHub.cli` or [cli.github.com](https://cli.github.com/). After installing, open a **new terminal** and run `gh auth login`.  
Alternative: use **Method 2** (Git HTTPS + Personal Access Token) for push; `gh` is not required.

- Choose "GitHub.com"  
- Choose "HTTPS"  
- Choose "Login with a web browser" or "Paste an authentication token"  
- If the browser opens, enter the code; if using a token, paste the token  

### Check status
```powershell
gh auth status
```

### Cloning all ecosystem repos from a personal account (e.g. MchtMzffr)

If the repos exist under **MchtMzffr** (created or forked by you), run in the same folder:

```powershell
gh repo clone MchtMzffr/decision-schema
gh repo clone MchtMzffr/mdm-engine
gh repo clone MchtMzffr/decision-modulation-core
gh repo clone MchtMzffr/ops-health-core
gh repo clone MchtMzffr/evaluation-calibration-core
```

Change to the target folder first (e.g. Desktop):
```powershell
cd $env:USERPROFILE\Desktop
```

---

## Method 2: Git HTTPS (with token)

Git will ask for username and password on push/pull. GitHub no longer **accepts account passwords**; you must use a **Personal Access Token (PAT)**.

### 1) Create a token
1. GitHub → top-right profile → **Settings**
2. Left menu → **Developer settings** → **Personal access tokens** → **Tokens (classic)** or **Fine-grained tokens**
3. **Generate new token**
4. Check **repo** (or the scopes you need)
5. Copy the token (it is shown once; store it safely)

### 2) Sign in on first push
When you run a push command, Git will prompt:
- **Username:** Your GitHub username (e.g. `MchtMzffr` or `MeetlyTR`)
- **Password:** Not your password — use the **Personal Access Token** you created

```powershell
cd "c:\Users\tsgal\Desktop\Decision Ecosystem\decision-schema"
git push origin main
```

### 3) Storing credentials (so you are not asked again)
On Windows, the credential helper can store them after the first entry:

```powershell
git config --global credential.helper manager
```
Then on the first `git push` or `git pull` you enter username + token; later runs will not prompt.

---

## Method 3: SSH key

To push/pull without entering password/token using SSH:

### 1) Create SSH key
```powershell
ssh-keygen -t ed25519 -C "mucahit.muzaffer@gmail.com" -f "$env:USERPROFILE\.ssh\id_ed25519_github"
```
Press Enter (passphrase optional) to finish.

### 2) Add public key to GitHub
```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_github.pub"
```
Copy the output line.  
GitHub → **Settings** → **SSH and GPG keys** → **New SSH key** → paste.

### 3) Switch remote to SSH
If the current remote is HTTPS, switch to SSH:
```powershell
cd "c:\Users\tsgal\Desktop\Decision Ecosystem\decision-schema"
git remote set-url origin git@github.com:MeetlyTR/decision-schema.git
git push origin main
```

---

## Quick reference

| Goal | Command |
|------|--------|
| Sign in with GitHub CLI | `gh auth login` |
| Check sign-in status | `gh auth status` |
| Store credentials | `git config --global credential.helper manager` |
| First push (HTTPS) | `git push origin main` → enter username + **Token** |

**Important:** Do not share the token; ensure no one can see it when you paste it in the terminal.
