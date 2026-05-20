"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";

export function NavAuth() {
  const { user, profile, loading, signOut } = useAuth();

  if (loading) return null;

  if (!user) {
    return (
      <div className="flex items-center gap-3">
        <Link href="/login" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
          Sign in
        </Link>
        <Link href="/signup" className="rounded-pill bg-primary/20 px-3 py-1 text-nav-link text-on-dark transition-colors hover:bg-primary/30">
          Sign up
        </Link>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <Link href="/dashboard" className="text-nav-link text-on-dark/80 transition-colors hover:text-on-dark">
        {profile?.full_name || user.email?.split("@")[0] || "Dashboard"}
      </Link>
      {profile?.role === "advocate" && (
        <span className="rounded-pill bg-primary/20 px-2 py-0.5 text-[11px] text-primary">Advocate</span>
      )}
      <button
        onClick={() => signOut()}
        className="text-nav-link text-on-dark/60 transition-colors hover:text-on-dark"
      >
        Sign out
      </button>
    </div>
  );
}
