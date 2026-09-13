# MACD (Moving Average Convergence Divergence)

## Arti
MACD adalah indikator **tren sekaligus momentum** yang dikembangkan Gerald Appel. MACD mengukur jarak antara dua EMA: saat EMA pendek menjauh ke atas EMA panjang, momentum naik menguat, dan saat keduanya mendekat (konvergen), momentum melemah. Karena dibangun dari moving average, MACD termasuk indikator **lagging**. Pahami dulu `moving-average.md`.

## Komponen & rumus (setting standar 12, 26, 9)
| Komponen | Rumus | Fungsi |
|---|---|---|
| **MACD line** | EMA12 − EMA26 | Jarak tren pendek vs panjang |
| **Signal line** | EMA9 dari MACD line | Versi halus MACD sebagai pemicu sinyal |
| **Histogram** | MACD line − signal line | Kekuatan dan perubahan momentum |
| **Garis nol** | MACD = 0 | Titik EMA12 = EMA26 |

Beberapa artikel menulis rumusnya terbalik (EMA26 − EMA12). Standarnya **EMA12 − EMA26**, sehingga MACD positif berarti EMA pendek di atas EMA panjang.

Contoh: EMA12 = Rp1.260, EMA26 = Rp1.240 → MACD = **+20**. Jika signal = 15, histogram = **+5** (MACD di atas signal, momentum positif).

**Satuan**: MACD dinyatakan dalam rupiah, jadi nilainya tidak bisa dibandingkan antar saham. MACD +20 pada saham Rp1.250 (1,6%) jauh lebih kuat daripada +20 pada saham Rp9.000 (0,2%). Script juga menampilkan MACD sebagai persen dari harga.

## Cara membaca
### 1. Posisi terhadap garis nol
- **MACD > 0**: EMA12 di atas EMA26, tren pendek naik.
- **MACD < 0**: tren pendek turun.
- **Zero-line crossover**: MACD menembus nol ke atas mengonfirmasi tren naik, ke bawah mengonfirmasi tren turun. Sinyalnya lebih lambat tetapi lebih jarang palsu.

### 2. Crossover signal line
- **MACD memotong signal ke atas** (bullish crossover): momentum membaik.
- **MACD memotong signal ke bawah** (bearish crossover): momentum memburuk.
- Lokasi crossover penting:
  - Bullish crossover **di atas nol** berarti kelanjutan tren naik (lebih kuat).
  - Bullish crossover **jauh di bawah nol** hanya pantulan dalam tren turun (lebih berisiko).
  - Kebalikannya berlaku untuk bearish crossover.

### 3. Histogram
- Histogram **positif dan membesar**: momentum naik menguat. **Positif tapi mengecil**: momentum naik melemah, sering muncul **sebelum** bearish crossover.
- Histogram **negatif dan membesar** (makin dalam): momentum turun menguat. **Negatif tapi mengecil**: tekanan jual melemah, sering muncul sebelum bullish crossover.
- Puncak/lembah histogram biasanya berbalik lebih dulu daripada crossover, sehingga menjadi peringatan dini.

### 4. Divergence
| Jenis | Harga | MACD | Makna |
|---|---|---|---|
| Bullish (regular) | Lower low | Higher low | Momentum turun melemah, potensi pembalikan naik |
| Bearish (regular) | Higher high | Lower high | Momentum naik melemah, potensi pembalikan turun |
| Hidden bullish | Higher low | Lower low | Potensi kelanjutan tren naik |
| Hidden bearish | Lower high | Higher high | Potensi kelanjutan tren turun |

Divergence adalah peringatan, bukan pemicu entry. Tunggu konfirmasi dari crossover, tembusnya swing terdekat, atau candle pembalikan.

## Kombinasi dengan support & resistance
- **Bullish crossover atau histogram berbalik naik tepat di zona support kuat** memberi setup pantulan yang lebih meyakinkan daripada crossover di tengah rentang harga.
- **Breakout resistance + MACD di atas nol + histogram membesar** berarti momentum mendukung breakout.
- **Breakout dengan bearish divergence MACD** (harga high baru, MACD lebih rendah) lebih rawan false breakout.
- **Bearish crossover di resistance** menjadi alasan take profit atau menunda pembelian.
- **Konfluensi dengan RSI**: divergence yang muncul bersamaan di RSI dan MACD pada level support/resistance yang sama lebih bermakna daripada salah satunya.

## MACD vs RSI
| Aspek | MACD | RSI |
|---|---|---|
| Jenis | Tren + momentum (dari EMA) | Momentum murni (gain vs loss) |
| Skala | Tidak terbatas (rupiah) | 0–100 |
| Overbought/oversold | Tidak punya level baku | 70/30 |
| Kecepatan | Lebih lambat, lebih halus | Lebih cepat |
| Paling berguna untuk | Arah & perubahan tren | Kondisi jenuh & divergence jangka pendek |

## Setting per gaya trading
| Gaya | Timeframe | Setting |
|---|---|---|
| Scalper / BPJS | 1–15 menit | 12,26,9 atau setting lebih cepat yang beredar di komunitas (misal 6,13,5). Lebih banyak sinyal palsu |
| BSJP | Harian | 12,26,9, fokus pada histogram yang baru berbalik naik dan crossover di dekat support |
| Swing | Harian | 12,26,9 (standar) |
| Position / investor | Mingguan | 12,26,9 mingguan untuk arah tren besar |

Mengubah setting untuk mencocokkan chart masa lalu mudah berujung overfitting. Setting standar sudah memadai untuk sebagian besar kebutuhan.

## Kekhasan pasar Indonesia
- **ARA/ARB berjilid**: MACD melonjak atau anjlok ekstrem dan histogram baru berbalik beberapa hari setelah puncak/dasar. Sinyal terlambat sangat mahal pada saham gorengan.
- **Gap karena ex-date dividen atau aksi korporasi yang belum adjusted** menciptakan crossover palsu.
- **Saham tidak likuid atau gocap Rp50**: harga datar membuat MACD menempel di sekitar nol tanpa informasi.
- **Data intraday lintas sesi**: MACD 5 menit menggabungkan bar penutupan kemarin dan pembukaan hari ini, sehingga gap pagi bisa memicu crossover yang hanya mencerminkan gap.

## Kelemahan
- **Lagging**: crossover terjadi setelah pergerakan dimulai.
- **Whipsaw saat sideways**: MACD bolak-balik memotong signal di sekitar nol.
- Tidak punya batas overbought/oversold yang baku, sehingga sulit menilai "terlalu jauh".
- Nilai absolut tidak bisa dibandingkan antar saham.

## Kesalahan umum
- Beli setiap bullish crossover tanpa melihat posisi terhadap garis nol dan level harga.
- Mengabaikan histogram yang sudah mengecil sebelum crossover.
- Membandingkan angka MACD antar saham berbeda harga.
- Memakai MACD di saham sideways atau tidak likuid.

## Output script
`scripts/sr_levels.py` menampilkan:
- Nilai MACD, signal, dan histogram (12,26,9), plus MACD dalam % harga
- Posisi MACD terhadap signal dan garis nol
- Arah histogram (membesar/mengecil)
- Crossover signal dan garis nol terakhir beserta tanggal dan jaraknya (bar)
- Divergence MACD dari dua swing low/high terakhir

## Sumber
- [Stockbit Snips — Cara Membaca Indikator MACD](https://snips.stockbit.com/investasi/indikator-macd)
- [HeyGoTrade — Indikator MACD dan Strategi Entry](https://www.heygotrade.com/id/blog/indikator-macd-dan-strategi-entry/)
- [XTB — MACD: Cara Membaca Pergeseran Momentum](https://www.xtb.com/id/education/moving-average-convergence-divergence-cara-membaca-pergeseran-momentum-pasar)
- [Finansialku — Mengenal MACD pada Saham](https://www.finansialku.com/mengenal-indikator-macd-moving-average-convergence-divergence-dalam-trading-saham/)
- [RDIS IDX — Cara Menggunakan Indikator MACD](https://rdis.idx.co.id/id/events/cara-menggunakan-indikator-macd-untuk-analisis-teknikal-apa-itu-macd) (judul terindeks; isi tidak dapat diakses saat riset)
