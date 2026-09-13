# RSI (Relative Strength Index)

## Arti
RSI adalah indikator **momentum** yang dikembangkan J. Welles Wilder. RSI mengukur kecepatan dan besarnya kenaikan dibanding penurunan harga dalam periode tertentu, dengan skala **0–100**. RSI tidak memprediksi harga. RSI hanya menunjukkan apakah dorongan beli atau jual sedang menguat atau melemah.

## Rumus
1. Hitung perubahan close tiap bar: kenaikan (gain) dan penurunan (loss).
2. Rata-rata gain dan rata-rata loss selama *n* bar (default **14**), lalu dihaluskan dengan metode Wilder:
   `avg_gain_baru = (avg_gain_lama × 13 + gain_hari_ini) / 14`
3. `RS = avg_gain / avg_loss`
4. `RSI = 100 − 100 / (1 + RS)`

Contoh: rata-rata gain Rp20 dan rata-rata loss Rp10 → RS = 2 → RSI = 100 − 100/3 = **66,7**.

## Cara membaca
| Nilai RSI | Makna umum | Catatan |
|---|---|---|
| > 70 | Overbought (jenuh beli) | Kenaikan sudah cepat. Bukan otomatis sinyal jual |
| 50 – 70 | Momentum positif | Pembeli dominan |
| 50 | Garis tengah | Sering dipakai sebagai konfirmasi arah tren |
| 30 – 50 | Momentum negatif | Penjual dominan |
| < 30 | Oversold (jenuh jual) | Penurunan sudah cepat. Bukan otomatis sinyal beli |

**Pergeseran rentang (range shift)**: dalam tren naik kuat, RSI sering bergerak di kisaran 40–80 dan jarang turun di bawah 40. Dalam tren turun, RSI bergerak di kisaran 20–60. Di uptrend kuat, RSI bisa bertahan di atas 70 berminggu-minggu sementara harga terus naik, sehingga menjual hanya karena "overbought" berarti melewatkan sebagian besar kenaikan.

## Divergence
Divergence terjadi saat arah harga dan arah RSI tidak sejalan. Bandingkan **dua swing terakhir**:

| Jenis | Harga | RSI | Makna |
|---|---|---|---|
| Bullish (regular) | Lower low | Higher low | Tekanan jual melemah, potensi pembalikan naik |
| Bearish (regular) | Higher high | Lower high | Tekanan beli melemah, potensi pembalikan turun |
| Hidden bullish | Higher low | Lower low | Koreksi dalam tren naik, potensi kelanjutan naik |
| Hidden bearish | Lower high | Higher high | Pantulan dalam tren turun, potensi kelanjutan turun |

Divergence adalah **peringatan dini, bukan pemicu entry**. Harga bisa terus bergerak searah tren sambil membentuk beberapa divergence berturut-turut. Tunggu konfirmasi: harga menembus swing terdekat, candle pembalikan, atau RSI kembali melewati 50.

## Kombinasi dengan support & resistance
Kekuatan RSI muncul saat digabung dengan level harga:
- **RSI oversold + harga di support kuat + candle pembalikan** adalah setup Buy on Weakness yang umum.
- **Bullish divergence tepat di zona support** lebih bermakna daripada divergence di tengah-tengah rentang harga.
- **Bearish divergence di resistance** menjadi alasan untuk berhati-hati sebelum membeli dekat resistance atau untuk take profit.
- **Breakout resistance dengan RSI > 50 dan naik** menunjukkan momentum mendukung. Breakout dengan RSI yang sudah bearish divergence lebih rawan false breakout.
- **Failure swing**: RSI gagal melewati puncak RSI sebelumnya lalu menembus lembah RSI terakhir. Ini sinyal momentum yang tidak bergantung pada angka 70/30.

## Periode per gaya trading
| Gaya | Timeframe | Periode yang umum |
|---|---|---|
| Scalper / BPJS | 1–15 menit | RSI 7–9 (lebih sensitif) atau 14 |
| BSJP | Harian + 15 menit sesi terakhir | RSI 14 |
| Swing | Harian | RSI 14 (sebagian memakai 21 agar lebih halus) |
| Position / investor | Mingguan | RSI 14 mingguan |

Periode pendek memberi sinyal lebih banyak tetapi lebih banyak sinyal palsu. Periode panjang lebih halus tetapi lebih lambat.

## Kekhasan pasar Indonesia
- **ARA/ARB berjilid**: saham yang ARA beberapa hari beruntun bisa punya RSI di atas 90, dan saham ARB beruntun bisa di bawah 10. Pada kondisi terkunci ini, RSI tidak berguna untuk timing karena antrean dan bursa yang menentukan harga, bukan momentum normal.
- **Saham gorengan / tidak likuid**: hari tanpa transaksi (close sama) membuat RSI datar atau melompat, sehingga sinyal kurang bermakna.
- **Data belum adjusted** (stock split, right issue) membuat perubahan harga palsu yang merusak perhitungan RSI selama beberapa minggu.
- **Ex-date dividen**: gap turun sebesar dividen menurunkan RSI tanpa ada tekanan jual sungguhan.
- **Tick besar pada saham harga rendah**: pada saham Rp50–Rp100, satu tick setara 1–2%, sehingga RSI di timeframe kecil sangat berisik.

## Kesalahan umum
- Jual hanya karena RSI > 70 atau beli hanya karena RSI < 30 tanpa melihat tren dan level harga.
- Menganggap setiap divergence sebagai pembalikan pasti.
- Membandingkan RSI antar timeframe secara campur aduk.
- Memakai RSI di saham yang sedang ARA/ARB berjilid atau disuspensi.

## Output script
`scripts/sr_levels.py` menampilkan RSI(14) terakhir, zonanya, nilai 5 bar sebelumnya (arah momentum), dan divergence dari dua swing low/high terakhir beserta tanggal dan jaraknya (bar). Divergence yang terjadi puluhan bar lalu kurang relevan untuk gaya jangka pendek.

## Sumber
- [HeyGoTrade — Cara Menggunakan RSI Saham](https://www.heygotrade.com/id/blog/cara-menggunakan-rsi-saham/)
- [Pluang — Cara Membaca RSI Trading](https://pluang.com/akademi/berita-analisis/cara-membaca-rsi-trading)
- [HSB Investasi — RSI Divergence](https://blog.hsb.co.id/trading/rsi-divergence/)
- [XTB — Indikator RSI untuk Pemula](https://www.xtb.com/id/education/indikator-rsi-untuk-pemula-mengenali-kondisi-overbought-dan-oversold)
- [Dupoin — Indikator RSI: Dasar dan Fungsi](https://www.dupoin.co.id/insights/market-analysis/60626)
