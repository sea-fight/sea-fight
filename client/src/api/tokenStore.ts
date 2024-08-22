import { makeAutoObservable } from "mobx";

class TokenStore {
  private value?: string;

  constructor() {
    makeAutoObservable(this);
  }

  hasToken() {
    return this.value !== undefined;
  }

  getToken() {
    return this.value;
  }

  setToken(newValue: string) {
    this.value = newValue;
  }
}

const tokenStore = new TokenStore();

export default tokenStore;
