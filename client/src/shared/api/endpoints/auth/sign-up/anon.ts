import client from "@/src/fsd/shared/api/client";

export default function signUpAnonymous() {
  return client.get("/auth/sign-up/anon").then((r) => r.data.token as string);
}
