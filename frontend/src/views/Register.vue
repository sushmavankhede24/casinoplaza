<template>
  <div class="wrapper">
    <div class="card">
      <h1>Casino Plaza</h1>
      <p class="subtitle">Create your account</p>

      <input v-model="username" placeholder="Username" class="input" />
      <input v-model="password" type="password" placeholder="Password" class="input" />

      <button @click="handleRegister" class="btn">
        Register
      </button>

      <p v-if="error" class="error">{{ error }}</p>

      <p class="link">
        Already have an account?
        <span @click="goToLogin">Login</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import API from "../services/api";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const error = ref("");

const router = useRouter();

const handleRegister = async () => {
  error.value = "";

  try {
    await API.post("register/", {
      username: username.value.trim(),
      password: password.value.trim(),
    });

    alert("Registration successful!");
    router.push("/login");
  } catch (err) {
    error.value =
      err.response?.data?.username?.[0] ||
      err.response?.data?.password?.[0] ||
      "Registration failed";
  }
};

const goToLogin = () => {
  router.push("/login");
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

.card {
  background: white;
  padding: 35px;
  border-radius: 12px;
  width: 320px;
  text-align: center;
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
  box-sizing: border-box; 
}

.btn {
  width: 100%;
  padding: 12px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.btn:hover {
  background: #369870;
}

.error {
  margin-top: 10px;
  color: red;
  font-size: 13px;
}

.link {
  margin-top: 15px;
  font-size: 13px;
}

.link span {
  color: #42b983;
  cursor: pointer;
  font-weight: bold;
}
</style>