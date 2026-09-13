# ARA Hunter

## Arti
ARA hunter adalah trader yang **memburu saham yang sedang atau hampir menyentuh Auto Rejection Atas (ARA)**, yaitu batas kenaikan maksimal harian. Harapannya saham berlanjut **ARA berjilid** (ARA beberapa hari berturut-turut) atau dibuka gap up keesokan harinya, sehingga bisa dijual lebih tinggi. Biasanya mereka ikut mengantre beli (bid) di harga ARA atau membeli saat harga mendekati ARA dengan volume melonjak.

Ini gaya **spekulatif berisiko sangat tinggi**. Banyak kandidatnya adalah saham berkapitalisasi kecil, berlikuiditas tipis, atau "gorengan" yang harganya digerakkan kelompok tertentu (bandar). Sumber publik tentang metode ARA hunter terbatas. Isi file ini merangkum praktik komunitas yang umum dan mekanisme bursa, bukan metode resmi.

## Profil singkat
| Aspek | ARA hunter |
|---|---|
| Lama posisi | Beberapa jam – beberapa hari |
| Timeframe chart | Harian + intraday + order book |
| Waktu kunci | Sesi 1 (saham mulai menyala), akhir sesi 2 & pre-closing (antrean ARA bertahan?), pre-opening besok |
| Target | Gap up / ARA lanjutan; keluar cepat saat antrean melemah |
| Stop | Antrean bid ARA dicabut atau jebol → keluar tanpa menunggu |
| Saham cocok | Punya katalis (berita, aksi korporasi, saham baru IPO), volume meledak; hindari yang tidak bisa dijual |
| Risiko | Sangat tinggi: berbalik ke ARB, likuiditas hilang, UMA/suspensi |

## Cara kerja yang umum
1. **Deteksi**: saham naik tajam dengan volume jauh di atas rata-rata (misal >3–5× rata-rata 20 hari), mendekati harga ARA.
2. **Baca antrean**: di harga ARA, sisi offer habis dan antrean bid menumpuk. Antrean bid ARA yang **tebal dan bertambah** menjelang penutupan dianggap sinyal kuat. Antrean yang **menyusut** berarti ada yang mencabut bid atau menjual, tanda bahaya.
3. **Entry**: antre beli di harga ARA (eksekusi hanya jika ada yang menjual) atau beli sebelum ARA saat volume masih masuk.
4. **Exit**: pre-opening atau awal sesi 1 hari berikutnya saat gap up. Keluar cepat jika pembukaan lemah atau antrean ARA hari berikutnya tidak terbentuk.

## Cara pakai support & resistance untuk ARA hunter
- **Harga ARA hari ini adalah resistance absolut** yang ditetapkan bursa, bukan resistance teknikal. Tidak ada transaksi di atasnya.
- **Harga ARA besok** dihitung dari close hari ini. Script menampilkannya di bagian "Batas ARA/ARB". Contoh: saham Rp150 (ARA 35%) bisa naik ke Rp202 besok, sedangkan saham Rp210 (ARA 25%) hanya ke Rp262.
- **Perhatikan perubahan persentase ARA di batas harga**: saham yang menembus Rp200 turun batas ARA-nya dari 35% ke 25%, dan yang menembus Rp5.000 dari 25% ke 20%. Potensi kenaikan per hari mengecil.
- **Resistance historis di atas harga** (swing high lama, area volume besar/HVN) adalah tempat pemegang lama yang nyangkut cenderung menjual. ARA berjilid sering berhenti di sana.
- **Support terdekat di bawah** menunjukkan seberapa dalam harga bisa jatuh jika hype selesai. Pada saham gorengan, penurunan sering melewati beberapa support sekaligus dengan ARB beruntun.
- **Likuiditas historis**: jika rata-rata nilai transaksi sebelum lonjakan sangat kecil, level teknikal hampir tidak bermakna dan risiko tidak bisa keluar tinggi.

Jalankan script dengan data harian (lookback pendek):
```bash
python3 scripts/sr_levels.py --csv XXXX.csv --style ara-hunter
```
Perhatikan peringatan likuiditas, lonjakan harga, dan zona yang ditandai "di luar batas ARA".

## Mekanisme BEI yang relevan
- **ARA** (papan reguler, SK Kep-00003/BEI/04-2025): 35% untuk harga Rp50–Rp200, 25% untuk >Rp200–Rp5.000, 20% untuk >Rp5.000. **ARB 15%** untuk semua rentang.
- **Rencana aturan harga minimum Rp1** (target implementasi September 2026, sempat ditunda dari 7 September): untuk harga Rp1–Rp10, ARA dan ARB menjadi nominal Rp1. Kenaikan Rp1 pada saham Rp2 berarti +50% dalam sehari. Verifikasi status berlakunya di idx.co.id.
- **Papan Pemantauan Khusus (full call auction)**: batas 10% (atau Rp1 untuk harga Rp1–Rp10) dan transaksi hanya lewat lelang periodik. Dinamika antrean ARA berbeda dari pasar continuous.
- **UMA (Unusual Market Activity)**: BEI mengumumkan UMA pada saham dengan kenaikan tidak wajar. Sering diikuti **suspensi**, sehingga dana bisa terkunci.
- **Saham IPO**: sering jadi incaran ARA hunter di hari-hari awal pencatatan. Cek ketentuan batas harga yang berlaku untuk saham baru tercatat.

## Risiko utama
- **ARB berjilid** setelah ARA: bandar distribusi, antrean jual menumpuk di ARB sehingga posisi tidak bisa dijual berhari-hari.
- **Antrean ARA palsu**: bid besar dipasang untuk memancing lalu dicabut.
- **Suspensi** setelah UMA.
- **Pom-pom** di media sosial dan grup chat yang mengarahkan ritel membeli di puncak.
- Masuk papan pemantauan khusus atau notasi khusus.

## Kesalahan umum
- Mengejar saham yang sudah ARA berjilid tanpa melihat resistance historis dan likuiditas.
- Menaruh porsi modal besar di satu saham gorengan.
- Tidak punya aturan keluar saat antrean melemah.
- Mengira saham ARA pasti ARA lagi besok.

## Istilah terkait
ARA berjilid, ARB berjilid, gorengan, bandar, distribusi/akumulasi, antre bid ARA, UMA, suspensi, pom-pom, FOMO, nyangkut, papan pemantauan khusus.

## Sumber
- [Seputarforex — Apa itu ARA Hunter?](https://www.seputarforex.org/artikel/apa-itu-ara-hunter-305100-34) (judul terindeks; isi tidak dapat diakses saat riset)
- [Stockbit Snips — ARA dan ARB Saham](https://snips.stockbit.com/investasi/ara-dan-arb-saham-arti-auto-reject-atas-dan-bawah-serta-batasannya-di-bei)
- [Kontan — BEI Tetapkan ARB 15%](https://momsmoney.kontan.co.id/news/bei-tetapkan-auto-rejection-bawah-arb-hanya-15-dan-mengubah-batas-trading-halt-8)
- [Media Indonesia — BEI Siap Turunkan Batas Minimum Harga Saham Jadi Rp1](https://mediaindonesia.com/ekonomi/924027/bei-siap-turunkan-batas-minimum-harga-saham-jadi-rp1-per-7-september-2026)
- [Infobanknews — BEI Tunda Implementasi Harga Minimum Rp1](https://infobanknews.com/gara-gara-ini-bei-tunda-implementasi-harga-minimum-saham-rp1)
