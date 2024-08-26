import { makeAutoObservable } from "mobx";

class TokenStore {
  private value: string | null = null;

  constructor() {
    makeAutoObservable(this);
  }

  hasToken() {
    return this.value !== null;
  }

  getToken() {
    return this.value;
  }

  setToken(newValue: string) {
    this.value = newValue;
  }
}

const tokenStore = new TokenStore();

export default tokenStore
