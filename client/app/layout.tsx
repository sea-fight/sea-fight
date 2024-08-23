import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { PropsWithChildren } from "react";
import { ToastContainer } from "react-toastify";
import Image from "next/image";
import bg from "@/src/assets/sitebg.png";
import SetToken from "@/src/utils/SetToken";
import reissueToken from "@/src/api/endpoints/auth/reissue";
import signUpAnonymous from "@/src/api/endpoints/auth/sign-up/anon";
import "react-toastify/dist/ReactToastify.css";
import "./globals.css";

const inter = Inter({ subsets: ["cyrillic", "latin"] });

export const metadata: Metadata = { title: "Sea Fight" };

export default async function RootLayout({ children }: PropsWithChildren) {
  const token = await reissueToken().catch(signUpAnonymous);

  return (
    <>
      <SetToken token={token} />
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
    </>
  );
}
