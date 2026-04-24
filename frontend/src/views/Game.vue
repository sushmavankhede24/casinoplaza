<template>
  <div class="wrapper">
    <div class="top-bar">
      <button class="logout-btn" @click="handleLogout">
            Logout
      </button>
    </div>

     <div class="card">
      <h2>Casino Plaza</h2>
      <p>Welcome! You are logged in.</p>

      <!-- STATUS -->
      <div class="stats">
        <p>Credits: <strong>{{ game.credits }}</strong></p>
        <p>Wallet: <strong>{{ game.wallet }}</strong></p>
      </div>

      <!-- ACTIONS -->
      <div class="actions">
        <button @click="handleStartSession" :disabled="game.is_active">Start Session</button>
        <button @click="handleSpin" :disabled="!game.is_active">Spin</button>
        <button @click="handleCashout" :disabled="!game.is_active">Cashout</button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="game.is_active" class="info">Session already active</p>

      <!-- RESULT -->
      <div v-if="game.result" class="result">
         <p> Symbols:
            <span v-for="(symbol, index) in game.result.symbols" :key="index">
            {{ getEmoji(symbol) }}&nbsp;
            </span>
         </p>
        <p>Reward: {{ game.result.reward }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useGameStore } from "../stores/game";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const game = useGameStore();
const error = ref("");
const auth = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  router.push("/login");
};

const getEmoji = (symbol) => {
  const map = {
    cherry: "🍒",
    lemon: "🍋",
    orange: "🍊",
    watermelon: "🍉",
  };
  return map[symbol] || symbol;
};

const handleStartSession = async () => {
  error.value = "";

  try {
    await game.startSession();
  } catch (err) {
    error.value = err.response?.data?.detail || "Something went wrong";
  }
};

const handleSpin = async () => {
  error.value = "";

  try {
    await game.spin();
  } catch (err) {
    error.value = err.response?.data?.detail || "Spin failed";
  }
};

const handleCashout = async () => {
  error.value = "";

  try {
    await game.cashout();
  } catch (err) {
    error.value = err.response?.data?.detail || "Cashout failed";
  }
};

onMounted(() => {
  game.fetchStatus();
});
</script>

<style scoped>
.wrapper {
  position: relative;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #1e1e2f;
}

.card {
  position: relative;
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 350px;
  text-align: center;
}

.stats {
  margin: 15px 0;
}

.actions button {
  margin: 5px;
  padding: 10px;
  border: none;
  background: #42b983;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.actions button:hover {
  background: #369870;
}

.result {
  margin-top: 15px;
}

.error {
  margin-top: 10px;
  color: red;
  font-size: 14px;
}

.info {
  margin-top: 10px;
  color: #555;
  font-size: 13px;
}

.top-bar {
  position: absolute;
  top: 20px;
  right: 20px;
}

.logout-btn {
  padding: 8px 12px;
  background: #ff4d4f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.logout-btn:hover {
  background: #d9363e;
}

.result span {
  font-size: 24px;
  margin: 0 4px;
}
</style>