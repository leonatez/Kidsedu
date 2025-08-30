from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import random

app = FastAPI(title="Kidsedu - Educational Games for Kids", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

class MathQuestion(BaseModel):
    question: str
    answer: int
    options: List[int]

class MathGameRequest(BaseModel):
    max_number: int

class MathGameResponse(BaseModel):
    questions: List[MathQuestion]

class MathAnswerRequest(BaseModel):
    answers: List[int]
    correct_answers: List[int]

class MathAnswerResponse(BaseModel):
    score: int
    total: int
    percentage: float
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with math game"""
    with open("static/math_game.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/math", response_class=HTMLResponse)
async def math_game():
    """Math game for kids"""
    with open("static/math_game.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/math/generate", response_model=MathGameResponse)
async def generate_math_questions(request: MathGameRequest):
    """Generate 10 random math questions"""
    questions = []
    max_num = min(request.max_number, 100)  # Cap at 100 for safety
    
    for i in range(10):
        # Generate two random numbers
        num1 = random.randint(1, max_num)
        num2 = random.randint(1, max_num)
        
        # Random operation (addition, subtraction, multiplication)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            answer = num1 + num2
            question_text = f"{num1} + {num2} = ?"
        elif operation == '-':
            # Ensure positive result for kids
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            question_text = f"{num1} - {num2} = ?"
        else:  # multiplication
            # Keep numbers smaller for multiplication
            num1 = random.randint(1, min(12, max_num))
            num2 = random.randint(1, min(12, max_num))
            answer = num1 * num2
            question_text = f"{num1} × {num2} = ?"
        
        # Generate 3 wrong answers
        wrong_answers = []
        for _ in range(3):
            while True:
                wrong = answer + random.randint(-10, 10)
                if wrong != answer and wrong > 0 and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
                    break
        
        # Create options (1 correct + 3 wrong, shuffled)
        options = [answer] + wrong_answers
        random.shuffle(options)
        
        questions.append(MathQuestion(
            question=question_text,
            answer=answer,
            options=options
        ))
    
    return MathGameResponse(questions=questions)

@app.post("/math/check", response_model=MathAnswerResponse)
async def check_math_answers(request: MathAnswerRequest):
    """Check answers and provide motivational message"""
    correct_count = sum(1 for user_ans, correct_ans in zip(request.answers, request.correct_answers) 
                       if user_ans == correct_ans)
    total_questions = len(request.correct_answers)
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Motivational messages based on score
    if percentage == 100:
        message = "🌟 Perfect! You're a math superstar! 🌟"
    elif percentage >= 80:
        message = "🎉 Excellent work! You're amazing at math! 🎉"
    elif percentage >= 60:
        message = "👍 Great job! Keep practicing and you'll be even better! 👍"
    elif percentage >= 40:
        message = "💪 Good effort! Practice makes perfect! 💪"
    else:
        message = "🌈 Don't worry! Every mathematician started somewhere. Try again! 🌈"
    
    return MathAnswerResponse(
        score=correct_count,
        total=total_questions,
        percentage=percentage,
        message=message
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": "kidsedu"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)