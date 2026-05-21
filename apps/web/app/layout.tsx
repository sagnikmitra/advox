import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";
import { DisclaimerBar } from "@/components/disclaimer-bar";
import { ErrorBoundary } from "@/components/error-boundary";
import { AuthProvider } from "@/lib/auth";
import { NavAuth } from "@/components/nav-auth";

export const metadata = {
  title: "Advox | Legal Intelligence for India",
  description: "AI-powered legal guidance, court directory, and case tracking for Indian law. Verified sources, citation-gated responses, BNS/BNSS/BSA coverage.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
        <nav className="sticky top-0 z-50 flex h-[44px] items-center justify-between bg-surface-black px-5 md:px-10">
          <div className="flex items-center gap-7">
            <Link href="/" className="font-display text-nav-link font-semibold tracking-tight text-on-dark">
              Advox
            </Link>
            <div className="hidden items-center gap-5 md:flex">
              <Link href="/ask" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Ask
              </Link>
              <Link href="/courts" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Courts
              </Link>
              <Link href="/case-search" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Case Search
              </Link>
              <Link href="/advocate" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Advocate
              </Link>
              <Link href="/sources" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
                Sources
              </Link>
            </div>
          </div>
          <NavAuth />
        </nav>
        <ErrorBoundary>
        <main>{children}</main>
        </ErrorBoundary>
        <DisclaimerBar />
        <footer className="bg-canvas-parchment px-6 pb-8 pt-16 md:px-10">
          <div className="mx-auto max-w-content">
            <div className="grid gap-8 text-dense-link md:grid-cols-4">
              <div>
                <p className="text-caption-strong text-ink">Platform</p>
                <Link href="/ask" className="mt-2 block text-ink-muted-80 hover:text-primary">Ask</Link>
                <Link href="/courts" className="block text-ink-muted-80 hover:text-primary">Courts Directory</Link>
                <Link href="/case-search" className="block text-ink-muted-80 hover:text-primary">Case Search</Link>
                <Link href="/sources" className="block text-ink-muted-80 hover:text-primary">Sources</Link>
              </div>
              <div>
                <p className="text-caption-strong text-ink">Advocate Tools</p>
                <Link href="/advocate" className="mt-2 block text-ink-muted-80 hover:text-primary">Workspace</Link>
                <Link href="/advocate/research" className="block text-ink-muted-80 hover:text-primary">Precedent Research</Link>
                <Link href="/advocate/cases" className="block text-ink-muted-80 hover:text-primary">Case Management</Link>
                <Link href="/upload" className="block text-ink-muted-80 hover:text-primary">Document Analyzer</Link>
              </div>
              <div>
                <p className="text-caption-strong text-ink">Account</p>
                <Link href="/login" className="mt-2 block text-ink-muted-80 hover:text-primary">Sign In</Link>
                <Link href="/signup" className="block text-ink-muted-80 hover:text-primary">Create Account</Link>
                <Link href="/dashboard" className="block text-ink-muted-80 hover:text-primary">Dashboard</Link>
              </div>
              <div>
                <p className="text-caption-strong text-ink">Legal</p>
                <Link href="/disclaimer" className="mt-2 block text-ink-muted-80 hover:text-primary">Disclaimer</Link>
                <Link href="/privacy" className="block text-ink-muted-80 hover:text-primary">Privacy Policy</Link>
              </div>
            </div>
            <div className="mt-12 border-t border-hairline pt-4 flex flex-wrap items-center justify-between gap-4">
              <p className="text-fine-print text-ink-muted-48">
                Advox provides legal information only. Not a substitute for qualified legal counsel. AI output may contain errors — verify all citations independently.
              </p>
              <p className="text-fine-print text-ink-muted-48">
                &copy; 2025 Advox. Indian law only.
              </p>
            </div>
          </div>
        </footer>
      </AuthProvider>
      </body>
    </html>
  );
}
