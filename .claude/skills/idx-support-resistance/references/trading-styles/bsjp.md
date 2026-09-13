# BSJP — Beli Sore Jual Pagi (Overnight Trading)

## Arti
BSJP adalah strategi membeli saham **menjelang penutupan pasar** (akhir sesi 2 atau saat pre-closing) lalu menjualnya **keesokan paginya** saat pre-opening atau di awal sesi 1. Tujuannya menangkap **gap up** atau kenaikan pagi hari. Harapannya, momentum beli yang kuat di sore hari berlanjut saat pasar dibuka.

Karena posisi menginap satu malam, BSJP menanggung **risiko overnight**: berita, pergerakan bursa global, atau harga komoditas malam hari bisa membuat harga dibuka gap down. BSJP populer di kalangan pekerja kantoran karena tidak perlu memantau pasar seharian.

## Profil singkat
| Aspek | BSJP |
|---|---|
| Lama posisi | ±1 malam (sore → pagi berikutnya) |
| Waktu beli | ±14.30–15.49 (akhir sesi 2) atau pre-closing 15.50–16.00 |
| Waktu jual | Pre-opening 08.45–09.00 atau 09.00–10.00 |
| Timeframe chart | Harian (screening) + 15 menit (perilaku sesi terakhir) |
| Target / stop (heuristik umum) | Target ±1–3%, stop di bawah support terdekat |
| Saham cocok | Likuid, volume sore melonjak, close dekat high harian, tren naik |
| Risiko overnight | **Ada**: gap down, berita malam, akhir pekan |

## Kriteria screening yang sering dipakai
Semua kriteria ini heuristik komunitas, bukan jaminan:
- **Volume hari itu di atas rata-rata** (misal ≥1,5× rata-rata 20 hari), terutama volume di sesi 2 atau pre-closing.
- **Close dekat high harian**, yaitu candle bullish dengan ekor atas pendek. Artinya pembeli masih dominan sampai akhir.
- **Breakout resistance harian** dengan close di atas zona, atau **pantulan dari support kuat**.
- **Di atas MA20/MA50** (searah tren).
- **Likuiditas cukup dan spread tipis** agar mudah keluar di pagi hari.
- **Katalis**: berita positif, laporan keuangan, sektor sedang diminati, net buy asing.
- Varian lain: sebagian trader memakai BSJP untuk **rebound** saham yang turun tajam (RSI oversold ditambah candle reversal di support). Risikonya lebih tinggi karena melawan tren.

## Cara pakai support & resistance untuk BSJP
1. **Resistance terdekat di atas close** adalah target realistis untuk pagi hari. Jika jaraknya kurang dari biaya plus target minimum (misal <1,5%), ruang gap up terbatas.
2. **Harga ARA besok** (dihitung dari close hari ini) adalah batas atas absolut. Resistance di atasnya tidak relevan untuk BSJP.
3. **Support terdekat di bawah close** adalah titik invalidasi. Jika pagi dibuka di bawah support ini, keluar dan jangan berharap harga balik.
4. **Close tepat di atas resistance yang baru ditembus** (role reversal) adalah setup favorit, karena resistance lama diharapkan jadi support saat retest pagi.
5. **Hindari membeli tepat di bawah resistance kuat**. Pagi hari, penjual lama di level itu sering langsung melepas barang.
6. **Pivot untuk hari berikutnya** (P, R1, S1) membantu menentukan target pagi dan level cut loss.

Jalankan script dengan data harian (lookback pendek karena fokus pada struktur 3 bulan terakhir):
```bash
python3 scripts/sr_levels.py --csv ANTM.csv --style bsjp
```
Periksa di output: jarak ke R1 (%), batas ARA sesi berikutnya, S1 sebagai titik invalidasi, dan rasio volume bar terakhir terhadap rata-rata 20 hari.

## Mekanisme BEI yang relevan
- **Pre-closing 15.50–16.00 memakai call auction**. Order yang masuk dipertemukan sekaligus untuk membentuk harga penutupan resmi, sehingga harga close bisa berbeda dari harga terakhir sesi 2. Beli di pre-closing berarti membeli di harga penutupan yang belum pasti.
- **Post-trading setelah 16.00**: transaksi di harga penutupan.
- **Pre-opening 08.45–09.00 juga memakai call auction** untuk membentuk harga pembukaan. Menjual di pre-opening memberi eksekusi di harga pembukaan, tetapi harganya belum diketahui pasti saat order dipasang.
- **Batas ARA/ARB** berlaku juga untuk harga pembukaan. Gap down maksimal sebesar batas ARB (15% untuk papan reguler sesuai SK Kep-00003/BEI/04-2025).
- **BSJP hari Jumat berarti menahan posisi 2 malam plus akhir pekan**, sehingga risiko berita lebih besar.
- **Ex-date dividen**: jika besok ex-date, harga pembukaan akan turun sebesar dividen. Cek kalender aksi korporasi.
- **Settlement T+2**: saham yang dibeli sore boleh dijual pagi berikutnya.

## Risiko utama
- **Gap down**: sentimen global (Wall Street, harga komoditas, kurs), berita emiten di malam hari, atau IHSG dibuka merah.
- Harga close "dikerek" di pre-closing (window dressing atau manipulasi), lalu pagi harinya dilepas.
- Target terlalu tinggi sehingga momentum pagi yang singkat terlewat.
- Ramai-ramai BSJP di saham yang sama membuat banyak orang menjual di pagi hari (profit taking serentak).

## Kesalahan umum
- Membeli saham yang sudah naik sangat tinggi atau hampir ARA tanpa melihat resistance dan batas ARA besok.
- Tidak punya rencana jika dibuka gap down, lalu menahan posisi berhari-hari.
- Mengabaikan hari Jumat dan tanggal ex-date.
- Screening hanya dari kenaikan harga tanpa volume.

## Istilah terkait
Gap up/gap down, pre-closing, pre-opening, call auction, closing marubozu, profit taking, window dressing, BPJS (kebalikannya: tutup di hari yang sama), ARA hunter.

## Sumber
- [Boskusaham — Strategi Beli Sore Jual Pagi (BSJP)](https://boskusaham.com/strategi-beli-sore-jual-pagi-bsjp-saham/)
- [Suluah.id — Rahasia "Beli Sore Jual Pagi"](https://www.suluah.id/2025/06/rahasia-beli-sore-jual-pagi-strategi-trading-singkat-yang-bisa-raup-cuan-sebelum-sarapan.html)
- [Pikiran Rakyat — Strategi BSJP: Masih Worth It?](https://potensibisnis.pikiran-rakyat.com/ekbis/pr-6910158488/strategi-bsjp-solusi-cuan-low-effort-buat-kamu-yang-sibuk-masih-worth-it-ga-sih?page=all)
- [Pluang — Jam Bursa Saham Indonesia](https://pluang.com/akademi/berita-analisis/jam-bursa-saham-indonesia)
- [Stockbit Snips — ARA dan ARB Saham](https://snips.stockbit.com/investasi/ara-dan-arb-saham-arti-auto-reject-atas-dan-bawah-serta-batasannya-di-bei)
