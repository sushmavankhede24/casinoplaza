import { defineStore } from "pinia";
import API from "../services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    username: localStorage.getItem("username") || null,
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
      this.username = username;

      localStorage.setItem("token", this.token);
      localStorage.setItem("username", username); 
    },

    logout() {
      this.token = null;
      this.username = null;
      this.isAuthenticated = false;
      localStorage.removeItem("token");
      localStorage.removeItem("username");
    },
  },
});