# BPJS — Beli Pagi Jual Sore (Day Trading / Intraday)

## Arti
BPJS adalah istilah populer di Indonesia untuk **day trading**: membeli saham di pagi hari (setelah pasar buka) dan menjualnya **di hari yang sama** sebelum pasar tutup. Posisi tidak dibawa menginap, jadi tidak ada risiko gap overnight. Keuntungan dicari dari pergerakan harga dalam satu hari.

Bedanya dengan scalper: BPJS menahan posisi menit hingga jam dengan target beberapa persen. Scalper menahan detik hingga menit dengan target 1–2 tick.

## Profil singkat
| Aspek | BPJS / Day trader |
|---|---|
| Lama posisi | Menit – jam, tutup sebelum 16.00 |
| Timeframe chart | 5 – 60 menit, ditambah chart harian untuk konteks |
| Frekuensi | Beberapa transaksi per hari |
| Waktu pantau | Sebagian besar jam bursa |
| Target / stop (heuristik umum) | Target ±1–5%, stop loss ±1–2% |
| Saham cocok | Likuid, volume tinggi, sedang punya momentum atau katalis berita |
| Risiko overnight | Tidak ada |

## Alur harian yang umum
1. **Sebelum 08.45**: siapkan watchlist dari screening sore sebelumnya (volume naik, breakout harian, berita). Tandai support/resistance harian dan intraday.
2. **Pre-opening 08.45–09.00**: amati harga pembukaan terbentuk (gap up atau gap down).
3. **09.00–09.30**: fase paling volatil. Banyak pelaku BPJS menunggu **pullback kecil setelah pembukaan** lalu masuk saat harga memantul di support intraday, atau masuk saat harga menembus high opening range.
4. **Sesi 1 – sesi 2**: kelola posisi. Naikkan stop (trailing) jika harga bergerak sesuai rencana.
5. **Sebelum 15.49**: tutup posisi di sesi continuous. Jangan bergantung pada pre-closing (15.50–16.00) karena harga penutupan ditentukan lewat call auction dan hasilnya sulit dikontrol.
6. **Jumat**: sesi 1 selesai 11.30 dan sesi 2 baru mulai 14.00, jadi waktu trading lebih pendek.

## Cara pakai support & resistance untuk BPJS
Kombinasikan dua lapis level:
- **Lapis harian (konteks)**: support/resistance swing 1–3 bulan dari chart harian. Hindari membeli tepat di bawah resistance harian kuat karena ruang naik sempit.
- **Lapis intraday (eksekusi)**:
  - High/low/close sesi sebelumnya
  - Opening range 30 menit
  - VWAP sesi: pullback yang bertahan di atas VWAP adalah pola yang umum dipakai
  - Pivot harian (P, R1, S1)
  - Cluster swing dari chart 5–15 menit

Jalankan script:
```bash
python3 scripts/sr_levels.py --csv BBRI_5m.csv --style bpjs       # data 5 menit ±5 hari
python3 scripts/sr_levels.py --csv BBRI_harian.csv --style swing  # konteks harian
```

**Rasio risk:reward**: tentukan stop di bawah support intraday (1–2 tick di bawah zona) dan target di resistance terdekat. Jika target lebih kecil dari 1,5–2× jarak stop setelah biaya, lewati setup tersebut.

**Batas ARA/ARB sesi berjalan** dihitung dari close kemarin. Target di atas harga ARA tidak mungkin tercapai hari itu. Saham yang sudah naik 20%+ mendekati ARA punya ruang tersisa yang terbatas.

## Mekanisme BEI yang relevan
- **Settlement T+2**: saham yang dibeli pagi boleh dijual sore di hari yang sama.
- **Fitur day trading / trading limit**: sekuritas bisa memberi daya beli beberapa kali lipat dana tunai. Contohnya BIONS menyebut limit 3× dana ditambah 2× portofolio setelah haircut, dan beberapa aplikasi mengiklankan hingga 7×. Syaratnya posisi harus dijual di hari yang sama (T+0) atau dana dilunasi sebelum T+2. Terlambat dapat berujung denda atau **forced sell**. Leverage memperbesar untung dan rugi.
- **Biaya** round trip ±0,4%. Target 1% hanya menyisakan net ±0,6%.
- **Trading halt**: jika IHSG turun tajam dalam sehari, BEI dapat menghentikan perdagangan sementara, sehingga posisi intraday bisa terkunci.

## Risiko utama
- Whipsaw: harga menembus level lalu berbalik di hari yang sama.
- Leverage day trading yang memaksa jual rugi di akhir hari.
- Overtrading dan balas dendam setelah rugi.
- Saham gorengan bisa ARB dalam hitungan menit setelah naik tajam.
- Biaya kumulatif: 3 transaksi sehari dengan biaya 0,4% setara ±24% modal per bulan (simulasi Stockbit).

## Kesalahan umum
- Masuk pukul 09.00 tepat karena FOMO saat gap up tanpa menunggu konfirmasi.
- Tidak menutup posisi sehingga day trade berubah jadi "investasi terpaksa".
- Mengabaikan resistance harian di dekat harga entry.
- Memakai stop loss yang lebih sempit dari noise normal (lebih kecil dari ATR intraday).

## Istilah terkait
Day trading, intraday, gap up/gap down, opening range, VWAP, trading limit, forced sell, HAKA/HAKI, cut loss, BSJP (kebalikannya: posisi menginap).

## Sumber
- [Ajaib — Beli Saham Pagi-Sore, Strategi Trading Cepat](https://ajaib.co.id/belajar/jadi-trader-handal/strategi-trading-cepat-teknik-beli-saham-pagi-sore)
- [CNBC Indonesia Research — BPJS Bisa Jadi Mesin Uang](https://www.cnbcindonesia.com/research/20250904100154-128-664185/bpjs-bisa-jadi-mesin-uang-bukan-buat-berobat-tapi-buat-cuan)
- [Stockbit Snips — Scalper, Intraday, dan Swing Trader](https://snips.stockbit.com/investasi/scalper-intraday-dan-swing-trader-perbedaan-gaya-trading-saham-dan-cara-memilihnya)
- [BRI Danareksa (BRIGHTS) — Day Trading dan Trading Limit](https://www.brights.id/en/blog/day-trading-dan-trading-limit)
- [BIONS — Trading Limit](https://www.bions.id/edukasi/saham/trading-limit-bni-sekuritas)
- [Stockbit Help — Syarat Trading Limit](https://help.stockbit.com/id/article/trading-limit-apa-saja-syarat-dan-ketentuan-penggunaan-trading-limit-1becv4r/)
- [Pluang — Jam Bursa Saham Indonesia](https://pluang.com/akademi/berita-analisis/jam-bursa-saham-indonesia)
