# Scalper (Scalping)

## Arti
Scalping adalah gaya trading tercepat: membuka dan menutup posisi dalam hitungan **detik hingga menit**, mengincar selisih harga sangat kecil (sering hanya 1–2 tick) tetapi dengan frekuensi transaksi tinggi. Contoh klasik: beli pukul 09.01, jual pukul 09.03 dengan selisih beberapa rupiah per lembar.

## Profil singkat
| Aspek | Scalper |
|---|---|
| Lama posisi | Detik – menit, selalu tutup di hari yang sama |
| Timeframe chart | 1 – 5 menit, ditambah order book (bid/offer) dan running trade |
| Frekuensi | Sangat tinggi (belasan–puluhan transaksi per hari) |
| Waktu pantau | Penuh selama sesi, terutama 30–60 menit pertama |
| Target / stop | 1–2 tick (heuristik umum) |
| Saham cocok | Sangat likuid, antrean bid/offer tebal, spread 1 tick |
| Risiko overnight | Tidak ada (tidak menginap) |

## Masalah utama: biaya vs fraksi harga
Biaya round trip (beli + jual) umumnya sekitar **0,3–0,6%**, tergantung sekuritas. Profit 1 tick hanya bermakna jika persentase tick lebih besar dari biaya. Persentase tick berubah drastis tergantung harga:

| Harga | Fraksi | 1 tick = |
|---|---|---|
| Rp100 | Rp1 | 1,00% |
| Rp199 | Rp1 | 0,50% |
| Rp200 | Rp2 | 1,00% |
| Rp499 | Rp2 | 0,40% |
| Rp500 | Rp5 | 1,00% |
| Rp1.250 | Rp5 | 0,40% |
| Rp1.995 | Rp5 | 0,25% |
| Rp2.000 | Rp10 | 0,50% |
| Rp2.500 | Rp10 | 0,40% |
| Rp4.990 | Rp10 | 0,20% |
| Rp5.000 | Rp25 | 0,50% |
| Rp6.250 | Rp25 | 0,40% |
| Rp10.000 | Rp25 | 0,25% |

Dengan asumsi biaya 0,4%, satu tick kira-kira hanya impas di harga ±Rp1.250, ±Rp2.500, atau ±Rp6.250, dan rugi di atasnya dalam rentang fraksi yang sama. Saham tepat di atas batas fraksi (Rp200–Rp250, Rp500–Rp1.000, Rp2.000–Rp2.500, Rp5.000–Rp6.000) memberi ruang 1 tick yang lebih lebar. Saham harga rendah memang punya tick besar dalam persen, tetapi sering tidak likuid atau "gorengan", jadi pertimbangkan keduanya.

Simulasi Stockbit (modal Rp10 juta, biaya 0,4% per putaran): 15 transaksi sehari dapat memakan beban biaya setara ±120% modal per bulan. Tanpa win rate dan disiplin tinggi, biaya saja bisa menghabiskan modal.

## Cara pakai support & resistance untuk scalper
Level historis jangka panjang kurang relevan. Yang dipakai adalah level **intraday**:
1. **High/low/close sesi sebelumnya**: level paling sering diuji di pagi hari.
2. **Opening range**: high/low 15–30 menit pertama. Breakout dari rentang ini sering jadi pemicu.
3. **VWAP sesi**: harga rata-rata tertimbang volume. Di atas VWAP pembeli dominan, di bawahnya penjual dominan.
4. **Pivot klasik harian** (P, R1, S1) dari sesi sebelumnya.
5. **Antrean tebal di order book**: "tembok" bid/offer berfungsi sebagai support/resistance sangat pendek. Antrean ini bisa dicabut kapan saja, jadi pantau apakah lot di antrean berkurang atau bertambah.
6. **Angka bulat & batas fraksi** (Rp500, Rp1.000, Rp2.000, Rp5.000).

Jalankan script dengan data 1 menit:
```bash
python3 scripts/sr_levels.py --csv BBRI_1m.csv --style scalper
python3 scripts/sr_levels.py --ticker BBRI --style scalper   # yfinance 1m, maks ±7 hari
```
Output intraday menampilkan batas ARA/ARB sesi berjalan, high/low sesi sebelumnya, opening range 30 menit, dan VWAP.

Contoh skenario (edukasi): harga memantul di low sesi kemarin yang bertepatan dengan antrean bid tebal. Entry 1 tick di atas level, target 2 tick di bawah resistance intraday terdekat, keluar segera jika antrean bid dicabut atau harga tembus level.

## Mekanisme BEI yang relevan
- **Jam**: pre-opening 08.45–09.00 (call auction), sesi 1 09.00–12.00 (Jumat s.d. 11.30), sesi 2 13.30–15.49 (Jumat 14.00–15.49), pre-closing 15.50–16.00. Scalping hanya berjalan di sesi continuous auction (sesi 1 dan 2).
- **HAKA (hajar kanan)**: beli langsung di harga offer agar cepat match. **HAKI (hajar kiri)**: jual langsung di harga bid. Scalper sering HAKA saat masuk dan HAKI saat keluar, sehingga membayar spread dua kali.
- **Settlement T+2**: saham yang dibeli hari ini boleh dijual hari ini juga, dengan penyelesaian netting.
- **Trading limit / fitur day trading**: beberapa sekuritas memberi daya beli melebihi dana tunai. Wajib jual di hari yang sama atau lunasi sebelum T+2. Terlambat bisa kena denda atau forced sell. Besaran limit berbeda antar sekuritas.
- **ARA/ARB** tetap membatasi pergerakan harian. Saham yang sudah dekat ARA/ARB sering kehilangan likuiditas di satu sisi antrean.

## Risiko utama
- Biaya transaksi menggerus profit (lihat tabel di atas).
- Slippage saat antrean tipis, sehingga keluar lebih dari 1 tick dari rencana.
- Spoofing: antrean besar yang dipasang lalu dicabut.
- Kelelahan mental dan overtrading.
- Gangguan aplikasi atau jaringan saat pergerakan cepat.

## Kesalahan umum
- Scalping di saham dengan spread lebih dari 1 tick atau volume tipis.
- Tidak menghitung biaya per putaran.
- Menahan posisi rugi "sampai balik" sehingga berubah jadi day trade atau swing tak terencana.
- Menggunakan leverage trading limit tanpa rencana keluar.

## Istilah terkait
HAKA, HAKI, antre bid/offer, running trade, spread, tick, tektok (jual-beli cepat berulang di rentang sempit), cut loss.

## Sumber
- [Stockbit Snips — Scalper, Intraday, dan Swing Trader](https://snips.stockbit.com/investasi/scalper-intraday-dan-swing-trader-perbedaan-gaya-trading-saham-dan-cara-memilihnya)
- [Maybank Sekuritas — 6 Tipe dan Gaya Trading](https://www.maybanktrade.co.id/berita/mau-jadi-trader-saham-kenali-6-tipe-dan-gaya-trading-nya/)
- [Ajaib — HAKI, HAKA, dan Kiat Menerapkannya](https://ajaib.co.id/belajar/jadi-trader-handal/haki-haka-strategi-trading-saham)
- [Pluang — Jam Bursa Saham Indonesia](https://pluang.com/akademi/berita-analisis/jam-bursa-saham-indonesia)
- [BRI Danareksa (BRIGHTS) — Day Trading dan Trading Limit](https://www.brights.id/en/blog/day-trading-dan-trading-limit)
