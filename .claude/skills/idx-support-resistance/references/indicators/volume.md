# Volume

## Arti
**Volume** adalah jumlah saham yang berpindah tangan dalam satu periode (bar). Volume menunjukkan **seberapa besar partisipasi** di balik pergerakan harga. Harga naik dengan partisipasi besar lebih meyakinkan daripada harga naik saat sepi.

Di pasar Indonesia ada tiga ukuran aktivitas yang sering tertukar:
| Ukuran | Arti | Catatan |
|---|---|---|
| **Volume** | Jumlah lembar atau lot yang ditransaksikan | Aplikasi sekuritas umumnya menampilkan **lot** (1 lot = 100 lembar). yfinance memakai **lembar** |
| **Nilai transaksi** | Volume × harga (Rp) | Ukuran likuiditas paling adil antar saham berbeda harga |
| **Frekuensi** | Jumlah transaksi (kali) | Frekuensi tinggi dengan lot kecil per transaksi cenderung ritel. Frekuensi rendah dengan lot besar bisa jadi institusi (heuristik) |

Membandingkan volume BBCA (harga ribuan) dengan saham Rp60 tidak bermakna. Bandingkan **nilai transaksi**, atau volume terhadap rata-rata saham itu sendiri.

## Prinsip dasar: volume mengonfirmasi harga
| Harga | Volume | Interpretasi umum |
|---|---|---|
| Naik | Naik | Kenaikan didukung partisipasi, tren sehat |
| Naik | Turun | Kenaikan melemah, waspada kehabisan pembeli |
| Turun | Naik | Tekanan jual kuat (distribusi atau panic selling) |
| Turun | Turun | Koreksi sepi, sering koreksi sehat dalam tren naik |

## Volume spike
Volume spike adalah volume yang **jauh di atas rata-rata**, misalnya ≥2× rata-rata 20 bar (ambang heuristik; sebagian screener memakai 1,5× atau 3×). Maknanya bergantung pada **lokasi harga**:
- **Saat breakout resistance** → konfirmasi breakout (umumnya dianggap valid jika ≥1,5× rata-rata).
- **Di support setelah penurunan panjang** → bisa **selling climax / kapitulasi**, yaitu penjual terakhir keluar, apalagi jika candle berekor bawah panjang.
- **Di puncak setelah kenaikan panjang** → bisa **buying climax / distribusi**: pemegang besar menjual ke pembeli yang FOMO, apalagi jika candle berekor atas panjang atau close jauh dari high.
- **Karena berita** → cek apakah volume bertahan beberapa hari atau hanya sehari.

## Akumulasi & distribusi
- **Akumulasi**: harga bergerak sideways atau naik perlahan, volume lebih besar di hari naik daripada di hari turun, dan koreksi terjadi dengan volume kecil.
- **Distribusi**: harga sideways di area tinggi, volume lebih besar di hari turun, dan kenaikan terjadi dengan volume kecil.
- **Rasio volume naik/turun**: total volume di bar naik dibagi total volume di bar turun selama 20 bar. Nilai > 1 berarti volume lebih banyak di hari naik.
- **OBV (On-Balance Volume)**: total berjalan volume, ditambah saat close naik dan dikurangi saat close turun. Yang dilihat adalah arahnya, bukan angkanya. OBV naik saat harga naik berarti searah. **OBV turun saat harga naik** adalah divergence bearish: kenaikan tidak didukung volume.

## Volume & support/resistance
- **Volume profile / HVN (High Volume Node)**: area harga dengan volume historis besar. Banyak posisi terbentuk di sana, sehingga area ini cenderung menjadi support atau resistance kuat. **LVN (Low Volume Node)** adalah area sepi yang cenderung dilewati harga dengan cepat.
- **Pantulan di support dengan volume tinggi** lebih kuat daripada pantulan sepi.
- **Support tembus dengan volume besar** lebih mungkin menjadi breakdown sungguhan dan berubah menjadi resistance (role reversal).
- **Retest breakout dengan volume kecil** menandakan tidak ada tekanan jual baru, pertanda baik bagi breakout.

## Kekhasan pasar Indonesia
- **ARA/ARB terkunci**: saat saham ARA, offer habis sehingga volume bisa kecil padahal permintaan besar (antre bid menumpuk). Volume kecil di ARA **bukan** tanda lemah. Sebaliknya, volume kecil di ARB berarti tidak ada pembeli. Lihat juga antrean di `bid-offer.md`.
- **Pasar negosiasi (crossing/blok)**: sebagian sumber data menggabungkan transaksi pasar negosiasi ke volume harian. Transaksi blok besar di luar pasar reguler tidak mencerminkan tekanan beli/jual di order book. Cek rincian pasar reguler vs negosiasi di aplikasi sekuritas jika ada lonjakan tak wajar.
- **Pre-closing & rebalancing indeks** (MSCI, FTSE, LQ45): volume raksasa di penutupan hari rebalancing terjadi karena penyesuaian portofolio, bukan sinyal teknikal biasa.
- **Kode broker & domisili**: sejak 6 Desember 2021, BEI menutup tampilan real-time kode broker dan domisili investor selama jam perdagangan. Sejak 25 Agustus 2025, ringkasan transaksi berdasarkan kode domisili juga didistribusikan di akhir sesi I, selain di akhir hari. Analisis broker summary dan foreign flow jadi hanya bisa dilakukan setelah sesi. Verifikasi status terkini kode broker.
- **Likuiditas minimum**: nilai transaksi rata-rata di bawah ~Rp1 miliar/hari (heuristik skill ini) membuat level teknikal kurang andal dan sulit keluar dalam jumlah besar.
- **Saham gorengan**: volume bisa dipompa lewat transaksi berulang antar pihak terkait. Frekuensi tinggi dengan pola lot seragam di running trade patut dicurigai.

## Volume per gaya trading
| Gaya | Yang diperhatikan |
|---|---|
| Scalper / BPJS | Volume per menit, running trade (lot besar yang HAKA/HAKI), volume 30 menit pertama |
| BSJP | Volume sesi 2 dan pre-closing dibanding rata-rata; close dekat high dengan volume besar |
| ARA hunter | Lonjakan volume >3–5× rata-rata saat mulai naik; perubahan antrean ARA |
| Swing | Konfirmasi breakout ≥1,5×; koreksi dengan volume turun; OBV searah |
| Position / investor | Nilai transaksi untuk ukuran posisi; tren volume mingguan; foreign flow jangka panjang |

**Ukuran posisi vs likuiditas** (heuristik): posisi yang nilainya melebihi porsi kecil dari nilai transaksi harian (misal lebih dari 5–10%) akan sulit dijual cepat tanpa menekan harga.

## Kesalahan umum
- Membandingkan volume antar saham tanpa memperhatikan harga (pakai nilai transaksi).
- Menganggap setiap volume spike sebagai sinyal beli.
- Mengabaikan transaksi negosiasi atau rebalancing yang mengotori data volume.
- Membaca volume ARA/ARB dengan logika hari normal.

## Output script
`scripts/sr_levels.py` menampilkan rata-rata volume 20 dan 50 bar, rasio 20/50 (tren partisipasi), rasio volume bar terakhir, rasio volume naik/turun 20 bar, arah OBV vs harga (dengan tanda divergence), dan daftar volume spike (≥2× rata-rata) dalam 20 bar terakhir. Satuan volume mengikuti sumber data.

## Sumber
- [Reku — Mengenal Volume Saham dan Indikatornya](https://reku.id/en/campus/volume-saham)
- [Invezgo — Volume Spike Saham](https://invezgo.com/blog/volume-spike-saham-cara-mendeteksinya-dengan-screener-invezgo)
- [HeyGoTrade — 7 Pola Volume Saham](https://www.heygotrade.com/id/blog/pola-volume-saham)
- [Nabitu — Penggunaan Volume Transaksi dalam Analisa](https://blog.nabitu.id/penggunaan-volume-transaksi-dalam-analisa-harga-saham/)
- [ANTARA — BEI Resmi Buka Kode Domisili di Akhir Sesi 1](https://www.antaranews.com/berita/5061413/bei-resmi-buka-kode-domisili-di-akhir-sesi-1-perdagangan)
- [Bisnis — BEI Ungkap Rencana Buka Kode Broker & Domisili](https://market.bisnis.com/read/20250616/7/1885231/bei-ungkap-rencana-buka-kode-broker-domisili-investor-menyambut)
