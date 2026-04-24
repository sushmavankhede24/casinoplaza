import { createRouter, createWebHistory } from 'vue-router'
import Login from "../views/Login.vue";
import Game from "../views/Game.vue";
import { useAuthStore } from "../stores/auth";


const routes = [
  { path: "/", component: Login },
  { path: "/game", component: Game },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Protect game route
router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.path === "/game" && !auth.isAuthenticated) {
    next("/");
  } else {
    next();
  }
});

export default router
