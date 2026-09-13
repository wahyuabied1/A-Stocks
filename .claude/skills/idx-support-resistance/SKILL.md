---
name: idx-support-resistance
description: Mendeteksi dan menjelaskan level support & resistance saham Indonesia (Bursa Efek Indonesia / IDX / IHSG) dari data harga OHLCV — swing high/low, cluster level, volume profile, pivot point, VWAP, moving average — lalu merapikannya sesuai aturan BEI (fraksi harga/tick size, batas ARA/ARB, lot 100 lembar, harga minimum) dan menyesuaikannya dengan gaya trading (scalper, BPJS/day trading, BSJP, swing, position trader, investor, ARA hunter), dilengkapi pola candlestick dan indikator pendukung moving average, MACD, RSI, volume, bid/offer (order book), dan Fibonacci. Gunakan skill ini setiap kali user menyebut support, resistance, "sup/res", area demand/supply, level entry/stop loss/target, breakout/breakdown, buy on weakness/breakout, istilah gaya trading seperti scalping, BSJP, BPJS, swing, ARA hunter, pola candlestick (hammer, doji, engulfing, morning star, marubozu, gap, candle ARA/ARB), indikator moving average/MA/EMA/golden cross/death cross, MACD, RSI/divergence, volume/volume spike/akumulasi-distribusi, bid/offer/antrean/order book/running trade/IEP, Fibonacci retracement, atau minta analisis teknikal/chart untuk kode saham 4 huruf seperti BBCA, BBRI, TLKM, ANTM, GOTO, atau file CSV harga saham .JK — walaupun user tidak menyebut kata "support" atau "resistance" secara eksplisit. Juga gunakan saat user bertanya arti atau perbedaan gaya trading saham Indonesia, atau cara membaca candlestick, moving average, MACD, RSI, volume, bid/offer, dan Fibonacci.
---

# Deteksi Support & Resistance Saham Indonesia (IDX)

Support adalah area harga di mana tekanan beli historis cukup kuat untuk menahan penurunan. Resistance adalah area di mana tekanan jual menahan kenaikan. Keduanya berupa **zona**, bukan satu angka persis, karena harga sering menembus sedikit lalu kembali. Tugas skill ini: menemukan zona tersebut secara sistematis dari data, menyesuaikannya dengan gaya trading user, lalu menyajikannya dalam harga yang benar-benar bisa dipasang di order book BEI.

Kenapa aturan BEI penting: level seperti "Rp1.237" tidak bisa di-order kalau fraksi harganya Rp5, dan target "naik 30% besok" mustahil jika batas ARA 25%. Analisis yang mengabaikan mikrostruktur ini terlihat pintar tapi tidak bisa dieksekusi.

## Sesuaikan dengan gaya trading
"Support yang penting" berbeda untuk tiap gaya. Scalper peduli high kemarin dan VWAP, sedangkan investor peduli dasar konsolidasi 5 tahun. Tentukan gaya trading user dari percakapan (misal "buat BSJP besok", "mau swing 2 minggu", "nabung jangka panjang"), lalu **baca file gaya yang sesuai** sebelum menganalisis:

| Gaya | Horizon | Data yang dipakai | `--style` | File |
|---|---|---|---|---|
| Scalper | detik–menit | 1 menit + order book | `scalper` | `references/trading-styles/scalper.md` |
| BPJS (Beli Pagi Jual Sore) / day trader | menit–jam, tutup hari itu | 5–15 menit + harian | `bpjs` | `references/trading-styles/bpjs.md` |
| BSJP (Beli Sore Jual Pagi) | 1 malam | harian (3 bulan) + sesi terakhir | `bsjp` | `references/trading-styles/bsjp.md` |
| ARA hunter | jam–beberapa hari | harian + antrean ARA | `ara-hunter` | `references/trading-styles/ara-hunter.md` |
| Swing trader | hari–minggu | harian (1 tahun) + mingguan | `swing` | `references/trading-styles/swing.md` |
| Position trader | minggu–bulan | harian 2 tahun + mingguan | `position` | `references/trading-styles/position.md` |
| Investor (value/growth/dividen) | tahunan | mingguan 5–10 tahun | `investor` | `references/trading-styles/investor.md` |

Jika gaya tidak disebut, gunakan **swing (data harian)** sebagai default dan sebutkan bahwa levelnya bisa berbeda untuk gaya lain. Tidak perlu menunda analisis hanya untuk bertanya. Jika user hanya bertanya arti atau perbedaan gaya trading, jawab dari file-file tersebut.

## Indikator pendukung
Support & resistance menjadi lebih meyakinkan jika dikonfirmasi momentum, partisipasi, dan antrean. Baca file indikator saat user menyebut indikatornya, atau saat perlu menjelaskan konfirmasi sebuah level:

| Indikator | Kegunaan untuk S/R | Dihitung script? | File |
|---|---|---|---|
| Candlestick | Price action di level: candle pembalikan/lanjutan, gap, candle ARA/ARB | Ya (pola 3 bar terakhir + lokasi & volume) | `references/indicators/candlestick.md` |
| Moving average | Arah tren, support/resistance dinamis (MA20/50/200), susunan MA, golden/death cross | Ya (MA5–MA200, EMA20, slope, crossover) | `references/indicators/moving-average.md` |
| MACD | Arah & perubahan momentum di level: crossover, histogram, divergence | Ya (12,26,9 + divergence) | `references/indicators/macd.md` |
| RSI | Momentum di level: oversold/overbought, divergence di support/resistance | Ya (RSI 14 + divergence) | `references/indicators/rsi.md` |
| Volume | Validasi pantulan/breakout, akumulasi-distribusi, OBV, likuiditas | Ya (spike, OBV, rasio naik/turun) | `references/indicators/volume.md` |
| Bid & offer | Support/resistance mikro dari antrean, running trade, IEP/IEV, antrean ARA/ARB | Tidak (butuh data order book real-time) | `references/indicators/bid-offer.md` |
| Fibonacci | Level retracement/extension sebagai kandidat zona & konfluensi | Ya (dari high/low lookback) | `references/indicators/fibonacci.md` |

Data order book tidak tersedia dari OHLCV. Jika user membagikan screenshot atau angka antrean, baca dengan panduan `bid-offer.md` dan perlakukan sebagai informasi jangka sangat pendek.

## Alur kerja

### 1. Siapkan data
- Minta atau cari data **OHLCV** (Date/Datetime, Open, High, Low, Close, Volume) dengan timeframe sesuai gaya (lihat tabel di atas).
- Sumber umum: file CSV/Excel dari user, export aplikasi sekuritas, atau `yfinance` dengan akhiran `.JK` (contoh `BBCA.JK`). Pakai yfinance hanya jika paketnya sudah terpasang atau user setuju memasangnya. Data 1 menit di yfinance hanya tersedia ±7 hari, data 5 menit ±60 hari.
- Gunakan **harga yang disesuaikan (adjusted)** jika saham pernah stock split, reverse split, right issue, atau bonus saham. Tanpa penyesuaian, level lama bisa bergeser berkali-kali lipat. Lonjakan >40% dalam sehari tanpa volume besar biasanya tanda aksi korporasi, karena batas ARA membuat lonjakan sebesar itu hampir mustahil dalam satu hari normal.
- Jika user tidak punya data dan data tidak bisa diambil, jelaskan metodenya dan minta data. Jangan mengarang angka harga.

### 2. Jalankan script perhitungan
Script `scripts/sr_levels.py` (Python murni, tanpa dependensi) melakukan semua perhitungan deterministik:

```bash
python3 <skill-dir>/scripts/sr_levels.py --csv data/BBCA.csv --style swing
python3 <skill-dir>/scripts/sr_levels.py --csv data/BBRI_5m.csv --style bpjs
python3 <skill-dir>/scripts/sr_levels.py --ticker BBCA --style investor   # butuh yfinance
python3 <skill-dir>/scripts/sr_levels.py --csv data.csv --json            # output mesin
```

`--style` mengatur timeframe yfinance, lookback, dan lebar fractal swing. Opsi lain yang ditulis eksplisit akan menimpa preset: `--lookback`, `--window`, `--interval`, `--period`, `--board` (`utama`/`pengembangan`/`ekonomi-baru`, `akselerasi`, `pemantauan`), `--arb-pct` (default 0,15), dan `--price-rule` (`lama` = minimum Rp50, `baru` = minimum Rp1 dengan ARA/ARB nominal Rp1 untuk harga Rp1–10; lihat status aturan di `references/idx-rules.md`).

Script mendeteksi timeframe data (intraday/harian/mingguan) dan mengeluarkan:
- harga terakhir, fraksi, dan batas ARA/ARB (sesi berjalan untuk data intraday, dan sesi berikutnya)
- zona support & resistance beserta skor dan konfluensinya
- volume profile (HVN)
- pivot klasik dan MA20/50/200
- untuk data intraday: high/low sesi sebelumnya, opening range 30 menit, dan VWAP
- pola candlestick 3 bar terakhir (pembalikan, lanjutan, gap, candle ARA/ARB) beserta zona yang diuji dan volumenya
- moving average (MA5–MA200 dan EMA20: jarak, slope, susunan, golden/death cross) dan MACD (12,26,9: crossover, histogram, divergence)
- RSI(14) dan divergence, analisis volume (spike, OBV, rasio volume naik/turun), serta Fibonacci retracement/extension dari high–low lookback
- peringatan likuiditas dan data

Pakai script daripada menghitung manual, karena pembulatan tick dan clustering mudah salah jika dikerjakan di kepala.

### 3. Validasi dan interpretasi (bagian yang butuh penilaian)
Angka dari script adalah kandidat. Pertimbangkan hal-hal berikut sebelum menyajikannya, dengan penekanan sesuai file gaya trading.

**Kekuatan level**: semakin banyak faktor yang bertemu (konfluensi), semakin kuat.
- Jumlah sentuhan: 3+ pantulan jauh lebih bermakna daripada 1.
- Kebaruan: level yang diuji baru-baru ini (relatif terhadap horizon gaya) lebih relevan.
- Volume: pantulan dengan volume di atas rata-rata menunjukkan partisipasi nyata.
- Bertepatan dengan HVN, MA, VWAP (intraday), level Fibonacci, atau angka psikologis.
- Dikonfirmasi price action: candle pembalikan (hammer, bullish engulfing, morning star) di support, atau (shooting star, bearish engulfing, evening star) di resistance, idealnya diikuti candle konfirmasi.
- Didukung momentum dan partisipasi: MACD crossover atau histogram berbalik di level, RSI oversold atau bullish divergence di support, bearish divergence di resistance, volume spike saat pantulan atau breakout, OBV searah harga.

**Kekhasan pasar Indonesia:**
- *Angka bulat & batas fraksi*: Rp50 (lantai saham gocap selama harga minimum masih Rp50), Rp100, Rp200, Rp500, Rp1.000, Rp2.000, Rp5.000, Rp10.000. Batas pergantian fraksi (200, 500, 2.000, 5.000) sering memunculkan penumpukan antrean karena spread per tick berubah.
- *ARA/ARB*: batas harian mutlak. Resistance di atas harga ARA tidak mungkin tercapai dalam sesi itu. Script menandainya.
- *Order book*: untuk intraday, antrean bid/offer tebal di satu harga berfungsi sebagai support/resistance jangka sangat pendek. Antrean ini bisa dicabut kapan saja (spoofing), jadi jangan anggap setara level historis.
- *Likuiditas*: saham dengan nilai transaksi rata-rata kecil (misal di bawah ~Rp1 miliar/hari) sering bergerak "loncat" beberapa tick dan level teknikalnya kurang andal. Saham di Papan Pemantauan Khusus (full call auction) perlu diperlakukan hati-hati.
- *Ex-date dividen*: harga turun sebesar dividen pada ex-date. Gap ini bukan breakdown support.
- *Suspensi / UMA*: data tidak kontinu. Jangan menarik level dari celah suspensi.

**Role reversal**: support yang tembus (close di bawahnya dengan volume) cenderung menjadi resistance, dan sebaliknya.

**Konfirmasi breakout/breakdown** (heuristik umum, bukan aturan pasti):
- Close menembus zona pada timeframe gaya tersebut, bukan hanya shadow/ekor.
- Volume ≥ 1,5× rata-rata 20 bar.
- Idealnya bertahan atau di-retest tanpa kembali ke dalam zona.

### 4. Rapikan ke harga yang valid
Semua level yang disajikan harus sesuai fraksi harga BEI. Saat membentuk batas zona, support dibulatkan ke bawah dan resistance ke atas. Untuk titik tengah, gunakan pembulatan terdekat. Detail tabel fraksi, ARA/ARB, jam perdagangan, dan papan ada di `references/idx-rules.md`. Baca file itu saat perlu menjelaskan aturan atau menangani saham di papan non-reguler.

Jika user membahas skenario entry/stop, hitung dalam **lot** (1 lot = 100 lembar) dan sertakan estimasi biaya (umumnya ±0,15% beli dan ±0,25% jual termasuk PPh final 0,1%, tergantung sekuritas). Stop loss atau target yang hanya 1–2 tick bisa lebih kecil dari biaya transaksi. Sebutkan jika hal ini terjadi.

## Format output

Gunakan struktur ini. Sesuaikan panjangnya dengan pertanyaan user, karena pertanyaan singkat cukup dijawab singkat:

```markdown
# Support & Resistance — [KODE] ([gaya trading], data [timeframe] [periode], per [tanggal/jam bar terakhir])

**Harga terakhir:** Rp[x] · **Fraksi:** Rp[x] · **Rentang ARA/ARB [sesi]:** Rp[x] – Rp[x]
**Tren:** [posisi terhadap MA / VWAP dan artinya singkat]

## Resistance (dari terdekat)
| # | Zona | Jarak | Kekuatan | Alasan |
|---|------|-------|----------|--------|
| R1 | Rp[a] – Rp[b] | +x% | Kuat/Sedang/Lemah | [touches, volume, konfluensi] |

## Support (dari terdekat)
| # | Zona | Jarak | Kekuatan | Alasan |
|---|------|-------|----------|--------|
| S1 | Rp[a] – Rp[b] | -x% | Kuat/Sedang/Lemah | [touches, volume, konfluensi] |

## Skenario untuk [gaya trading]
- **Jika bertahan di atas S1:** ...
- **Jika tembus S1 dengan volume:** ... (S1 berpotensi menjadi resistance)
- **Jika breakout R1:** ...

## Catatan
[waktu/sesi relevan, likuiditas, aksi korporasi, keterbatasan data, asumsi aturan ARA/ARB]

_Analisis teknikal ini bersifat edukasi, bukan rekomendasi beli/jual. Keputusan investasi sepenuhnya tanggung jawab investor._
```

Tampilkan maksimal 3 support dan 3 resistance terdekat, karena daftar panjang justru membingungkan. Jarak persentase dari harga terakhir membantu user menilai relevansi.

## Batasan yang perlu dijaga
- Support/resistance adalah probabilitas, bukan kepastian. Hindari bahasa seperti "pasti mantul" atau "target pasti".
- Jangan memberi rekomendasi personal ("kamu sebaiknya beli 50 lot"). Sajikan skenario dan level, dan biarkan keputusan di tangan user. Jika diminta nasihat personal, jelaskan bahwa kamu bukan penasihat keuangan berlisensi.
- Untuk gaya berisiko sangat tinggi (scalping dengan leverage, ARA hunter, saham gorengan), jelaskan risikonya secara jujur dan jangan meromantisasi potensi untungnya.
- Sebutkan tanggal data. Level dari data lama bisa sudah tidak relevan.
- Aturan BEI (fraksi, ARA/ARB, harga minimum, jam, biaya) bisa berubah. Jika hasil bergantung pada angka itu, ingatkan untuk verifikasi di idx.co.id.
