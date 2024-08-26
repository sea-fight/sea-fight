import axios from "axios";
import { INVALID_ACCESS_TOKEN } from "./errorCodes";
import tokenStore from "./tokenStore";
import reissueToken from "./endpoints/auth/reissue";
import signUpAnonymous from "./endpoints/auth/sign-up/anon";

let __promise = Promise.resolve();
let __isProcessing = false;

async function doRefreshToken() {
  if (!__isProcessing) {
    __isProcessing = true;
    __promise = reissueToken()
      .catch(signUpAnonymous)
      .then((token) => {
        tokenStore.setToken(token);
        __isProcessing = false;
      });
  }
  return __promise;
}

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
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
