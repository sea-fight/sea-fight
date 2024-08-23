import axios from "axios";
import { INVALID_ACCESS_TOKEN } from "./errorCodes";
import tokenStore from "./tokenStore";
import reissueToken from "./endpoints/auth/reissue";

let __promise = Promise.resolve();
let __isProcessing = false;

const doRefreshToken = () => {
  if (__isProcessing) {
    return __promise;
  } else {
    const { promise, resolve, reject } = Promise.withResolvers<void>();
    __promise = promise;
    __isProcessing = true;
    reissueToken().then(token => {
      tokenStore.setToken(token)
      resolve();
      __isProcessing = false;
    }, reject);
  }
};

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
    }
    return Promise.reject(response);
  }
  return response;
});

export default client;
