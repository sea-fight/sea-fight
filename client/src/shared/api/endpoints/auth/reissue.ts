import client from "../../client";

export default function reissueToken() {
  return client.get("/auth/reissue").then((resp) => resp.data.token as string);
}
