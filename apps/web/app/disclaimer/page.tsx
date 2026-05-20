import { LEGAL_DISCLAIMER } from "@/lib/constants";

export default function DisclaimerPage() {
  return (
    <section className="page-shell space-y-4">
      <h1 className="display-serif text-4xl">Legal Disclaimer</h1>
      <div className="card whitespace-pre-line text-sm text-body">{LEGAL_DISCLAIMER}</div>
    </section>
  );
}
