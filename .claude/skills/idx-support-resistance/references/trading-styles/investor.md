# Investor (Investasi Jangka Panjang)

## Arti
Investor membeli saham sebagai **kepemilikan bisnis jangka panjang**, bertahun-tahun, dengan keputusan utama berbasis **analisis fundamental**: kualitas bisnis, laba, valuasi, dan dividen. Keuntungan datang dari kenaikan nilai perusahaan (capital gain jangka panjang) dan **dividen**. Pergerakan harga harian dan mingguan umumnya diabaikan.

Bagi investor, analisis teknikal seperti support & resistance bersifat **pelengkap**. Gunanya membantu memilih **area akumulasi** yang lebih baik, bukan menentukan kapan jual cepat.

## Tiga gaya investor utama
### Value investing
Mencari saham yang diperdagangkan **di bawah nilai intrinsiknya**: perusahaan bagus yang sedang tidak diminati pasar. Diperkenalkan Benjamin Graham, dianut Warren Buffett, dan di Indonesia dikenal lewat Lo Kheng Hong.
- Metrik umum: PER, PBV, EV/EBITDA rendah dibanding historis atau sektor; neraca sehat; margin of safety.
- Sumber return: harga kembali ke nilai wajar + dividen.

### Growth investing
Membeli perusahaan yang **labanya diperkirakan tumbuh lebih cepat** dari pasar, walaupun valuasinya terlihat mahal saat ini.
- Metrik umum: pertumbuhan pendapatan/laba, ROE, ekspansi pasar, PEG ratio.
- Risiko: valuasi tinggi sensitif terhadap perlambatan pertumbuhan dan kenaikan suku bunga.

### Dividend investing
Fokus pada emiten matang yang **rutin membagi dividen** dengan arus kas stabil.
- Metrik umum: dividend yield, payout ratio, konsistensi dividen bertahun-tahun, arus kas bebas.
- Catatan: harga turun sebesar dividen pada **ex-date**. Membeli sehari sebelum cum-date hanya untuk dividen belum tentu untung setelah pajak dan penurunan harga.

## Profil singkat
| Aspek | Investor |
|---|---|
| Lama kepemilikan | Tahunan |
| Timeframe chart | Mingguan / bulanan |
| Frekuensi | Sangat rendah; akumulasi bertahap |
| Waktu pantau | Laporan keuangan kuartalan, RUPS, berita material |
| Keputusan jual | Fundamental memburuk, valuasi terlalu mahal, ada peluang lebih baik |
| Saham cocok | Fundamental kuat, tata kelola baik, likuid cukup untuk ukuran posisi |

## Cara pakai support & resistance untuk investor
1. **Chart mingguan/bulanan dengan lookback 5–10 tahun.** Level yang bertahan bertahun-tahun (dasar krisis, konsolidasi panjang) paling relevan.
2. **Area akumulasi**: support mayor mingguan, terutama jika bertepatan dengan valuasi murah (misal PBV di dekat batas bawah historis). Konfluensi teknikal dan fundamental adalah sinyal terkuat bagi investor.
3. **Cicil beli (dollar cost averaging / beli bertahap)**: bagi dana ke beberapa tahap di beberapa zona support daripada sekaligus. Jika support pertama jebol, tahap berikutnya di support lebih bawah.
4. **Resistance mayor/all-time high** bukan otomatis sinyal jual. Tetapi jika valuasi sudah jauh di atas rata-rata historis, bisa jadi area mengurangi posisi (take profit sebagian atau rebalancing).
5. **MA200 harian / MA40 mingguan** sebagai gambaran tren jangka panjang. Harga jauh di bawah MA200 bisa berarti peluang value atau tanda masalah fundamental, jadi cek penyebabnya.
6. Investor jarang memakai stop loss teknikal ketat. **Invalidasi utamanya adalah tesis fundamental**, bukan tembusnya satu level.

Jalankan script dengan data mingguan:
```bash
python3 scripts/sr_levels.py --csv BBCA_weekly.csv --style investor
python3 scripts/sr_levels.py --ticker BBCA --style investor   # yfinance 1wk, 10 tahun
```
Pada data mingguan, batas ARA/ARB dan pivot di output kurang relevan untuk investor. Fokus pada zona support/resistance, HVN, dan MA.

## Mekanisme BEI & pajak yang relevan
- **Dividen**: PPh final 10% untuk wajib pajak orang pribadi dalam negeri, dapat dikecualikan jika diinvestasikan kembali di Indonesia dalam jangka waktu dan instrumen sesuai ketentuan (UU Cipta Kerja / HPP). Verifikasi aturan terkini.
- **Jadwal dividen**: cum-date (terakhir berhak), ex-date (harga disesuaikan), recording date, payment date.
- **Right issue**: jika tidak menebus HMETD, kepemilikan terdilusi. Harga teoretis setelah right issue mengubah level teknikal lama, jadi gunakan data adjusted.
- **Stock split / reverse split**: level lama harus disesuaikan rasio split.
- **Buyback**: dapat menjadi support permintaan selama periode buyback.
- **Delisting / Papan Pemantauan Khusus**: risiko terbesar investor jangka panjang pada emiten bermasalah.

## Risiko utama
- **Value trap**: saham terlihat murah karena bisnisnya memang memburuk.
- Membayar terlalu mahal untuk pertumbuhan yang tidak terwujud.
- Konsentrasi berlebihan di satu saham atau sektor.
- Perubahan regulasi, tata kelola buruk, atau aksi korporasi yang merugikan minoritas.
- Likuiditas: saham kecil sulit dijual dalam jumlah besar.

## Kesalahan umum
- Averaging down tanpa mengecek apakah fundamental masih utuh.
- Menganggap support teknikal sebagai "harga murah" tanpa valuasi.
- Mengejar dividend yield tinggi sesaat tanpa melihat keberlanjutan laba.
- Panik jual saat koreksi pasar padahal tesis tidak berubah.

## Istilah terkait
Value investing, growth investing, dividend investing, nilai intrinsik, margin of safety, PER, PBV, ROE, dividend yield, payout ratio, cum-date, ex-date, right issue, HMETD, DCA/cicil beli, averaging down, value trap, buy and hold.

## Sumber
- [Ajaib — Value Investing vs Growth Investing](https://ajaib.co.id/value-investing-vs-growth-investing)
- [OCBC — Value Investing, Metode Lo Kheng Hong](https://www.ocbc.id/id/article/2024/08/09/value-investing-adalah)
- [Stockbit Snips — Jenis Investor Saham: Growth vs Value](https://snips.stockbit.com/investasi/jenis-investor-saham)
- [HeyGoTrade — Saham Dividen vs Growth](https://www.heygotrade.com/id/blog/saham-dividen-vs-growth)
- [Pluang — 3 Jenis Gaya Investasi Saham](https://pluang.com/blog/academy/equity-101/3-jenis-gaya-investasi-saham)
