# Bid & Offer (Order Book / Antrean)

## Arti
- **Bid**: harga dan jumlah lot yang **ingin dibeli** investor (antrean pembeli).
- **Offer** (ask): harga dan jumlah lot yang **ingin dijual** investor (antrean penjual).
- **Order book**: daftar semua antrean bid dan offer yang belum tereksekusi.
- **Last price**: harga transaksi terakhir.
- **Spread**: selisih antara offer terendah (best offer) dan bid tertinggi (best bid). Saham likuid biasanya punya spread **1 tick**.

Order book hanya menunjukkan **niat** pembeli dan penjual, bukan transaksi yang sudah terjadi. Antrean bisa diubah atau ditarik kapan saja sebelum tereksekusi.

## Cara membaca order book
Tampilan umum di aplikasi sekuritas:

| Freq | Lot (bid) | **Bid** | **Offer** | Lot (offer) | Freq |
|---|---|---|---|---|---|
| 45 | 12.300 | 1.250 | 1.255 | 8.100 | 30 |
| 60 | 25.000 | 1.245 | 1.260 | 40.500 | 12 |
| 20 | 5.400 | 1.240 | 1.265 | 6.200 | 18 |

- Sisi bid diurutkan dari harga tertinggi ke bawah, sisi offer dari harga terendah ke atas.
- **Lot**: total lot di harga tersebut. **Freq**: jumlah order yang membentuk antrean itu.
- Lot besar dengan freq kecil berarti sedikit order berukuran besar (bisa satu pihak besar). Lot besar dengan freq besar berarti banyak order kecil (ritel).
- Contoh di atas: spread 1 tick (Rp5), dan ada "tembok" offer 40.500 lot di Rp1.260.

## Mekanisme eksekusi di BEI
- **Prioritas harga, lalu waktu**: bid tertinggi dan offer terendah dieksekusi lebih dulu. Di harga yang sama, order yang masuk lebih awal didahulukan. Mengubah order umumnya membuat order kehilangan prioritas waktu.
- **Partial fill**: order bisa terisi sebagian.
- **Limit order**: order dengan harga tertentu (paling umum).
- **Market order** (sejak Desember 2021): order hanya dengan volume, dieksekusi di harga terbaik yang tersedia, dengan mekanisme sisa Fill and Kill (FAK) atau Fill or Kill (FOK).
- **HAKA (Hajar Kanan)**: membeli langsung di harga offer agar langsung match. **HAKI (Hajar Kiri)**: menjual langsung di harga bid.
- **Antre**: memasang bid di bawah offer atau offer di atas bid, lalu menunggu lawan datang. Harganya lebih baik, tapi belum tentu terisi.
- **Fraksi harga** menentukan jarak antar level antrean. Lihat `idx-rules.md` dan tabel persentase tick di `trading-styles/scalper.md`.

## Running trade
Running trade adalah daftar transaksi yang benar-benar terjadi secara real-time (waktu, kode saham, harga, lot).
- Transaksi di **harga offer** berarti pembeli yang agresif (HAKA). Transaksi di **harga bid** berarti penjual yang agresif (HAKI).
- Rangkaian lot besar yang terus memakan offer menunjukkan tekanan beli agresif. Rangkaian lot besar yang terus memakan bid menunjukkan tekanan jual agresif.
- Sejak 6 Desember 2021, **kode broker dan domisili investor tidak ditampilkan real-time** selama perdagangan. Ringkasan domisili tersedia di akhir sesi I (sejak 25 Agustus 2025) dan akhir hari. Analisis "bandar" dari broker summary baru bisa dilakukan setelah sesi.

## Membaca ketebalan antrean
| Pengamatan | Interpretasi umum | Waspada |
|---|---|---|
| Bid jauh lebih tebal dari offer | Minat beli besar, bisa menahan penurunan | Bisa **bid palsu (spoofing)**: ditarik saat harga mendekat |
| Offer jauh lebih tebal dari bid | Tekanan jual besar, bisa menahan kenaikan | Bisa **offer palsu** untuk menakut-nakuti ritel agar menjual murah |
| Tembok offer besar **dimakan** terus | Pembeli agresif menyerap suplai, sinyal kuat | Pastikan terlihat di running trade, bukan hanya offer yang ditarik |
| Tembok bid besar **ditarik** saat harga mendekat | Penopang palsu hilang, rawan turun | — |
| Tembok bid besar **dimakan** terus (HAKI) | Penjual agresif, support intraday jebol | — |
| Antrean berubah drastis dalam hitungan detik | Ada pemain besar yang aktif mengatur antrean | Jangan ambil keputusan dari satu snapshot |

Cara membaca yang lebih rasional:
1. Amati **konsistensi** antrean selama beberapa menit, bukan satu momen.
2. Bandingkan antrean dengan **transaksi nyata** di running trade: yang penting adalah apa yang tereksekusi, bukan apa yang dipajang.
3. Gunakan antrean untuk membaca **tekanan jangka sangat pendek**, bukan tren utama.

**Ciri "fake demand/supply"** yang sering dikaitkan dengan saham gorengan: antrean sangat tidak seimbang, volume transaksi tipis, bid tiba-tiba tebal, lalu diikuti spam order kecil berulang di running trade.

## Pre-opening, pre-closing & IEP/IEV
- Pre-opening (08.45–09.00) dan pre-closing (15.50–16.00) memakai **call auction**. Order dikumpulkan lalu dipertemukan sekaligus.
- **IEP (Indicative Equilibrium Price)**: perkiraan harga pembukaan/penutupan, yaitu harga dengan potensi volume match terbesar berdasarkan antrean saat itu. **IEV (Indicative Equilibrium Volume)**: perkiraan volume yang bisa match di IEP. Keduanya ditampilkan sejak Desember 2021 dan terus berubah selama sesi.
- Selama pengumpulan order, order bisa dimasukkan, diubah, atau ditarik. Saat **random closing** terpicu (menit-menit terakhir sesi call auction), order tidak bisa lagi dimasukkan, diubah, atau ditarik. Mekanisme ini mencegah manipulasi harga penutupan (marking the close).
- IEP bisa "dipoles" lalu berubah di detik terakhir. Jangan anggap IEP sebagai harga final.
- **Papan Pemantauan Khusus (full call auction)**: order book bersifat tertutup (blind). Yang terlihat terutama IEP/IEV.

## Antrean di ARA & ARB
- **Di ARA**: offer habis, bid menumpuk di harga ARA. Ukuran dan **perubahan** antrean bid ARA adalah informasi utama. Antrean yang menebal menjelang penutupan dianggap kuat, sedangkan antrean yang menyusut (bid dicabut atau ada yang menjual ke antrean) adalah tanda bahaya.
- **Di ARB**: bid habis, offer menumpuk di harga ARB. Penjual bisa tidak keluar berhari-hari jika ARB berjilid.

## Kaitan dengan support & resistance
- Tembok bid/offer tebal adalah **support/resistance mikro** (intraday). Level ini paling bermakna jika **bertepatan** dengan zona historis, VWAP, high/low kemarin, atau angka bulat.
- Antrean sering menumpuk di **angka bulat** (Rp500, Rp1.000) dan **batas fraksi** (Rp200, Rp500, Rp2.000, Rp5.000).
- Untuk swing trader dan investor, order book dipakai untuk **eksekusi**: memasang antrean beli di dalam zona support daripada HAKA saat harga lari, dan memperhatikan spread pada saham kurang likuid.

## Bid & offer per gaya trading
| Gaya | Peran order book |
|---|---|
| Scalper | Alat utama: tembok antrean, running trade, spread, prioritas antrean |
| BPJS | Konfirmasi entry di support intraday; memantau antrean saat breakout |
| BSJP | IEP/IEV pre-closing untuk harga beli, IEP pre-opening untuk harga jual |
| ARA hunter | Antrean bid ARA dan perubahannya |
| Swing / position / investor | Eksekusi order limit di zona; hindari saham dengan spread lebar |

## Kesalahan umum
- Percaya "bid tebal = pasti naik" dan "offer tebal = pasti turun".
- Mengambil keputusan dari satu snapshot order book.
- HAKA di saham ber-spread lebar, sehingga langsung rugi beberapa tick.
- Menganggap IEP pre-closing sebagai harga penutupan pasti.
- Overtrading karena terpaku pada perubahan antrean detik demi detik.

## Sumber
- [Stockbit Snips — Bid dan Offer Saham](https://snips.stockbit.com/investasi/bid-offer-saham)
- [Bareksa — Apa Itu Antrian Bid & Offer dan Cara Membacanya](https://www.bareksa.com/berita/saham/2026-01-08/apa-itu-antrian-bid-offer-saham-dan-cara-membacanya)
- [Ajaib — Cara Membaca Ketebalan Bid dan Offer untuk Scalping](https://ajaib.co.id/belajar/investasi/cara-membaca-ketebalan-bid-dan-offer)
- [Pasbana — Membaca Orderbook Saham](https://www.pasbana.com/2026/01/membaca-orderbook-saham-cara-melihat-medan-perang-bandar-dan-retail-secara-real-time.html)
- [Invezgo — Cara Membaca Bid dan Offer untuk Entry Intraday](https://invezgo.com/id/blog/cara-membaca-bid-dan-offer-saham-untuk-entry-intraday)
- [KB Valbury — Mekanisme IEP dan IEV](https://www.kbvalbury.com/iep-and-iev-mechanism-en)
- [Kompas — Pre-Opening, Pre-Closing, Random Closing, Market Order](https://money.kompas.com/read/2021/12/17/071500526/istilah-baru-sistem-perdagangan-di-bei--apa-itu-mekanisme-pre-opening-pre?page=all)
- [ANTARA — BEI Resmi Buka Kode Domisili di Akhir Sesi 1](https://www.antaranews.com/berita/5061413/bei-resmi-buka-kode-domisili-di-akhir-sesi-1-perdagangan)
