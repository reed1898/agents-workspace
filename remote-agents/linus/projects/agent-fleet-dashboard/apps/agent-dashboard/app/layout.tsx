import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Agent Fleet Dashboard",
  description: "Operational view of OpenClaw agents"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="mx-auto min-h-screen max-w-6xl px-4 py-6 sm:px-6">
          <header className="mb-8 flex flex-wrap items-center justify-between gap-3">
            <h1 className="text-2xl font-bold">Agent Fleet Dashboard</h1>
            <nav className="flex gap-2 text-sm">
              <Link className="rounded-md bg-slate-800 px-3 py-1.5 hover:bg-slate-700" href="/">
                Overview
              </Link>
              <Link className="rounded-md bg-slate-800 px-3 py-1.5 hover:bg-slate-700" href="/events">
                Events
              </Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
