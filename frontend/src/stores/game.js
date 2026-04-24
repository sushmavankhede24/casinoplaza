import { defineStore } from "pinia";

export const useGameStore = defineStore("game", {
  state: () => ({
    credits: 0,
    wallet: 0,
    is_active: false,
    result: null,
  }),

  actions: {
    // actions
  },
});