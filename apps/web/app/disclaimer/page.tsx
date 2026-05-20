import { LEGAL_DISCLAIMER } from "@/lib/constants";

export default function DisclaimerPage() {
  return (
    <>
      <section className="tile-light">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Legal Disclaimer.</h1>
        </div>
      </section>

      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content">
          <div className="utility-card whitespace-pre-line text-left text-body text-ink-muted-80">
            {LEGAL_DISCLAIMER}
          </div>
        </div>
      </section>
    </>
  );
}
