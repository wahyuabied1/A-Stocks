import type { ScannerState } from "@/lib/types";

export default function Notice({ state, error }: { state: ScannerState | null; error: string | null }) {
  if (!state && error) {
    return (
      <div className="notice">
        <b>API Python belum berjalan ({error}).</b>
        <br />
        Jalankan <code>.venv/bin/python -m scanner</code> di folder project (atau <code>./run.sh</code>), lalu muat
        ulang halaman ini.
      </div>
    );
  }
  if (!state) return <div className="notice">Memuat data…</div>;
  return (
    <div className="notice">
      <b>{state.data_note}</b>
      <br />
      {state.disclaimer}
    </div>
  );
}
