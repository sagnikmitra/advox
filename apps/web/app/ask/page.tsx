import { EmergencyBanner } from "@/components/emergency-banner";
import { JurisdictionSelector } from "@/components/jurisdiction-selector";
import { LanguageSelector } from "@/components/language-selector";
import { LegalChat } from "@/components/legal-chat";

export default function AskPage() {
  return (
    <section className="page-shell space-y-6">
      <h1 className="display-serif text-4xl">Layman Legal Assistant</h1>
      <EmergencyBanner />
      <div className="grid gap-3 md:grid-cols-4">
        <LanguageSelector />
        <JurisdictionSelector />
        <input type="date" className="h-10 rounded-md border border-hairline bg-canvas px-3 text-sm" />
        <button className="h-10 rounded-md bg-primary text-sm font-medium text-white">Talk to an advocate</button>
      </div>
      <LegalChat persona="layman" />
      <div className="card">
        <h2 className="text-lg font-medium">Layman output format</h2>
        <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-body">
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
    </section>
  );
}
