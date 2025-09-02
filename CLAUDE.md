# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kidsedu is a FastAPI-based educational math game for kids featuring interactive arithmetic problems (addition, subtraction, multiplication) with a colorful, responsive web interface. The application generates random math questions, provides multiple-choice answers, and offers motivational feedback.

## Development Commands

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server (serves on port 8001)
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8001
```

### Docker Development
```bash
# Build container
docker build -t kidsedu .

# Run container
docker run -p 8001:8001 kidsedu
```

## Architecture

### Backend Structure
- **main.py**: FastAPI application with math game logic
  - `/`: Home page serving the game interface
  - `/math/generate`: POST endpoint generating 10 random questions
  - `/math/check`: POST endpoint for answer validation
  - `/health`: Health check endpoint
- **Static file serving**: Game assets served from `/static/` directory

### Frontend Structure
- **static/math_game.html**: Single-page game interface
- **static/math_game.css**: Styling with animations and responsive design
- Game flow: Setup → Question generation → Answer checking → Results

### Game Logic
- Questions generated with configurable max number (5-100, capped at 100)
- Operations: addition, subtraction (ensures positive results), multiplication (limited to 12x12)
- Multiple choice: 1 correct + 3 wrong answers, randomly shuffled
- Scoring with motivational messages based on percentage (100%, 80%+, 60%+, 40%+, <40%)

## Deployment

### CapRover Deployment
- Configured for automatic deployment via git webhook
- Uses `captain-definition` and `Dockerfile`
- Runs on port 8001 (distinct from other services)
- Health check endpoint at `/health`

### Production Considerations
- Application runs on port 8001 by default
- Lightweight Docker image (python:3.11-slim base)
- Health checks configured for container orchestration
- Static files served directly by FastAPI (suitable for this simple app)

## Dependencies

Core dependencies in requirements.txt:
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `python-multipart==0.0.6` - Form data parsing
- `supabase==2.3.4` - Supabase integration
- `python-dotenv==1.0.0` - Environment variables

## Deployment Trigger
Last updated: 2025-09-02 - Modern redesign with vocabulary game deployed