import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { PropsWithChildren } from "react";
import { ToastContainer } from "react-toastify";
import Image from "next/image";
import bg from "@/src/assets/sitebg.png";
import "react-toastify/dist/ReactToastify.css";
import "./globals.css";

const inter = Inter({ subsets: ["cyrillic", "latin"] });

export const metadata: Metadata = { title: "Sea Fight" };

export default function RootLayout({ children }: PropsWithChildren) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <ToastContainer newestOnTop hideProgressBar />
        <Image
          className="object-cover h-screen w-screen -z-10 fixed"
          src={bg}
          alt=""
        />
        {children}
      </body>
    </html>
  );
}
