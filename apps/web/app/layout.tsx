import "./globals.css";
import Link from "next/link";
import type { ReactNode } from "react";
import { DisclaimerBar } from "@/components/disclaimer-bar";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-hairline bg-canvas">
          <nav className="page-shell flex items-center justify-between py-4">
            <Link href="/" className="display-serif text-2xl text-ink">Advox</Link>
            <div className="flex gap-4 text-sm text-body">
              <Link href="/ask">Ask</Link>
              <Link href="/advocate">Advocate</Link>
              <Link href="/upload">Upload</Link>
              <Link href="/sources">Sources</Link>
            </div>
          </nav>
        </header>
        <main className="pb-44">{children}</main>
        <DisclaimerBar />
      </body>
    </html>
  );
}
