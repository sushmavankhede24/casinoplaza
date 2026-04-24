import { defineStore } from "pinia";
import API from "../services/api"

export const useGameStore = defineStore("game", {
  state: () => ({
    credits: 0,
    wallet: 0,
    is_active: false,
    result: null,
  }),

  actions: {
    async fetchStatus() {
      const res = await API.get("status/");
      this.credits = res.data.credits;
      this.wallet = res.data.wallet_balance;
      this.is_active = res.data.is_active;
    },

    async startSession() {
      await API.post("start-session/");
      this.result = null;
      await this.fetchStatus();
    },

    async spin() {
      const res = await API.post("spin/");
      this.result = res.data;
      await this.fetchStatus();
    },

    async cashout() {
      await API.post("cashout/");
      this.result = null;
      await this.fetchStatus();
    },
  },
});