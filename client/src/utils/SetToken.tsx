"use client";

import tokenStore from "../api/tokenStore";

export default function SetToken({ token }: { token: string }) {
  tokenStore.setToken(token);
  return null;
}
