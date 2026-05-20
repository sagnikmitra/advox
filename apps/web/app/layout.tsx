import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";
import { DisclaimerBar } from "@/components/disclaimer-bar";

export const metadata = {
  title: "Advox — Indian Legal AI",
  description: "Legal information and procedure workflows for India, built to fail closed.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav className="sticky top-0 z-50 flex h-[44px] items-center justify-between bg-surface-black px-5 md:px-10">
          <div className="flex items-center gap-7">
            <Link href="/" className="font-display text-nav-link font-semibold tracking-tight text-on-dark">
              Advox
            </Link>
            <div className="hidden items-center gap-5 md:flex">
              <Link href="/ask" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Ask
              </Link>
              <Link href="/advocate" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Advocate
              </Link>
              <Link href="/upload" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Upload
              </Link>
              <Link href="/sources" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Sources
              </Link>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/admin/sources" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
              Admin
            </Link>
          </div>
        </nav>
        <main>{children}</main>
        <DisclaimerBar />
        <footer className="bg-canvas-parchment px-6 pb-8 pt-16 md:px-10">
          <div className="mx-auto max-w-content">
            <div className="grid gap-8 text-dense-link md:grid-cols-4">
              <div>
                <p className="text-caption-strong text-ink">Platform</p>
                <Link href="/ask" className="mt-2 block text-ink-muted-80 hover:text-primary">Ask</Link>
                <Link href="/advocate" className="block text-ink-muted-80 hover:text-primary">Advocate</Link>
                <Link href="/upload" className="block text-ink-muted-80 hover:text-primary">Upload</Link>
                <Link href="/sources" className="block text-ink-muted-80 hover:text-primary">Sources</Link>
              </div>
              <div>
                <p className="text-caption-strong text-ink">Advocate Tools</p>
                <Link href="/advocate/research" className="mt-2 block text-ink-muted-80 hover:text-primary">Research</Link>
                <Link href="/advocate/cases" className="block text-ink-muted-80 hover:text-primary">Case Workspaces</Link>
              </div>
              <div>
                <p className="text-caption-strong text-ink">Legal</p>
                <Link href="/disclaimer" className="mt-2 block text-ink-muted-80 hover:text-primary">Disclaimer</Link>
                <Link href="/privacy" className="block text-ink-muted-80 hover:text-primary">Privacy Policy</Link>
              </div>
              <div>
                <p className="text-caption-strong text-ink">Admin</p>
                <Link href="/admin/ingestion" className="mt-2 block text-ink-muted-80 hover:text-primary">Ingestion</Link>
                <Link href="/admin/sources" className="block text-ink-muted-80 hover:text-primary">Source Verification</Link>
              </div>
            </div>
            <div className="mt-12 border-t border-hairline pt-4">
              <p className="text-fine-print text-ink-muted-48">
                Advox provides legal information only. Not a substitute for qualified legal counsel. AI output may contain errors — verify all citations independently.
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
