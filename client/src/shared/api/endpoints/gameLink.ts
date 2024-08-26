import client from "../client";

export default async function generateGameLink() {
  return client.get("/generateGameLink").then((x) => x.data.link as string);
}
