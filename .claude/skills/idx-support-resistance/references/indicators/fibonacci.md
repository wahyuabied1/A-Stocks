# Fibonacci Retracement & Extension

## Arti
Fibonacci retracement adalah alat untuk memperkirakan **seberapa jauh harga terkoreksi** dari satu pergerakan besar sebelum melanjutkan tren. Level-levelnya diambil dari rasio deret Fibonacci (0, 1, 1, 2, 3, 5, 8, 13, 21, ...) dan menjadi kandidat support atau resistance.

Tidak ada alasan matematis yang membuat harga harus berhenti di level Fibonacci. Level ini bekerja sebagian karena **banyak trader memakainya** (self-fulfilling), sehingga paling bermakna jika bertepatan dengan level harga lain.

## Level yang dipakai
| Level | Asal | Makna umum |
|---|---|---|
| 23,6% | Rasio Fibonacci | Koreksi dangkal, tren sangat kuat |
| 38,2% | Rasio Fibonacci | Koreksi sehat dalam tren kuat |
| 50% | **Bukan** rasio Fibonacci | Titik tengah psikologis, sangat populer |
| 61,8% | Golden ratio | Koreksi dalam, level pembalikan paling sering dikutip |
| 78,6% | Akar dari 61,8% | Koreksi sangat dalam, tren terancam gagal |
| 127,2% / 161,8% | Extension | Proyeksi target setelah harga menembus high/low awal |

Area 61,8–65% sering disebut *golden pocket* oleh sebagian trader.

## Cara menarik
1. **Pilih satu kaki pergerakan yang jelas dan signifikan** pada timeframe yang dianalisis, bukan pullback kecil.
2. **Tren naik**: tarik dari **swing low → swing high**. Level retracement dihitung turun dari high.
3. **Tren turun**: tarik dari **swing high → swing low**. Level retracement dihitung naik dari low.
4. Konsisten memakai **high/low (ekor candle)** atau **close** sebagai titik anchor. Kesalahan paling umum adalah anchor yang salah atau tidak konsisten.

**Rumus tren naik** (range = high − low):
- Retracement r: `high − range × r`
- Extension e: `low + range × e`

**Rumus tren turun**:
- Retracement r: `low + range × r`
- Extension e: `high − range × e`

## Contoh dengan fraksi harga BEI
Kaki naik dari Rp1.000 ke Rp1.500 (range Rp500, fraksi Rp5):

| Level | Hitungan | Hasil | Dibulatkan ke fraksi |
|---|---|---|---|
| 38,2% | 1.500 − 191 | 1.309 | **Rp1.310** |
| 50% | 1.500 − 250 | 1.250 | **Rp1.250** |
| 61,8% | 1.500 − 309 | 1.191 | **Rp1.190** |
| 78,6% | 1.500 − 393 | 1.107 | **Rp1.105** |
| Ext 161,8% | 1.000 + 809 | 1.809 | **Rp1.810** |

Harga yang tidak sesuai fraksi (Rp1.309, Rp1.191) tidak bisa di-order, jadi selalu bulatkan. Perlakukan level sebagai **zona** beberapa tick, bukan satu harga. Harga sering mendekati tanpa menyentuh persis sebelum berbalik.

## Cara membaca kedalaman koreksi
- **Bertahan di 23,6–38,2%**: tren sangat kuat, pembeli tidak sabar menunggu harga murah.
- **Memantul di 50–61,8%**: koreksi normal. Area favorit untuk Buy on Weakness dalam tren naik.
- **Menembus 78,6%** (apalagi close di bawahnya): kaki naik kemungkinan gagal, dan tren perlu dievaluasi ulang.
- **Setelah high ditembus**: extension 127,2% dan 161,8% sering dipakai sebagai target bertahap.

## Kombinasi dengan support & resistance dan indikator lain
Fibonacci paling berguna sebagai **pencari konfluensi**:
- Level Fibonacci yang **bertepatan dengan zona swing historis**, HVN, MA50/MA200, atau angka bulat jauh lebih kuat daripada level Fibonacci sendirian.
- **RSI**: bullish divergence atau RSI keluar dari oversold di level 61,8% memperkuat setup pantulan.
- **Volume**: koreksi ke level Fibonacci dengan volume menurun, lalu pantulan dengan volume naik.
- **Candle**: tunggu candle pembalikan (hammer, bullish engulfing) di level, jangan hanya pasang antrean buta.

Contoh skenario (edukasi): tren naik Rp1.000 → Rp1.500 lalu terkoreksi. Zona Rp1.190–Rp1.250 (Fib 50–61,8%) bertepatan dengan resistance lama Rp1.220 yang sudah ditembus (role reversal) dan MA50. Ini area pantulan yang lebih meyakinkan. Stop di bawah Fib 78,6% (Rp1.105) dan target awal kembali ke high Rp1.500.

## Kekhasan pasar Indonesia
- **Fraksi harga**: bulatkan setiap level. Pada saham harga rendah, jarak antar level Fibonacci bisa hanya beberapa tick sehingga level saling berdempetan dan kurang bermakna.
- **ARA/ARB**: target extension yang jaraknya melebihi batas ARA tidak bisa tercapai dalam satu hari.
- **Saham gorengan**: lonjakan ARA berjilid lalu ARB berjilid membuat anchor ekstrem yang tidak mencerminkan permintaan wajar, sehingga retracement hampir tidak bermakna.
- **Data adjusted**: stock split atau right issue menggeser anchor lama. Gunakan data yang disesuaikan.

## Fibonacci per gaya trading
| Gaya | Kaki yang ditarik |
|---|---|
| Scalper / BPJS | Kaki intraday (misal low–high 30–60 menit pertama) di chart 1–15 menit |
| BSJP | Kaki harian terakhir, untuk menilai apakah close berada di area pantulan |
| Swing | Kaki harian utama 1–6 bulan (penggunaan paling umum) |
| Position / investor | Kaki mingguan multi-bulan atau multi-tahun |

## Kesalahan umum
- Memakai Fibonacci sendirian tanpa level harga lain.
- Memaksakan Fibonacci pada chart tanpa tren jelas (sideways).
- Anchor di pullback kecil, atau berganti-ganti anchor sampai level "cocok" (bias konfirmasi).
- Mengabaikan tren besar (membeli di 61,8% saat tren mingguan turun).
- Menganggap level sebagai harga persis, bukan zona.

## Output script
`scripts/sr_levels.py` menarik Fibonacci dari **high tertinggi dan low terendah dalam rentang lookback**. Arahnya ditentukan oleh mana yang terjadi lebih akhir (low lalu high berarti kaki naik). Output menampilkan tanggal anchor, level retracement dan extension yang sudah dibulatkan ke fraksi, serta posisi harga saat ini (dalam % retracement). Level Fibonacci juga ikut dihitung sebagai **konfluensi** pada zona support/resistance. Jika kaki yang relevan berbeda (misal hanya kaki 2 bulan terakhir), sesuaikan `--lookback` atau hitung manual dari anchor yang tepat.

## Sumber
- [BRIGHTS (BRI Danareksa) — Mengenal Fibonacci Retracement](https://www.brights.id/en/blog/mengenal-fibonacci-retracement)
- [Zerodha Varsity — Fibonacci Retracements](https://zerodha.com/varsity/chapter/fibonacci-retracements/)
- [StockAlarm — Fibonacci Retracement Levels Explained](https://pro.stockalarm.io/blog/fibonacci-retracement-trading-guide)
