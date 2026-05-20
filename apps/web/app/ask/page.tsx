import { EmergencyBanner } from "@/components/emergency-banner";
import { JurisdictionSelector } from "@/components/jurisdiction-selector";
import { LanguageSelector } from "@/components/language-selector";
import { LegalChat } from "@/components/legal-chat";
import Link from "next/link";

export default function AskPage() {
  return (
    <>
      {/* Sub-nav */}
      <div className="sticky top-[44px] z-40 border-b border-hairline bg-canvas-parchment/80 backdrop-blur-xl backdrop-saturate-[180%]">
        <div className="mx-auto flex h-[52px] max-w-content items-center justify-between px-6 md:px-10">
          <p className="text-tagline text-ink">Ask</p>
          <Link href="/advocate" className="btn-primary !py-[7px] !px-[18px] !text-caption">
            For advocates
          </Link>
        </div>
      </div>

      {/* Hero */}
      <section className="tile-light">
        <div className="mx-auto max-w-content text-center">
          <h1 className="headline-tight text-display-lg text-ink">Layman Legal Assistant.</h1>
          <p className="mt-3 text-lead text-ink-muted-80">
            Safety-first guidance for common people navigating Indian law.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="bg-canvas-parchment px-6 pb-section pt-12 md:px-10">
        <div className="mx-auto max-w-content space-y-6">
          <EmergencyBanner />

          <div className="grid gap-3 md:grid-cols-4">
            <LanguageSelector />
            <JurisdictionSelector />
            <input type="date" className="input-rect" />
            <Link href="/advocate" className="btn-dark-utility flex items-center justify-center">
              Talk to an advocate
            </Link>
          </div>

          <LegalChat persona="layman" />

          <div className="utility-card text-left">
            <p className="text-body-strong text-ink">Output format</p>
            <ol className="mt-4 list-decimal space-y-1 pl-5 text-caption text-ink-muted-80">
              <li>First, check your safety</li>
              <li>What this situation may legally involve</li>
              <li>What you can do now</li>
              <li>Documents/evidence to keep</li>
              <li>Where to go</li>
              <li>When to contact a lawyer urgently</li>
              <li>What not to do</li>
              <li>Sources used</li>
              <li>Legal disclaimer</li>
            </ol>
          </div>
        </div>
      </section>
    </>
  );
}
