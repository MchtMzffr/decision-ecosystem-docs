# Terminal Üzerinden GitHub Girişi

## Yöntem 1: GitHub CLI (Önerilen)

GitHub CLI yüklüyse tarayıcı veya token ile giriş yaparsınız.

### Kurulum (yoksa)
```powershell
winget install GitHub.cli
```
Veya: https://cli.github.com/

### Giriş (gh yüklüyse)
```powershell
gh auth login
```
**`gh` komutu tanınmıyorsa:** GitHub CLI yüklü değildir. Önce kurun: `winget install GitHub.cli` veya [cli.github.com](https://cli.github.com/). Kurulumdan sonra **yeni bir terminal** açıp `gh auth login` çalıştırın.  
Alternatif: **Yöntem 2** (Git HTTPS + Personal Access Token) ile push yapabilirsiniz; `gh` gerekmez.

- "GitHub.com" seçin  
- "HTTPS" seçin  
- "Login with a web browser" veya "Paste an authentication token" seçin  
- Tarayıcı açılırsa kodu girin; token kullanacaksanız token’ı yapıştırın  

### Kontrol
```powershell
gh auth status
```

### Kişisel hesaptan (MchtMzffr) tüm ekosistem repolarını klonlama

Repolar **MchtMzffr** altında mevcutsa (sizin oluşturduğunuz veya fork), aynı klasörde sırayla:

```powershell
gh repo clone MchtMzffr/decision-schema
gh repo clone MchtMzffr/mdm-engine
gh repo clone MchtMzffr/decision-modulation-core
gh repo clone MchtMzffr/ops-health-core
gh repo clone MchtMzffr/evaluation-calibration-core
```

Önce ilgili klasöre gidin (örn. masaüstü):
```powershell
cd $env:USERPROFILE\Desktop
```

---

## Yöntem 2: Git HTTPS (Token ile)

Push/pull sırasında Git sizden kullanıcı adı ve şifre ister. GitHub artık **şifre kabul etmez**; **Personal Access Token (PAT)** kullanmanız gerekir.

### 1) Token oluşturma
1. GitHub → Sağ üst profil → **Settings**
2. Sol menü → **Developer settings** → **Personal access tokens** → **Tokens (classic)** veya **Fine-grained tokens**
3. **Generate new token**
4. **repo** (veya gerekli scope’lar) işaretleyin
5. Token’ı kopyalayın (bir kez gösterilir; kaydedin)

### 2) İlk push’ta giriş
Aşağıdaki komutlardan birini çalıştırdığınızda Git sizden ister:
- **Username:** GitHub kullanıcı adınız (örn. `MchtMzffr` veya `MeetlyTR`)
- **Password:** Şifre değil, **oluşturduğunuz Personal Access Token**

```powershell
cd "c:\Users\tsgal\Desktop\Decision Ecosystem\decision-schema"
git push origin main
```

### 3) Bilgileri saklamak (tekrar sormasın)
Windows’ta credential helper ile bir kez girince saklanır:

```powershell
git config --global credential.helper manager
```
Sonra ilk `git push` veya `git pull`’da kullanıcı adı + token girilir; sonrakilerde sorulmaz.

---

## Yöntem 3: SSH Key

SSH ile şifre/token girmeden push/pull yapmak için:

### 1) SSH key oluşturma
```powershell
ssh-keygen -t ed25519 -C "mucahit.muzaffer@gmail.com" -f "$env:USERPROFILE\.ssh\id_ed25519_github"
```
Enter’a basıp (passphrase isteğe bağlı) bitirin.

### 2) Public key’i GitHub’a ekleme
```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_github.pub"
```
Çıkan satırı kopyalayın.  
GitHub → **Settings** → **SSH and GPG keys** → **New SSH key** → yapıştırın.

### 3) Remote’u SSH yapma
Mevcut remote HTTPS ise SSH’a çevirin:
```powershell
cd "c:\Users\tsgal\Desktop\Decision Ecosystem\decision-schema"
git remote set-url origin git@github.com:MeetlyTR/decision-schema.git
git push origin main
```

---

## Hızlı Özet

| Amaç | Komut |
|------|--------|
| GitHub CLI ile giriş | `gh auth login` |
| Giriş durumunu kontrol | `gh auth status` |
| Credential’ı saklamak | `git config --global credential.helper manager` |
| İlk kez push (HTTPS) | `git push origin main` → username + **Token** girin |

**Önemli:** Token’ı kimseyle paylaşmayın; terminale yapıştırırken başkası görmesin.
