# Candlestick

## Arti
Candlestick adalah cara menampilkan harga dalam satu periode (1 menit, 1 hari, 1 minggu) dalam bentuk "lilin" yang merangkum **empat harga**: open, high, low, dan close. Teknik ini berasal dari pedagang beras Jepang abad ke-18. Pola candlestick adalah bagian dari **price action**: membaca perilaku pembeli dan penjual langsung dari bentuk harga, bukan dari indikator turunan.

Candlestick menunjukkan **siapa yang menang dalam periode itu dan seberapa meyakinkan**. Pola candlestick sendirian tidak cukup untuk mengambil keputusan. Maknanya bergantung pada **lokasi** (dekat support/resistance), **tren sebelumnya**, **volume**, dan **konfirmasi** candle berikutnya.

## Anatomi
```
        │  ← upper shadow (ekor atas): high − max(open, close)
      ┌─┴─┐
      │   │ ← body: jarak open ↔ close
      │   │
      └─┬─┘
        │  ← lower shadow (ekor bawah): min(open, close) − low
```
- **Candle naik (hijau/putih)**: close > open. Body bawah = open, body atas = close.
- **Candle turun (merah/hitam)**: close < open. Body atas = open, body bawah = close.
- Sebagian aplikasi mewarnai candle berdasarkan **close vs close kemarin**, bukan close vs open. Candle bisa berwarna hijau padahal close < open jika harga tetap di atas close kemarin (terjadi saat gap up). Cek pengaturan chart.

## Membaca bentuk dasar
| Bentuk | Arti |
|---|---|
| Body panjang | Satu pihak mendominasi sepanjang periode |
| Body kecil (spinning top) | Tarik-menarik seimbang, momentum melemah |
| Ekor atas panjang | Harga sempat naik tapi ditolak, ada penjual di atas |
| Ekor bawah panjang | Harga sempat turun tapi ditolak, ada pembeli di bawah |
| Tanpa ekor (marubozu) | Satu pihak menguasai dari open sampai close |
| Open ≈ close (doji) | Keraguan; pembeli dan penjual seimbang |

## Pola satu candle
| Pola | Ciri | Lokasi bermakna | Bias |
|---|---|---|---|
| **Hammer** | Body kecil di atas, ekor bawah ≥2× body, ekor atas sangat pendek | Setelah turun / di support | Bullish |
| **Hanging man** | Bentuk sama dengan hammer | Setelah naik / di resistance | Bearish (lemah, butuh konfirmasi) |
| **Inverted hammer** | Body kecil di bawah, ekor atas ≥2× body | Setelah turun / di support | Bullish (butuh konfirmasi) |
| **Shooting star** | Bentuk sama dengan inverted hammer | Setelah naik / di resistance | Bearish |
| **Doji** | Body sangat tipis (≤10% range) | Setelah tren panjang / di level kunci | Netral, tanda keraguan |
| Dragonfly doji | Doji dengan ekor bawah panjang | Di support | Condong bullish |
| Gravestone doji | Doji dengan ekor atas panjang | Di resistance | Condong bearish |
| **Marubozu** | Body ≥90% range, hampir tanpa ekor | Breakout / breakdown | Searah warna (kuat) |
| Spinning top | Body kecil, ekor atas dan bawah seimbang | Setelah tren | Netral, momentum melemah |

## Pola dua candle
| Pola | Ciri | Bias |
|---|---|---|
| **Bullish engulfing** | Candle naik yang body-nya menelan body candle turun sebelumnya | Bullish (di support/setelah turun) |
| **Bearish engulfing** | Candle turun yang body-nya menelan body candle naik sebelumnya | Bearish (di resistance/setelah naik) |
| **Bullish harami** | Candle kecil di dalam body candle turun besar sebelumnya | Tekanan jual melemah, butuh konfirmasi |
| **Bearish harami** | Candle kecil di dalam body candle naik besar sebelumnya | Tekanan beli melemah, butuh konfirmasi |
| **Piercing line** | Setelah candle turun, candle naik yang close di atas tengah body sebelumnya | Bullish |
| **Dark cloud cover** | Setelah candle naik, candle turun yang close di bawah tengah body sebelumnya | Bearish |
| Tweezer bottom / top | Dua candle dengan low (atau high) hampir sama | Support/resistance mikro ditolak dua kali |

## Pola tiga candle
| Pola | Ciri | Bias |
|---|---|---|
| **Morning star** | Candle turun besar → candle body kecil → candle naik yang close melewati tengah candle pertama | Bullish reversal |
| **Evening star** | Candle naik besar → candle body kecil → candle turun yang close di bawah tengah candle pertama | Bearish reversal |
| **Three white soldiers** | Tiga candle naik beruntun, close makin tinggi, ekor atas pendek | Tren naik kuat |
| **Three black crows** | Tiga candle turun beruntun, close makin rendah, ekor bawah pendek | Tren turun kuat |

## Gap
Gap adalah celah harga antara candle hari ini dan kemarin: **gap up** jika low hari ini di atas high kemarin, dan **gap down** jika high hari ini di bawah low kemarin. Sebagian trader juga menyebut "gap" untuk open di atas high kemarin, walaupun celahnya tertutup di hari yang sama. Celah yang belum tertutup lebih bermakna.
- Di BEI, gap terbentuk di **pre-opening (08.45–09.00)** saat harga pembukaan ditentukan lewat call auction, biasanya karena berita, sentimen global, atau antrean besar.
- Jenis gap:
  - **Common gap**: kecil, sering tertutup kembali.
  - **Breakaway gap**: keluar dari konsolidasi dengan volume besar, awal tren baru.
  - **Runaway gap**: di tengah tren, tanda kelanjutan.
  - **Exhaustion gap**: di akhir tren panjang, lalu harga berbalik.
- Gap **tidak selalu ditutup**. Area gap sering menjadi support (gap up) atau resistance (gap down) saat diuji kembali.
- **Gap karena ex-date dividen** bukan sinyal teknikal.

## Konteks lebih penting daripada bentuk
Urutan penilaian yang disarankan:
1. **Lokasi**: apakah candle terbentuk di zona support/resistance, MA penting, atau level Fibonacci? Hammer di tengah rentang harga hampir tidak bermakna. Hammer tepat di support kuat jauh lebih bermakna.
2. **Tren sebelumnya**: pola pembalikan butuh tren yang mau dibalik. "Hammer" setelah harga naik adalah hanging man.
3. **Volume**: pola pembalikan dengan volume di atas rata-rata lebih meyakinkan.
4. **Konfirmasi**: candle berikutnya bergerak searah sinyal, misalnya close di atas high hammer.
5. **Timeframe**: pola di chart harian/mingguan lebih berbobot daripada chart 1–5 menit.

Contoh skenario (edukasi): harga turun ke zona support Rp1.190–Rp1.250 yang bertepatan dengan Fib 61,8% dan MA50. Terbentuk bullish engulfing dengan volume 1,8× rata-rata dan RSI bullish divergence. Keesokan harinya close di atas high engulfing. Konfluensi seperti ini jauh lebih kuat daripada engulfing sendirian.

## Kekhasan pasar Indonesia
- **Candle ARA**: candle naik panjang dengan **close tepat di harga ARA** dan biasanya tanpa ekor atas. Volume bisa besar, atau kecil jika offer habis sejak pagi.
- **ARA sejak pembukaan**: open = high = low = close di harga ARA, sehingga candle berbentuk garis mendatar tanpa body. Artinya permintaan jauh melebihi penawaran sepanjang hari, bukan "doji keraguan".
- **Sempat ARA lalu turun** (ekor atas panjang di harga ARA): antrean ARA gagal bertahan, sering dibaca sebagai distribusi, mirip shooting star.
- **Candle ARB**: candle turun panjang dengan close di harga ARB. ARB sejak pembukaan juga berbentuk garis tanpa body. **Sempat ARB lalu pulih** (ekor bawah panjang): ada pembeli di batas bawah.
- **Harga close ditentukan pre-closing (15.50–16.00, call auction dengan random closing)**: close bisa melompat beberapa tick dari harga sesi 2, sehingga body dan ekor candle harian ikut berubah. Candle yang "dikerek" di pre-closing perlu diwaspadai, terutama pada saham tidak likuid.
- **Fraksi harga**: pada saham harga rendah (Rp50–Rp200), selisih 1 tick sudah 0,5–2%, sehingga banyak candle berbody 0–1 tick terlihat seperti doji. Doji di saham ini kurang bermakna.
- **Saham gocap** yang tertahan di Rp50 membentuk deretan candle datar tanpa informasi.
- **Candle intraday**: jeda siang (12.00–13.30, Jumat 11.30–14.00) dan jeda antarhari menciptakan gap di chart menit yang bukan gap sungguhan dalam arti harian.
- **Candle mingguan** di BEI berakhir hari Jumat. Libur bursa membuat candle mingguan berisi kurang dari 5 hari.

## Candlestick per gaya trading
| Gaya | Timeframe candle | Fokus |
|---|---|---|
| Scalper | 1 menit | Candle ekor panjang di tembok antrean, marubozu saat breakout opening range |
| BPJS | 5–15 menit + harian | Hammer/engulfing di support intraday atau VWAP; candle harian kemarin sebagai konteks |
| BSJP | Harian (candle hari ini saat sore) | Close dekat high (marubozu bullish, tanpa ekor atas panjang); hindari shooting star atau ekor atas panjang |
| ARA hunter | Harian | Candle ARA vs "sempat ARA lalu turun"; bentuk candle hari berikutnya |
| Swing | Harian | Pola pembalikan di zona S/R dengan konfirmasi |
| Position / investor | Mingguan | Engulfing/hammer mingguan di support mayor; marubozu mingguan saat breakout basis |

## Kesalahan umum
- Menghafal nama pola tanpa melihat lokasi dan tren.
- Entry langsung saat pola terbentuk tanpa menunggu konfirmasi.
- Membaca candle intraday yang belum selesai sebagai pola final. Candle harian baru final setelah pre-closing.
- Menganggap candle ARA sejak open (tanpa body) sebagai doji.
- Mengabaikan volume dan data belum adjusted (gap palsu karena aksi korporasi).

## Output script
`scripts/sr_levels.py` memindai **3 bar terakhir** dan melaporkan pola yang terdeteksi beserta:
- bias (bullish/bearish/netral)
- tren 5 bar sebelumnya
- zona support/resistance yang sedang diuji candle tersebut
- volume dibanding rata-rata 20 bar

Definisi yang dipakai (heuristik, bisa berbeda dari platform lain):
- **Doji**: body ≤10% range
- **Hammer / shooting star**: ekor ≥2× body dan ≥60% range, ekor sisi lain pendek. Nama hammer vs hanging man (atau inverted hammer vs shooting star) ditentukan dari tren 5 bar sebelumnya
- **Marubozu**: body ≥90% range
- **Engulfing, harami, piercing/dark cloud, morning/evening star, three white soldiers/black crows**: sesuai ciri di tabel di atas
- **Gap**: low di atas high bar sebelumnya (gap up) atau high di bawah low bar sebelumnya (gap down), yaitu celah yang belum tertutup di bar itu; tidak dihitung untuk data intraday
- **Morning/evening star**: candle pertama berbody ≥50% range, candle tengah berbody ≤30% candle pertama dan berada di bawah (morning) atau di atas (evening) close candle pertama, lalu candle ketiga close melewati tengah body candle pertama
- **Candle ARA/ARB**: close atau high/low menyentuh batas auto rejection yang dihitung dari close kemarin (khusus data harian)

Pola yang tidak menguji zona S/R ditandai "tidak di dekat zona S/R terdeteksi", jadi beri bobot lebih kecil.

## Sumber
- [HeyGoTrade — Pola Candlestick: Arti, Jenis, dan Cara Membacanya](https://www.heygotrade.com/id/blog/pola-candlestick-adalah/)
- [Pluang — Pola Candlestick Lengkap](https://pluang.com/akademi/berita-analisis/pola-candlestick-lengkap)
- [Pluang — Candlestick Saham: Panduan Pola ARA ARB](https://pluang.com/akademi/berita-analisis/candlestick-saham-panduan-pola-ara-arb)
- [Pluang — Memahami Ragam Pola Candlestick](https://pluang.com/blog/academy/analisis-teknikal-101/memahami-ragam-pola-candlestick)
- [Stockbit Snips — Cara Membaca Grafik Candlestick Saham](https://snips.stockbit.com/investasi/cara-membaca-grafik-candlestick-saham-traders-simak)
- [Ajaib — Cara Membaca Pola Candlestick Saham](https://ajaib.co.id/belajar/saham/macam-macam-grafik-candlestick-dalam-dunia-trading)
- [Ajaib — Gap Saat Trading](https://ajaib.co.id/belajar/analisa-fundamental-saham/gap-saat-trading)
- [StockCharts ChartSchool — Introduction to Candlesticks](https://chartschool.stockcharts.com/table-of-contents/chart-analysis/candlestick-charts/introduction-to-candlesticks)
