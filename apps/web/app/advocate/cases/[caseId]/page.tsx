import { DocumentUpload } from "@/components/document-upload";
import { RiskRadar } from "@/components/risk-radar";
import Link from "next/link";

export default function CaseDetailPage({ params }: { params: { caseId: string } }) {
  return (
    <>
      {/* Sub-nav */}
      <div className="sticky top-[44px] z-40 border-b border-hairline bg-canvas-parchment/80 backdrop-blur-xl backdrop-saturate-[180%]">
        <div className="mx-auto flex h-[52px] max-w-content items-center justify-between px-6 md:px-10">
          <p className="text-tagline text-ink">{params.caseId}</p>
          <Link href="/advocate/cases" className="text-btn-utility text-primary hover:underline">
            All cases
          </Link>
        </div>
      </div>

      {/* Hero */}
      <section className="tile-dark">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-on-dark">
            Case: {params.caseId}
          </h1>
        </div>
      </section>

      {/* Content */}
      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-6">
          <RiskRadar />
          <DocumentUpload />
        </div>
      </section>
    </>
  );
}
