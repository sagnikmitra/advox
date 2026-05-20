"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/lib/auth";

export default function SignupPage() {
  const { signUp } = useAuth();
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"layman" | "advocate">("layman");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    const { error: err } = await signUp(email, password, { full_name: fullName, role });
    if (err) {
      setError(err);
      setLoading(false);
    } else {
      setSuccess(true);
      setLoading(false);
    }
  }

  if (success) {
    return (
      <section className="tile-light">
        <div className="mx-auto max-w-[400px] text-center">
          <h1 className="headline-tight text-display-lg text-ink">Check your email.</h1>
          <p className="mt-4 text-lead text-ink-muted-80">
            We sent a confirmation link to <strong>{email}</strong>. Click it to activate your account.
          </p>
          <Link href="/login" className="btn-primary mt-8 inline-block">Go to sign in</Link>
        </div>
      </section>
    );
  }

  return (
    <section className="tile-light">
      <div className="mx-auto max-w-[400px]">
        <h1 className="headline-tight text-display-lg text-ink">Create account.</h1>
        <p className="mt-3 text-lead text-ink-muted-80">
          Join Advox to save conversations, manage cases, and access advocate tools.
        </p>

        <form onSubmit={handleSubmit} className="mt-10 space-y-4">
          <div>
            <label className="text-caption-strong text-ink">Full name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="input-rect mt-1 w-full"
              placeholder="Your full name"
              required
            />
          </div>
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
              placeholder="Minimum 6 characters"
              required
              minLength={6}
            />
          </div>
          <div>
            <label className="text-caption-strong text-ink">I am a</label>
            <div className="mt-2 flex gap-3">
              <button
                type="button"
                onClick={() => setRole("layman")}
                className={role === "layman" ? "chip-selected flex-1" : "chip flex-1"}
              >
                Citizen
              </button>
              <button
                type="button"
                onClick={() => setRole("advocate")}
                className={role === "advocate" ? "chip-selected flex-1" : "chip flex-1"}
              >
                Advocate / Lawyer
              </button>
            </div>
          </div>

          {error && <p className="text-caption text-error">{error}</p>}

          <button type="submit" disabled={loading} className="btn-primary w-full disabled:opacity-50">
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-caption text-ink-muted-48">
          Already have an account?{" "}
          <Link href="/login" className="text-primary hover:underline">Sign in</Link>
        </p>
      </div>
    </section>
  );
}
