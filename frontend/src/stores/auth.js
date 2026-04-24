import { defineStore } from "pinia";
import API from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    isAuthenticated: !!localStorage.getItem("token"),
  }),

  actions: {
    async login(username, password) {
      const res = await API.post("token/", {
        username,
        password,
      });

      this.token = res.data.access;
      this.isAuthenticated = true;

      localStorage.setItem("token", this.token);
    },

    logout() {
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem("token");
    },
  },
});