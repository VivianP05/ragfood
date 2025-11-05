import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Vivian Pham - AI Data Analyst",
  description: "Digital Twin Portfolio - Ask me about my professional experience, skills, and projects",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
