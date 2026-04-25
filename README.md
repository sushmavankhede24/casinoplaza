# CasinoPlaza

A full-stack slot machine game built with **Django (Backend)** and **Vue 3 (Frontend)**.  
Users can register, log in, play a session-based game, and manage their credits and wallet balance.

The backend acts as the source of truth for all game logic, including session handling and reroll behavior.

---

## Live Application
- **Frontend:** https://casinoplaza.vercel.app/
- **Backend:** https://sushmavankhede.pythonanywhere.com/api/
- **API Health Check:** https://sushmavankhede.pythonanywhere.com/

---

## Features

- User registration and authentication (JWT)
- Session-based gameplay
- Slot machine with random symbols
- Reward system for matching symbols
- Backend-controlled reroll logic for game balancing
- Wallet system with cashout functionality
- Protected routes and logout

---

## How to Use

1. Register a new account  
2. Login  
3. Start a game session  
4. Spin the slot machine  
5. Cash out credits to wallet  
6. Start a new session to play again (optional)  
7. Logout

## Game Rules

- Each session starts with **10 credits**
- Each spin costs **1 credit**
- Each spin generates **3 random symbols**
- Rewards are given when all symbols match:

  |  Symbols  |  Reward  |
  |-----------|----------|
  | Cherry (🍒) |   +10   |
  | Lemon (🍋)  |   +20   |
  | Orange (🍊) |   +30   |
  |Watermelon(🍉)| +40   |
  
---

## Reroll Logic

Winning results may be rerolled based on current credits:

- **< 40 credits** → No reroll  
- **40–60 credits** → 30% chance  
- **> 60 credits** → 60% chance

Rerolling is handled on the backend and is not visible to the user.

---

## Wallet & Sessions

- Credits can be cashed out to wallet  
- Session ends when:
  - Credits reach **0**, or
  - User cashes out  
- Only one active session per user

---

## API Endpoints

Base URL: https://sushmavankhede.pythonanywhere.com/api/

- **POST** /register/ — Register a new user
- **POST** /token/ — Login and receive JWT tokens
- **POST** /token/refresh/ — Refresh access token
- **POST** /start-session/ — Start a new session
- **POST** /spin/ — Spin the slot machine
- **POST** /cashout/ — Cash out credits
- **GET** /status/ — Get current session status

---

## Tech Stack

- **Backend:** Django, Django REST Framework  
- **Frontend:** Vue 3 (Vite, Pinia)  
- **Database:** SQLite  
- **Authentication:** JWT

---

## Deployment

- Backend deployed on PythonAnywhere
- Frontend deployed on Vercel

The frontend communicates with the backend via REST APIs.

---

## Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (choose one)
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows (cmd)
# venv\Scripts\Activate.ps1     # Windows (PowerShell)

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Start server
python manage.py runserver

```
Runs on: http://127.0.0.1:8000/ (local development)

### Frontend

```bash

cd frontend

# Install dependencies
npm install

# Start development server
npm run dev   

```
Runs on: http://localhost:5173/ (local development)

### Frontend - Backend Communication

The frontend communicates with the backend API at:
- Local: http://127.0.0.1:8000/api/
- Production: https://sushmavankhede.pythonanywhere.com/api/

Make sure CORS is properly configured in the backend to allow requests from: http://localhost:5173.

## Environment Variables

Create a .env file in the backend:
```bash

SECRET_KEY=your-secret-key
DEBUG=True # for local development

```

## Assumptions & Tradeoffs

- JWT-based authentication was used for simplicity and scalability
- Single active session per user to simplify session management
- Reroll logic is handled silently on the backend
- Wallet balance persists across sessions
- SQLite used for simplicity 
- Backend handles all game logic
- Minimal UI design to prioritize core functionality within time constraints
  
## Future Improvements

- Add leaderboard or scoring system
- Add game history / transaction tracking
- Improve UI with animations
- Containerize the application using Docker for easier setup and deployment

## Author

Sushma Vankhede
