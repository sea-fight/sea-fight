import axios from "axios";
import tokenStore from "./tokenStore";
import { INVALID_ACCESS_TOKEN } from "./errorCodes";
import refreshToken from "./endpoints/refreshToken";

let __promise = Promise.resolve();
let __isProcessing = false;

function doRefreshToken() {
  if (__isProcessing) {
    return __promise;
  } else {
    const { promise, resolve, reject } = Promise.withResolvers<void>();
    __promise = promise;
    __isProcessing = true;
    refreshToken().then(() => (resolve(), (__isProcessing = false)), reject);
  }
}

const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
});

client.interceptors.request.use((config) => {
  if (tokenStore.hasToken()) {
    config.headers["Authorization"] = tokenStore.getToken();
  }
  return config;
});

client.interceptors.response.use(async (response) => {
  if (!response.data.ok) {
    switch (response.data.code) {
      case INVALID_ACCESS_TOKEN:
        await doRefreshToken();
        return client(response.config);

      default:
        throw Error("Request failed: " + response.data.code);
    }
  }
  return response;
});

export default client;
