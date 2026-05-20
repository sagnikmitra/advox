import { NextRequest, NextResponse } from "next/server";

const AUTH_USER = process.env.BASIC_AUTH_USER ?? "admin";
const AUTH_PASS = process.env.BASIC_AUTH_PASSWORD ?? "change-me";
const AUTH_ENABLED = (process.env.BASIC_AUTH_ENABLED ?? "false") === "true";

export function middleware(request: NextRequest) {
  if (!AUTH_ENABLED) return NextResponse.next();

  const auth = request.headers.get("authorization");
  if (!auth || !auth.startsWith("Basic ")) {
    return new NextResponse("Authentication required", {
      status: 401,
      headers: { "WWW-Authenticate": 'Basic realm="Secure Area"' }
    });
  }

  const encoded = auth.split(" ")[1] ?? "";
  const decoded = atob(encoded);
  const [user, pass] = decoded.split(":");

  if (user !== AUTH_USER || pass !== AUTH_PASS) {
    return new NextResponse("Invalid credentials", {
      status: 401,
      headers: { "WWW-Authenticate": 'Basic realm="Secure Area"' }
    });
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"]
};
