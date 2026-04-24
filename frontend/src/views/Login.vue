<template>
  <div class="wrapper">
    <div class="login-card">
      <h1>CasinoPlaza</h1>
      <p class="subtitle">Login to start playing</p>

      <input
        v-model="username"
        placeholder="Username"
        class="input"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="input"
      />

      <button @click="handleLogin" class="btn">
        Login
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const error = ref("");

const auth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  error.value = "";

  try {
    await auth.login(username.value.trim(), password.value.trim());
    router.push("/game");
  } catch (err) {
    error.value = "Invalid username or password";
  }
};
</script>

<style scoped>
.wrapper {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1e1e2f, #2c2c54);
}

.login-card {
  background: #ffffff;
  padding: 35px;
  border-radius: 12px;
  width: 320px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  text-align: center;
}

h1 {
  margin-bottom: 5px;
}

.subtitle {
  font-size: 14px;
  color: #777;
  margin-bottom: 20px;
}

.input {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 6px;
  outline: none;
  transition: 0.2s;
}

.input:focus {
  border-color: #42b983;
  box-shadow: 0 0 5px rgba(66, 185, 131, 0.4);
}

.btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.2s;
}

.btn:hover {
  background: #369870;
}

.error {
  margin-top: 10px;
  color: red;
  font-size: 13px;
}
</style>