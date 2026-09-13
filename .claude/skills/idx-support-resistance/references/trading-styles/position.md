# Position Trader (Position Trading)

## Arti
Position trading menahan posisi **berminggu-minggu hingga berbulan-bulan**, kadang lebih dari setahun, untuk mengikuti **tren besar**. Position trader menggabungkan analisis teknikal (tren jangka panjang) dengan faktor fundamental dan makro: kinerja emiten, siklus sektor, suku bunga, kurs, harga komoditas. Frekuensi transaksinya rendah dan fluktuasi harian diabaikan.

Posisinya di antara swing trader (hari–minggu, lebih teknikal) dan investor (tahunan, lebih fundamental).

## Profil singkat
| Aspek | Position trader |
|---|---|
| Lama posisi | Minggu – bulan (kadang >1 tahun) |
| Timeframe chart | Mingguan (utama) + harian (timing entry) |
| Frekuensi | Rendah (beberapa transaksi per kuartal) |
| Waktu pantau | Mingguan; cek laporan keuangan & berita makro |
| Target / stop | Target di resistance mayor; stop di bawah support mayor atau MA jangka panjang |
| Saham cocok | Tren naik jangka panjang, fundamental membaik, likuid, sektor sedang dalam siklus naik |
| Faktor makro | BI rate, kurs rupiah, harga komoditas (batu bara, nikel, CPO, emas), aliran dana asing, siklus pemilu/kebijakan |

## Cara pakai support & resistance untuk position trader
1. **Gunakan chart mingguan** untuk menentukan tren dan zona mayor. Level yang bertahan bertahun-tahun (misal all-time high atau dasar konsolidasi panjang) paling berbobot.
2. **MA50 dan MA200 harian** (atau MA20/MA40 mingguan) sebagai support dinamis tren. Harga di atas MA200 yang menanjak adalah konteks positif. Golden cross/death cross sering dipakai sebagai filter.
3. **Entry**: breakout dari basis konsolidasi panjang (berbulan-bulan) dengan volume, atau pullback ke support mayor dalam tren naik.
4. **Stop loss lebar**: di bawah support mayor mingguan atau close mingguan di bawah MA jangka panjang. Karena jaraknya lebar, **ukuran posisi (jumlah lot) harus lebih kecil** agar risiko rupiah tetap terkendali.
5. **Target bertahap**: jual sebagian di resistance mayor pertama, lalu sisanya dibiarkan berjalan dengan trailing stop di bawah swing low mingguan.
6. **Level psikologis & all-time high**: saat harga di all-time high tidak ada resistance historis. Gunakan angka bulat, proyeksi, atau trailing stop.

Jalankan script:
```bash
python3 scripts/sr_levels.py --csv ADRO.csv --style position        # harian ±2 tahun, fractal lebar
python3 scripts/sr_levels.py --ticker ADRO --style investor          # konfirmasi di chart mingguan
```

## Faktor fundamental & makro yang sering dipakai
- **Laporan keuangan kuartalan**: pertumbuhan laba, margin, arus kas.
- **Siklus komoditas** untuk saham tambang/energi/perkebunan. Resistance mayor sering bertepatan dengan puncak siklus harga komoditas sebelumnya.
- **Suku bunga BI & kurs**: sensitif untuk perbankan, properti, dan emiten berutang valas.
- **Aliran dana asing (foreign flow)**: net buy/sell asing berkelanjutan sering mendorong tren saham big cap.
- **Rebalancing indeks** (LQ45, IDX30, MSCI/FTSE): masuk atau keluarnya saham dari indeks memengaruhi permintaan.

## Mekanisme BEI yang relevan
- **Aksi korporasi** hampir pasti terjadi selama posisi panjang: dividen, right issue (dilusi), stock split, buyback. Selalu gunakan harga adjusted untuk level lama.
- **Pajak dividen**: 10% final untuk investor individu dalam negeri, bisa dikecualikan jika diinvestasikan kembali di Indonesia sesuai ketentuan.
- **Papan Pemantauan Khusus / notasi khusus**: posisi panjang lebih mungkin menghadapi perubahan status emiten.
- **Libur panjang bursa** tidak terlalu berpengaruh pada horizon ini, tetapi gap besar tetap mungkin terjadi.

## Risiko utama
- Tren berbalik akibat perubahan siklus atau kebijakan.
- Drawdown dalam yang menguji kesabaran, dan stop lebar yang nilainya besar jika tersentuh.
- Opportunity cost: modal tertahan lama di saham sideways.
- Perubahan fundamental emiten (laba anjlok, skandal, gagal bayar).

## Kesalahan umum
- Memakai stop ketat ala swing trader pada posisi jangka panjang.
- Menggunakan chart harian saja sehingga terkecoh noise.
- Mengabaikan siklus komoditas (membeli saham batu bara di puncak harga batu bara).
- Tidak mengecilkan jumlah lot padahal stop jauh lebih lebar.

## Istilah terkait
Trend following, MA200, golden cross/death cross, basis konsolidasi, all-time high, foreign flow, rebalancing indeks, siklus komoditas, trailing stop.

## Sumber
- [Maybank Sekuritas — 6 Tipe dan Gaya Trading](https://www.maybanktrade.co.id/berita/mau-jadi-trader-saham-kenali-6-tipe-dan-gaya-trading-nya/)
- [Dupoin — Cek Gaya Trading, dari Scalper hingga Position Trader](https://www.dupoin.co.id/insights/market-analysis/69523)
- [HeyGoTrade — Trading Style: Arti, Jenis, dan Cara Memilihnya](https://www.heygotrade.com/id/blog/trading-style-adalah/)
- [BIONS — Tipe-Tipe Trader Saham](https://www.bions.id/edukasi/saham/tipe-tipe-trader-saham-sesuaikan-gaya-trading-saham-demi-hasil-yang-lebih-maksimal)
