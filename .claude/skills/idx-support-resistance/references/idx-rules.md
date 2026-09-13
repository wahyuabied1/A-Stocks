# Aturan Perdagangan BEI yang Relevan untuk Support & Resistance

Ringkasan untuk referensi, diperbarui September 2026. Aturan bursa dapat berubah melalui Surat Keputusan Direksi BEI. Verifikasi di https://www.idx.co.id jika angka ini menentukan kesimpulan.

## Daftar isi
1. Jam perdagangan
2. Satuan perdagangan & harga minimum
3. Fraksi harga (tick size)
4. Auto rejection (ARA/ARB)
5. Papan pencatatan
6. Settlement, trading limit, dan biaya
7. Hal lain yang memengaruhi data harga
8. Sumber

## 1. Jam perdagangan (pasar reguler)
| Fase | Senin–Kamis | Jumat | Mekanisme |
|---|---|---|---|
| Pre-opening | 08.45–09.00 | 08.45–09.00 | Call auction → harga pembukaan |
| Sesi 1 | 09.00–12.00 | 09.00–11.30 | Continuous auction |
| Istirahat | 12.00–13.30 | 11.30–14.00 | — |
| Sesi 2 | 13.30–15.49 | 14.00–15.49 | Continuous auction |
| Pre-closing | 15.50–16.00 | 15.50–16.00 | Call auction → harga penutupan |
| Post-trading | setelah 16.00 | setelah 16.00 | Transaksi di harga penutupan |

Jadwal dapat berbeda saat Ramadan atau pengumuman khusus BEI. Pasar negosiasi beroperasi terpisah untuk transaksi blok.

## 2. Satuan perdagangan & harga minimum
- 1 lot = 100 lembar saham.
- **Harga minimum pasar reguler (Papan Utama, Pengembangan, Ekonomi Baru): Rp50.**
- **Rencana perubahan**: BEI akan menurunkan harga minimum pasar reguler dan tunai menjadi **Rp1**. Target awalnya 7 September 2026, lalu ditunda ke minggu ketiga/keempat September 2026 (paling lambat akhir bulan). Sosialisasi dan uji coba dilakukan 22 & 29 Agustus 2026. **Status per 13 September 2026: belum dipastikan berlaku.** Script menyediakan `--price-rule baru` untuk simulasi.
- Harga acuan ARA/ARB adalah harga penutupan hari bursa sebelumnya (atau harga teoretis setelah aksi korporasi).

## 3. Fraksi harga (tick size)
| Rentang harga | Fraksi | Maks perubahan per order |
|---|---|---|
| < Rp200 | Rp1 | 10 tick |
| Rp200 – < Rp500 | Rp2 | 10 tick |
| Rp500 – < Rp2.000 | Rp5 | 10 tick |
| Rp2.000 – < Rp5.000 | Rp10 | 10 tick |
| ≥ Rp5.000 | Rp25 | 10 tick |

Implikasinya, persentase per tick berbeda antar saham. Saham Rp210 bergerak ±0,95% per tick, sedangkan saham Rp1.990 hanya ±0,25%. Karena itu zona support/resistance minimal harus selebar beberapa tick. Tabel persentase tick terhadap biaya ada di `trading-styles/scalper.md`.

## 4. Auto rejection (ARA/ARB)
### Berlaku saat ini: SK Direksi BEI Kep-00003/BEI/04-2025, efektif 8 April 2025
Papan Utama, Papan Pengembangan, Papan Ekonomi Baru (termasuk ETF & DIRE untuk ARB):
| Harga acuan | ARA | ARB |
|---|---|---|
| Rp50 – Rp200 | 35% | 15% |
| > Rp200 – Rp5.000 | 25% | 15% |
| > Rp5.000 | 20% | 15% |

Papan Pemantauan Khusus (full call auction):
| Harga acuan | ARA / ARB |
|---|---|
| Rp1 – Rp10 | Rp1 (nominal) |
| > Rp10 | 10% simetris |

### Rencana bersamaan dengan harga minimum Rp1 (belum dipastikan berlaku)
| Harga acuan | ARA | ARB |
|---|---|---|
| Rp1 – Rp10 | Rp1 nominal | Rp1 nominal |
| Rp11 – Rp200 | 35% | 15% |
| Rp201 – Rp5.000 | 25% | 15% |
| > Rp5.000 | 20% | 15% |

BEI juga berencana menghapus kriteria Papan Pemantauan Khusus terkait harga rata-rata di bawah Rp51.

### Riwayat ARB (penting untuk membaca data historis)
- Maret 2020: ARB asimetris 7% (pandemi).
- 2023: pelonggaran bertahap.
- 8 April 2025: ARB 15% untuk semua rentang harga (setelah gejolak pasar Maret 2025), bersamaan dengan perubahan ambang trading halt.

Penurunan harian yang tertahan tepat di batas ARB bukan support teknikal, melainkan batas bursa. Pada periode ARB 7%, banyak candle turun beruntun berhenti di batas yang sama.

### Pembulatan
Harga ARA dibulatkan ke bawah sesuai fraksi, harga ARB dibulatkan ke atas, dan ARB tidak boleh di bawah harga minimum papan.

## 5. Papan pencatatan
- **Papan Utama / Pengembangan / Ekonomi Baru**: aturan standar di atas.
- **Papan Akselerasi**: harga minimum Rp1, batas auto rejection lebih sempit (±10% atau nominal untuk harga sangat rendah). Verifikasi rincian terkini.
- **Papan Pemantauan Khusus**: mekanisme full call auction (FCA), harga minimum Rp1. Transaksi terjadi pada lelang periodik, sehingga pola candle dan level teknikal kurang representatif.

## 6. Settlement, trading limit, dan biaya
- **Settlement T+2**. Saham yang dibeli boleh dijual di hari yang sama (day trading) atau hari berikutnya (BSJP) sebelum settlement.
- **Trading limit / fitur day trading**: daya beli melebihi dana tunai (contoh BIONS: 3× dana + 2× portofolio setelah haircut; beberapa aplikasi hingga 7×). Posisi wajib dijual T+0 atau dana dilunasi paling lambat T+2 (contoh Stockbit: pukul 17.00 WIB). Terlambat berakibat denda atau forced sell. Ketentuan berbeda antar sekuritas.
- **Biaya**: beli ±0,15%, jual ±0,25% (termasuk PPh final 0,1% dari nilai jual). Round trip ±0,4%. Jarak entry-stop atau target yang lebih kecil dari biaya praktis tidak bermakna. Fee berbeda antar sekuritas.
- **Pajak dividen**: 10% final untuk individu dalam negeri, dapat dikecualikan jika diinvestasikan kembali sesuai ketentuan.

## 7. Hal lain yang memengaruhi data harga
- **Aksi korporasi** (stock split, reverse split, right issue, bonus, dividen saham): gunakan harga adjusted.
- **Ex-date dividen tunai**: gap turun sebesar dividen.
- **Suspensi & UMA (Unusual Market Activity)**: celah data atau lonjakan tidak wajar.
- **Notasi khusus** (huruf di belakang kode, misal terkait laporan keuangan, ekuitas negatif, PKPU): sinyal risiko fundamental yang dapat membuat level teknikal tidak berlaku.
- **Trading halt pasar**: BEI dapat menghentikan perdagangan jika IHSG turun tajam dalam sehari, sehingga candle hari tersebut terpotong.

## 8. Sumber
- [Stockbit Snips — ARA dan ARB Saham (SK Kep-00003/BEI/04-2025)](https://snips.stockbit.com/investasi/ara-dan-arb-saham-arti-auto-reject-atas-dan-bawah-serta-batasannya-di-bei)
- [Kontan — BEI Tetapkan ARB 15% dan Ubah Batas Trading Halt](https://momsmoney.kontan.co.id/news/bei-tetapkan-auto-rejection-bawah-arb-hanya-15-dan-mengubah-batas-trading-halt-8)
- [Media Indonesia — BEI Siap Turunkan Batas Minimum Harga Saham Jadi Rp1](https://mediaindonesia.com/ekonomi/924027/bei-siap-turunkan-batas-minimum-harga-saham-jadi-rp1-per-7-september-2026)
- [Infobanknews — BEI Tunda Implementasi Harga Minimum Saham Rp1](https://infobanknews.com/gara-gara-ini-bei-tunda-implementasi-harga-minimum-saham-rp1)
- [Berita Moneter — BEI Belum Pastikan Harga Minimum Rp1 Berlaku 7 September](https://beritamoneter.com/bei-belum-pastikan-harga-saham-minimum-rp1-berlaku-7-september/)
- [Pluang — Jam Bursa Saham Indonesia](https://pluang.com/akademi/berita-analisis/jam-bursa-saham-indonesia)
- [BIONS — Trading Limit](https://www.bions.id/edukasi/saham/trading-limit-bni-sekuritas)
- [Stockbit Help — Syarat Trading Limit](https://help.stockbit.com/id/article/trading-limit-apa-saja-syarat-dan-ketentuan-penggunaan-trading-limit-1becv4r/)
