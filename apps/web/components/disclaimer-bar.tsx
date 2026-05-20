import { LEGAL_DISCLAIMER } from "@/lib/constants";

export function DisclaimerBar() {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 border-t border-hairline bg-surface-dark px-4 py-3 text-xs text-canvas md:px-8">
      <p className="mx-auto max-w-6xl whitespace-pre-line">{LEGAL_DISCLAIMER}</p>
    </div>
  );
}
