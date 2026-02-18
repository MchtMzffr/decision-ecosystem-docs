# Git Kimlik Kontrolü — Commit'lerde Sizin Adınız Görünsün

## Şu an ayarlı kimlik

Tüm commit ve push işlemlerinde **sizin adınız** (Mücahit Muzaffer Karafil) ve **e-postanız** (mucahit.muzaffer@gmail.com) kullanılsın diye global Git ayarları yapıldı:

- **user.name:** Mücahit Muzaffer Karafil  
- **user.email:** mucahit.muzaffer@gmail.com  

Bu e-posta GitHub hesabınızda (Public email) kayıtlı olduğu için, **yeni commit'ler Katkıda Bulunanlar listesinde sizin profilinize** işlenecek.

---

## Commit / push öncesi kontrol

Terminalde şunu çalıştırın:

```powershell
git config --global user.name
git config --global user.email
```

Çıktı şöyle olmalı:
- `Mücahit Muzaffer Karafil`
- `mucahit.muzaffer@gmail.com`

Böyleyse **tsgal** veya başka bir isimle commit atılmaz; her commit sizin adınıza görünür.

---

## Push için giriş (HTTPS)

Push yaparken GitHub girişi istenebilir:

- **HTTPS** kullanıyorsanız: GitHub kullanıcı adı + **Personal Access Token** (şifre yerine) girin.  
  Token: GitHub → Settings → Developer settings → Personal access tokens.
- **SSH** kullanıyorsanız: SSH key’iniz hesabınıza tanımlı olmalı; ek giriş gerekmez.

Push’u hangi GitHub hesabıyla yaparsanız, commit’ler o hesaba gider. Commit’teki **author** (adınız) zaten `user.name` / `user.email` ile ayarlı; push sadece “hangi hesaptan gönderildiği”ni belirler.

---

## Özet

| Ne | Ayar |
|----|------|
| Commit’te görünen isim | Mücahit Muzaffer Karafil |
| Commit’te görünen e-posta | mucahit.muzaffer@gmail.com |
| Katkıda bulunanlarda | Bu e-posta GitHub’da sizin hesabınıza bağlı olduğu için **sizin adınız** görünür. |

Bundan sonra bu bilgisayarda yapacağınız tüm commit’ler **tsgal** veya default bir isimle değil, **Mücahit Muzaffer Karafil** olarak kaydedilir ve GitHub’da sizin profilinize yansır.
