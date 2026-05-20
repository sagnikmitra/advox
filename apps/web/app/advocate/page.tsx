import { AdvocateWorkspace } from "@/components/advocate-workspace";
import { LegalChat } from "@/components/legal-chat";
import Link from "next/link";

export default function AdvocatePage() {
  return (
    <>
      {/* Sub-nav */}
      <div className="sticky top-[44px] z-40 border-b border-hairline bg-canvas-parchment/80 backdrop-blur-xl backdrop-saturate-[180%]">
        <div className="mx-auto flex h-[52px] max-w-content items-center justify-between px-6 md:px-10">
          <p className="text-tagline text-ink">Advocate</p>
          <div className="flex items-center gap-4">
            <Link href="/advocate/research" className="text-btn-utility text-ink-muted-80 hover:text-primary">
              Research
            </Link>
            <Link href="/advocate/cases" className="text-btn-utility text-ink-muted-80 hover:text-primary">
              Cases
            </Link>
            <Link href="/advocate" className="btn-primary !py-[7px] !px-[18px] !text-caption">
              New workspace
            </Link>
          </div>
        </div>
      </div>

      {/* Hero */}
      <section className="tile-dark">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-on-dark">Advocate Workspace.</h1>
          <p className="mt-3 text-lead text-body-muted">
            Citation-backed research, case prep, and procedural mapping.
          </p>
        </div>
      </section>

      {/* Workspace */}
      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-6">
          <div className="grid gap-3 md:grid-cols-5">
            <input className="input-rect" placeholder="Court" />
            <input className="input-rect" placeholder="Matter type" />
            <input className="input-rect" placeholder="Jurisdiction" />
            <input type="date" className="input-rect" />
            <button className="btn-primary">Create workspace</button>
          </div>

          <LegalChat persona="advocate" />
          <AdvocateWorkspace />
        </div>
      </section>
    </>
  );
}
