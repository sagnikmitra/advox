"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
  const { signIn } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const { error: err } = await signIn(email, password);
    if (err) {
      setError(err);
      setLoading(false);
    } else {
      router.push("/ask");
    }
  }

  return (
    <section className="tile-light">
      <div className="mx-auto max-w-[400px]">
        <h1 className="headline-tight text-display-lg text-ink">Sign in.</h1>
        <p className="mt-3 text-lead text-ink-muted-80">
          Access your legal workspace and conversation history.
        </p>

        <form onSubmit={handleSubmit} className="mt-10 space-y-4">
          <div>
            <label className="text-caption-strong text-ink">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-rect mt-1 w-full"
              placeholder="you@example.com"
              required
            />
          </div>
          <div>
            <label className="text-caption-strong text-ink">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-rect mt-1 w-full"
              placeholder="••••••••"
              required
              minLength={6}
            />
          </div>

          {error && <p className="text-caption text-error">{error}</p>}

          <button type="submit" disabled={loading} className="btn-primary w-full disabled:opacity-50">
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="mt-6 text-center text-caption text-ink-muted-48">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="text-primary hover:underline">Create one</Link>
        </p>
      </div>
    </section>
  );
}
