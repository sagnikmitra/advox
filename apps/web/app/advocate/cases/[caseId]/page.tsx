import { DocumentUpload } from "@/components/document-upload";
import { RiskRadar } from "@/components/risk-radar";

export default function CaseDetailPage({ params }: { params: { caseId: string } }) {
  return (
    <section className="page-shell space-y-6">
      <h1 className="display-serif text-4xl">Case: {params.caseId}</h1>
      <RiskRadar />
      <DocumentUpload />
    </section>
  );
}
