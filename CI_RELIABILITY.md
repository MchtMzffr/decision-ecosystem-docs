# CI Güvenilirlik Rehberi

**Amaç:** CI’nin ara ara hata vermesinin nedenleri ve alınan önlemler.

---

## “Ara ara hata” normal mi?

Kısmen **evet**. Aşağıdakiler tek seferlik/geçici hatalara yol açabilir; tamamen sıfırlamak mümkün değil, **azaltmak** mümkün.

---

## Olası nedenler

| Neden | Açıklama | Alınan önlem |
|-------|----------|----------------|
| **Ağ / PyPI / GitHub** | `pip install` veya `git clone` zaman aşımı, geçici kesinti | Pip adımlarında **bir kez retry** (önce bekleyip tekrar dene, olmazsa git fallback) |
| **Job takılması** | Adım cevap vermeyince run saatlerce sürer | Her job’a **timeout-minutes** (15–25 dk) |
| **Concurrency iptali** | Yeni push yapıldığında önceki run **iptal** edilir | Bu “failure” değil, **cancelled**; UI’da “Cancelled” olarak görünür |
| **Matrix’te tek fail** | Varsayılan `fail-fast: true` ile bir Python versiyonu fail edince diğeri de iptal edilir | **fail-fast: false** ile 3.11 ve 3.12 ayrı ayrı biter, hangi ortamda fail olduğu netleşir |

---

## Yapılan iyileştirmeler (tüm repolarda)

1. **Job timeout**
   - `timeout-minutes: 15` (tek job’lı workflow’lar)
   - `timeout-minutes: 20` (integration-harness core_only)
   - `timeout-minutes: 25` (integration-harness full_stack)

2. **Pip retry**
   - Test aracı: `pip install ... || (sleep 15 && pip install ...)`
   - Bağımlılıklar: `pip install pkg... || (sleep 20 && pip install pkg...) || pip install git+...`
   - Böylece geçici ağ hatası tek denemede fail etmez.

3. **fail-fast: false**
   - Matrix’te (örn. 3.11, 3.12) bir hücre fail etse bile diğeri çalışır; raporlama daha net.

4. **decision-schema pin (core’lar)**
   - Tüm core’larda `>=0.2.2` + fallback `@v0.2.2` kullanılıyor; tek SSOT sürümü ile tutarlılık.

---

## UI’da gördüğün durumlar

- **Failed (kırmızı):** En az bir step gerçekten hata verdi. Log’a bak; çoğu zaman “pip” veya “pytest” satırında sebep yazar.
- **Cancelled (gri):** Yeni bir push bu run’ı iptal etti. Kod hatası değil; istersen “Re-run all jobs” ile aynı commit’i tekrar çalıştırabilirsin.
- **Success (yeşil):** Tüm adımlar geçti.

---

## Garanti mümkün mü?

**%100 garanti mümkün değil** (ağ, GitHub/PyPI kesintisi, runner problemi kontrolümüz dışında). Yapılanlarla:

- Geçici ağ hataları büyük ölçüde **retry** ile toparlanır.
- Takılan job’lar **timeout** ile kesilir, sonsuz bekleyen run kalmaz.
- **fail-fast: false** ile hangi Python/ortamda fail olduğu net görülür.

Ek istersen: flaky test’ler için pytest’te `--flake-finder` veya belirli testlere `@pytest.mark.flaky(retries=2)` eklenebilir; şu an workflow seviyesi önlemler uygulandı.

---

## Hangi repolarda güncellendi

- decision-schema  
- mdm-engine  
- ops-health-core  
- evaluation-calibration-core  
- decision-modulation-core  
- execution-orchestration-core  
- decision-ecosystem-integration-harness  

Hepsi aynı pattern: `timeout-minutes`, `fail-fast: false`, pip retry.

---

**Son güncelleme:** 2026-02-18
