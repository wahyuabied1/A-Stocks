# Moving Average (MA)

## Arti
Moving average adalah **rata-rata harga penutupan selama n bar terakhir** yang terus bergeser setiap bar baru muncul. MA menghaluskan naik-turun harga jangka pendek sehingga **arah tren** lebih mudah terlihat. MA juga sering berfungsi sebagai **support/resistance dinamis**, yaitu level yang ikut bergerak mengikuti harga, berbeda dengan support/resistance horizontal.

MA adalah indikator **lagging** (tertinggal): MA merangkum harga masa lalu dan tidak memprediksi harga.

## Jenis-jenis
| Jenis | Cara hitung | Sifat |
|---|---|---|
| **SMA** (Simple) | Jumlah close n bar ÷ n | Semua bar berbobot sama; halus tapi lambat |
| **EMA** (Exponential) | `EMA hari ini = close × k + EMA kemarin × (1 − k)`, dengan `k = 2 / (n + 1)` | Bobot lebih besar pada harga terbaru; lebih cepat bereaksi |
| **WMA** (Weighted) | Bobot linear (bar terbaru paling besar) | Di antara SMA dan EMA |

Contoh SMA5 dengan close Rp1.200, 1.210, 1.190, 1.220, 1.230: (1.200 + 1.210 + 1.190 + 1.220 + 1.230) ÷ 5 = **Rp1.210**.

Di aplikasi sekuritas Indonesia, "MA20" biasanya berarti SMA 20 hari. Periksa pengaturan chart karena sebagian platform memakai EMA secara default.

## Periode yang umum dipakai
Bursa Indonesia punya sekitar 20–21 hari bursa per bulan dan ±240 hari bursa per tahun.

| MA (harian) | Kira-kira mewakili | Kegunaan umum |
|---|---|---|
| MA5 / MA10 | 1–2 minggu | Momentum sangat pendek; populer di trader harian Indonesia |
| MA20 | ±1 bulan | Ritme tren dan pullback swing; support dinamis tren kuat |
| MA50 | ±2,5 bulan | Tren menengah; filter arah untuk swing dan position |
| MA100 | ±5 bulan | Tren menengah–panjang |
| MA200 | ±10 bulan | Batas tren besar (bull vs bear); acuan institusi |

## Cara membaca
### 1. Posisi harga terhadap MA
- Harga **di atas** MA berarti tren periode tersebut cenderung naik. Harga **di bawah** MA berarti cenderung turun.
- Close yang menembus MA dengan volume menandakan perubahan tren periode itu. Tembus hanya lewat ekor candle kurang bermakna.

### 2. Kemiringan (slope)
- MA yang **menanjak** menunjukkan tren naik yang aktif, MA **menurun** menunjukkan tren turun, dan MA **datar** menunjukkan sideways.
- Harga di atas MA yang datar lebih lemah daripada harga di atas MA yang menanjak.

### 3. Susunan beberapa MA (alignment)
- **MA20 > MA50 > MA200, semuanya menanjak**: tren naik sehat di semua horizon.
- **MA20 < MA50 < MA200, semuanya menurun**: tren turun di semua horizon.
- **Susunan campuran**: fase transisi atau sideways, dan sinyal MA kurang andal.

### 4. Crossover
| Crossover | Arti umum | Catatan |
|---|---|---|
| Harga memotong MA ke atas/bawah | Perubahan tren jangka periode itu | Paling cepat, paling banyak sinyal palsu |
| MA pendek memotong MA panjang ke atas (misal MA20 × MA50) | Momentum menengah membaik | — |
| **Golden cross**: MA50 memotong MA200 ke atas | Sinyal bullish jangka panjang | Terlambat. Sering muncul setelah harga naik jauh dari dasar |
| **Death cross**: MA50 memotong MA200 ke bawah | Sinyal bearish jangka panjang | Terlambat. Sering muncul setelah harga turun dalam |

### 5. Jarak harga dari MA (overextended)
Harga yang terlalu jauh di atas MA20 atau MA50 (misal jauh melebihi jarak rata-rata saham itu) cenderung mengalami **mean reversion**, yaitu koreksi atau konsolidasi kembali mendekati MA. Ini bukan sinyal jual otomatis, tetapi alasan untuk tidak mengejar harga.

## MA sebagai support & resistance dinamis
- Dalam tren naik kuat, pullback sering tertahan di **MA20** (tren sangat kuat) atau **MA50** (tren normal). Dalam tren turun, pantulan sering tertahan di MA yang sama sebagai resistance.
- **MA200** adalah garis tren besar. Saham yang lama di atas MA200 lalu jatuh ke bawahnya sering menjadikan MA200 sebagai resistance saat retest (role reversal).
- Perlakukan MA sebagai **zona**, bukan garis persis. Harga sering menusuk sedikit sebelum memantul.
- **Konfluensi**: MA yang bertepatan dengan support horizontal, level Fibonacci, atau HVN jauh lebih kuat. Script menandai konfluensi MA20/MA50/MA200 di tabel zona.
- MA dinamis bergeser setiap hari, jadi hitung ulang level entry/stop berbasis MA setiap sesi.

## Moving average per gaya trading
| Gaya | MA yang umum | Catatan |
|---|---|---|
| Scalper / BPJS | EMA 9/20 di chart 1–15 menit, VWAP | MA intraday dihitung per bar, bukan per hari |
| BSJP | MA5, MA20 harian | Close di atas MA5 dan MA20 yang menanjak jadi filter momentum |
| ARA hunter | MA5/MA10 | Harga biasanya sudah jauh di atas semua MA, sehingga MA kurang membantu |
| Swing | MA20, MA50 (atau EMA20) harian | Buy on Weakness di MA20/MA50 dalam susunan bullish |
| Position | MA50, MA200 harian; MA20/MA40 mingguan | Golden/death cross sebagai filter tren besar |
| Investor | MA200 harian, MA mingguan/bulanan | Jarak harga dari MA200 membantu melihat area murah atau mahal secara teknikal |

## Kekhasan pasar Indonesia
- **Data belum adjusted** (stock split, right issue): MA panjang seperti MA200 akan rusak berbulan-bulan jika harga lama tidak disesuaikan.
- **Ex-date dividen**: gap turun menarik MA pendek ke bawah tanpa ada perubahan tren sungguhan. Efeknya lebih besar pada saham dividend yield tinggi.
- **Saham gocap / tidak likuid**: harga tertahan di Rp50 membuat semua MA datar dan saling berimpit, sehingga tidak ada informasi tren.
- **ARA/ARB berjilid**: harga bisa terpisah sangat jauh dari MA dalam beberapa hari. MA baru "mengejar" jauh setelahnya.
- **Libur bursa panjang** (Lebaran, akhir tahun): MA dihitung per hari bursa, jadi celah libur tidak masuk hitungan, tetapi gap setelah libur memengaruhi MA pendek.

## Kelemahan
- **Lagging**: sinyal datang setelah pergerakan dimulai. Golden cross bisa muncul ketika sebagian besar kenaikan sudah terjadi.
- **Whipsaw saat sideways**: harga bolak-balik memotong MA sehingga sinyal palsu beruntun.
- Tidak ada periode "terbaik". Periode populer bekerja sebagian karena banyak orang memakainya.

## Kesalahan umum
- Mencari-cari periode MA yang "pas" di chart historis (overfitting).
- Membeli hanya karena golden cross tanpa melihat jarak harga dan resistance terdekat.
- Memakai crossover MA di pasar sideways.
- Mencampur MA harian dan mingguan tanpa sadar ("MA20 mingguan" ≈ MA100 harian).
- Menganggap MA sebagai garis tepat alih-alih zona.

## Output script
`scripts/sr_levels.py` menampilkan:
- MA5, MA10, MA20, MA50, MA100, MA200 (SMA) dan EMA20, dengan nilai yang dibulatkan ke fraksi harga, jarak harga (%), dan arah slope 5 bar
- Susunan MA20/MA50/MA200 (bullish, bearish, atau campuran)
- Crossover terakhir MA50/MA200 (golden/death cross) dan MA20/MA50 dalam rentang lookback

Pada data intraday dan mingguan, "MA20" berarti 20 bar pada timeframe tersebut.

## Sumber
- [HeyGoTrade — Moving Average: Cara Baca Tren, MA50 vs MA200](https://www.heygotrade.com/id/blog/moving-average-apa-itu/)
- [HeyGoTrade — Cara Menggunakan MA Crossovers](https://www.heygotrade.com/id/blog/cara-menggunakan-ma-crossovers/)
- [Pluang — Moving Average: Pengertian, Jenis, dan Cara Membaca](https://pluang.com/blog/academy/analisis-teknikal-101/memahami-4-indikator-teknikal-lain)
- [HSB — Mengenal Moving Average 10, 20, dan 50](https://blog.hsb.co.id/trading/moving-average-10-20-50/)
- [IDX Channel — Apa Itu MA5, MA10, dan MA20](https://www.idxchannel.com/market-news/apa-itu-ma5-ma10-dan-ma20-dalam-saham-investor-pemula-wajib-paham)
- [Galeri Saham — Beda SMA, EMA, dan WMA](https://galerisaham.com/apa-sih-bedanya-simple-moving-average-sma-exponensial-moving-average-ema-dan-weighted-moving-average-wma/)
