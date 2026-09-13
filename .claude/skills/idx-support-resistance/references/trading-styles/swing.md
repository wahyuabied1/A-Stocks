# Swing Trader (Swing Trading)

## Arti
Swing trading menahan posisi **beberapa hari hingga beberapa minggu** untuk menangkap satu "ayunan" (swing) harga. Contohnya naik dari support ke resistance dalam tren naik, atau keluar dari fase konsolidasi. Swing trader tidak perlu memantau layar sepanjang hari, sehingga gaya ini sering disebut paling masuk akal untuk pemula dan pekerja kantoran. Dampak biaya transaksinya juga paling ringan di antara gaya trading aktif.

## Profil singkat
| Aspek | Swing trader |
|---|---|
| Lama posisi | Beberapa hari – beberapa minggu (sering 5–20 hari bursa) |
| Timeframe chart | Harian (utama) + mingguan (konteks tren) |
| Frekuensi | Beberapa transaksi per bulan |
| Waktu pantau | Cek sebelum/sesudah bursa atau saat istirahat siang |
| Target / stop | Target di resistance berikutnya; stop di bawah support; risk:reward ≥ 1:2 |
| Saham cocok | Dalam tren naik, keluar dari konsolidasi, likuid, fundamental wajar |
| Risiko overnight | Ada (menginap berhari-hari, termasuk akhir pekan) |
| Indikator umum | MA20/MA50, RSI, MACD, volume |

## Dua teknik entry utama
### Buy on Weakness (BoW)
Membeli saat harga **terkoreksi mendekati support** dalam tren yang masih naik, dengan harapan harga memantul.
- Cocok saat tren besar masih naik dan koreksi terlihat sehat (volume turun saat koreksi).
- Support yang diincar: swing low sebelumnya, MA20/MA50, atau resistance lama yang sudah ditembus (role reversal).
- Stop: tutup harian di bawah zona support.
- Kelebihan: harga lebih murah dan jarak stop dekat. Kekurangan: support bisa jebol, jangan menangkap pisau jatuh.

### Buy on Breakout (BoBr)
Membeli saat harga **menembus resistance** dengan konfirmasi.
- Konfirmasi umum: close harian di atas zona dan volume ≥1,5× rata-rata 20 hari.
- Alternatif lebih aman: tunggu **retest**, yaitu harga kembali menyentuh resistance lama yang kini jadi support lalu memantul.
- Stop: kembali close di bawah zona breakout (breakout gagal atau false breakout).
- Kelebihan: momentum sudah terbukti. Kekurangan: harga entry lebih tinggi dan rawan false breakout.

## Cara pakai support & resistance untuk swing
Support & resistance adalah inti swing trading:
1. **Petakan zona di chart harian** (lookback ±1 tahun) dan periksa tren di chart mingguan.
2. **Entry** di dekat support (BoW) atau setelah breakout resistance (BoBr).
3. **Stop loss** beberapa tick di bawah batas bawah zona support, bukan tepat di level. Harga sering "menusuk" sedikit sebelum memantul. Pastikan jaraknya lebih besar dari noise harian (±0,5–1× ATR14).
4. **Target** di resistance berikutnya (R1). Jika R1 terlalu dekat sehingga risk:reward < 1:2, pertimbangkan R2 atau lewati setup.
5. **Trailing stop**: saat harga menembus R1, R1 bisa menjadi support baru dan stop dinaikkan ke bawahnya.
6. **Konfluensi** membuat level lebih meyakinkan: swing level bertepatan dengan MA50, HVN, atau angka bulat.

Contoh perhitungan dalam lot (edukasi, belum termasuk biaya):
- Entry Rp1.250, stop Rp1.195 (risiko Rp55/lembar), target Rp1.370 (reward Rp120/lembar) → R:R ≈ 1:2,2.
- Jika batas risiko Rp1.000.000 per transaksi: 1.000.000 ÷ (55 × 100) ≈ 18 lot.

Jalankan script:
```bash
python3 scripts/sr_levels.py --csv TLKM.csv --style swing
python3 scripts/sr_levels.py --csv TLKM_weekly.csv --style investor   # cek tren mingguan
```

## Mekanisme BEI yang relevan
- **Menginap berhari-hari** berarti terkena gap dan batas ARB beruntun. Pada skenario terburuk, harga bisa ARB beberapa hari dan stop loss tidak tereksekusi karena antrean jual menumpuk.
- **Akhir pekan & libur bursa panjang** (Lebaran, akhir tahun) menambah risiko gap.
- **Aksi korporasi** selama posisi terbuka (ex-date dividen, right issue, stock split) mengubah harga, jadi gunakan data adjusted.
- **Notasi khusus & Papan Pemantauan Khusus**: emiten yang masuk kategori ini perdagangannya berubah ke full call auction. Level teknikal lama bisa tidak berlaku.
- **UMA & suspensi**: swing trader bisa terjebak jika saham disuspensi.

## Risiko utama
- False breakout dan support jebol.
- Gap down akibat berita atau sentimen global.
- Tren berubah di tengah posisi (koreksi IHSG, rotasi sektor).
- Menunda cut loss sehingga swing berubah jadi investasi terpaksa.

## Kesalahan umum
- Entry di tengah-tengah antara support dan resistance (R:R buruk).
- Stop terlalu ketat sehingga kena noise harian.
- Menganggap setiap sentuhan support pasti memantul tanpa melihat tren mingguan.
- Tidak menyesuaikan target dengan resistance yang jelas terlihat.

## Istilah terkait
Buy on Weakness (BoW), Buy on Breakout (BoBr), retest, pullback, false breakout, trailing stop, risk:reward, trend following, konsolidasi/sideways.

## Sumber
- [Stockbit Snips — Scalper, Intraday, dan Swing Trader](https://snips.stockbit.com/investasi/scalper-intraday-dan-swing-trader-perbedaan-gaya-trading-saham-dan-cara-memilihnya)
- [Maybank Sekuritas — 6 Tipe dan Gaya Trading](https://www.maybanktrade.co.id/berita/mau-jadi-trader-saham-kenali-6-tipe-dan-gaya-trading-nya/)
- [Ajaib — Buy on Weakness vs Buy on Breakout](https://ajaib.co.id/belajar/saham/buy-on-weakness-vs-buy-on-breakout)
- [CGS International — BoW dan BoBr, Mana yang Cocok](https://www.cgsi.co.id/insights/buy-on-weakness-dan-buy-on-breakout-mana-yang-cocok-dengan-gaya-tradingmu?lang=ID)
- [MNC Sekuritas — Breakout atau Buy on Weakness](https://www.mncsekuritas.id/pages/mana-yang-lebih-baik-beli-saham-ketika-breakout-atau-buy-on-weakness/)
