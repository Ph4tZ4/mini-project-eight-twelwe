#!/bin/bash

# Start development servers for the e-commerce project

echo "🚀 Starting Eight-Twelve E-commerce Development Servers..."

# Function to check if port is in use
check_port() {
    lsof -ti:$1 > /dev/null 2>&1
}

# Kill existing processes
echo "🧹 Cleaning up existing processes..."
if check_port 5550; then
    echo "  Stopping backend on port 5550..."
    lsof -ti:5550 | xargs kill -9 2>/dev/null
fi

if check_port 3330; then
    echo "  Stopping frontend on port 3330..."
    lsof -ti:3330 | xargs kill -9 2>/dev/null
fi

# Start backend
echo "🔧 Starting backend server (port 5550)..."
cd backend
source venv/bin/activate
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Test backend
if curl -s http://localhost:5550/api/ > /dev/null 2>&1; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
fi

# Start frontend
echo "🎨 Starting frontend server (port 3330)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 5

echo ""
echo "🎉 Development servers started!"
echo "   Backend:  http://localhost:5550"
echo "   Frontend: http://localhost:3330"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap 'echo "Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait
