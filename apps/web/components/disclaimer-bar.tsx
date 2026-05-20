import { LEGAL_DISCLAIMER } from "@/lib/constants";

export function DisclaimerBar() {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-[rgba(255,255,255,0.1)] bg-surface-black/95 px-5 py-3 backdrop-blur-xl md:px-10">
      <p className="mx-auto max-w-content text-micro-legal text-body-muted">{LEGAL_DISCLAIMER}</p>
    </div>
  );
}
