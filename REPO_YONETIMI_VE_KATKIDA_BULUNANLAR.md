# Repo Yönetimi ve Katkıda Bulunanlar

## 1. İki Farklı Kavram

### Katkıda Bulunanlar (Contributors)
- GitHub’daki **Contributors** listesi, repoya **commit atmış** hesapları gösterir.
- Bu liste **otomatik** oluşur; commit’lerdeki `author` bilgisine göre.
- Bu liste **yetki vermez veya kaldırmaz**. Sadece “bu commit’leri kim yaptı” bilgisidir.

### Repoyu Kim Değiştirebilir? (Erişim / Permissions)
- Repoyu **değiştirebilen** (push atabilen) kişiler: **Settings → Collaborators / Manage access** ile tanımlıdır.
- Sadece **burada yazma yetkisi olan** hesaplar push atabilir.
- Yani: “Sadece ben yöneteyim” demek = **Collaborators** kısmında sadece kendi hesabınız (veya güvendiğiniz hesaplar) olsun demektir.

**Özet:**  
- **tsgal** listede görünüyorsa = geçmişte bazı commit’ler `tsgal` kullanıcı adı/e-postası ile atılmış.  
- **tsgal’in repoyu değiştirebilmesi** = sadece `tsgal` hesabına **Collaborator olarak yazma yetkisi verildiyse** mümkündür.  
- Yazma yetkisi yoksa tsgal sadece “geçmişte commit atmış” olarak görünür; artık push atamaz.

---

## 2. Repoyu Sadece Kendi Hesabınızla Yönetmek

1. GitHub’da ilgili repoya gidin (örn. `MeetlyTR/decision-schema`).
2. **Settings** → **Collaborators** (veya **Manage access**).
3. **tsgal** veya başka biri listede **yazma (Write)** veya **admin** ile görünüyorsa ve bu kişinin artık erişimi olmamasını istiyorsanız:
   - İlgili kullanıcıyı **Remove** edin.
4. Sadece **kendi hesabınız** (Mücahit Muzaffer / MeetlyTR) ve gerekirse organizasyon rolleri kalsın.

Böylece **repoyu fiilen sadece siz (ve yetki verdiğiniz hesaplar) değiştirebilir** hale gelir. Contributors listesi buna bağlı değildir.

---

## 3. “tsgal”i Katkıda Bulunanlar Listesinden Silmek

- GitHub’da **Contributors listesinden bir ismi “silmek”** diye bir seçenek **yoktur**.
- Liste, **commit geçmişindeki author bilgisine** göre otomatik oluşur.

İki yol vardır:

### Seçenek A: Hiçbir Şey Yapmamak (Önerilen)
- tsgal, **sizin bilgisayarınızda** (örn. `C:\Users\tsgal\...`) Cursor ile yapılan commit’lerde kullanılmış olabilir.
- Yani “tsgal” aslında sizin yaptığınız işler olabilir; sadece o anki Git kullanıcı adı farklıydı.
- Gelecek commit’ler artık **M.Muzaffer / mucahit.muzaffer@gmail.com** ile atılacak; yeni katkılar sizin adınıza görünür.
- Eski commit’ler tsgal olarak kalır; **yetki** tarafında bir değişiklik yapmadığınız sürece sorun olmaz.

### Seçenek B: Eski Commit’lerin Yazarını Değiştirmek (İleri Seviye)
- Tüm commit’lerdeki **author**’ı `M.Muzaffer <mucahit.muzaffer@gmail.com>` yapmak için **git history rewrite** gerekir.
- Bu işlem:
  - `git filter-branch` veya `git filter-repo` ile yapılır,
  - **Force push** gerektirir,
  - Tüm clone edenler için “history değişti” anlamına gelir.
- Eğer repo’yu tek başınıza kullanıyorsanız ve “tek isim görünsün” istiyorsanız yapılabilir; ama **mutlaka yedek alıp** ve sadece gerekirse uygulayın.

---

## 4. Kısa Cevaplar

| Soru | Cevap |
|------|--------|
| Başkası şu an bu repoyu değiştirebiliyor mu? | Sadece **Collaborators / Manage access**’te yazma yetkisi verdiğiniz hesaplar değiştirebilir. Kontrol: Settings → Collaborators. |
| Sadece benim hesabım yönetiyor olması için ne gerekir? | Collaborators’da sadece sizin (ve isterseniz organizasyon) hesabınızın yazma yetkisi olması yeterli. |
| tsgal’i silebiliyor muyum? | **Yetki listesinden** silmek: Evet (Collaborators’dan Remove). **Contributors listesinden** “silme” seçeneği yok; sadece eski commit’lerin yazarını değiştirirseniz liste zamanla değişir. |
| Kendi hesabım için ne gerekiyor? | 1) Git’te `user.name` / `user.email` = M.Muzaffer / mucahit.muzaffer@gmail.com (zaten ayarlı). 2) Repo erişiminde sadece sizin (ve güvendiğiniz) hesapların yazma yetkisi olması. |

---

## 5. Özet

- **Değiştirme yetkisi** = GitHub **Settings → Collaborators / Manage access**. Sadece siz (ve eklediğiniz hesaplar) yazabiliyorsa repoyu sadece siz yönetiyorsunuz demektir.
- **Katkıda bulunanlar** = Sadece commit geçmişine göre otomatik liste. tsgal orada çünkü bazı commit’ler o isimle atıldı; bunu “hesaptan silmek” yok, isterseniz eski commit’lerin yazarını değiştirerek listeyi değiştirebilirsiniz.
- İleride tüm commit’leri **M.Muzaffer** ile atarsanız, yeni katkılar zaten sizin adınıza görünecektir.
