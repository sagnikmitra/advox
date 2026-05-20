import { CitationPanel } from "./citation-panel";
import { RiskRadar } from "./risk-radar";
import { SourceViewer } from "./source-viewer";

export function AdvocateWorkspace() {
  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="space-y-6 lg:col-span-2">
        <RiskRadar />
        <SourceViewer />
      </div>
      <CitationPanel />
    </div>
  );
}
