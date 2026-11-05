import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MANSI AI — Your AI Companion",
  description: "Meet MANSI AI — your personal AI companion.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}