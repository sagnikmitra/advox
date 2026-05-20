export function EmergencyBanner() {
  return (
    <div className="rounded-lg border border-error/30 bg-[#fff5f5] px-6 py-4">
      <p className="text-body-strong text-ink">Emergency flag</p>
      <p className="mt-1 text-caption text-ink-muted-80">
        If this involves immediate harm, threat, arrest, domestic violence, sexual offence, or child safety —
        contact emergency services and a qualified advocate immediately.
      </p>
    </div>
  );
}
