from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import random
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
app = FastAPI(title="Kidsedu - Educational Games for Kids", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Supabase configuration
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_ANON_KEY", "")
supabase: Client = None

# Debug logging for environment variables
print(f"SUPABASE_URL loaded: {'✓' if supabase_url else '✗'} ({'***' + supabase_url[-10:] if supabase_url else 'NOT SET'})")
print(f"SUPABASE_ANON_KEY loaded: {'✓' if supabase_key else '✗'} ({'***' + supabase_key[-10:] if supabase_key else 'NOT SET'})")

if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)
    print("✓ Supabase client initialized successfully")
else:
    print("✗ Supabase client not initialized - missing environment variables")

class MathQuestion(BaseModel):
    question: str
    answer: int
    options: List[int]

class MathGameRequest(BaseModel):
    max_number: int
    operations: Optional[str] = "basic"

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

# Vocabulary game models
class VocabularyItem(BaseModel):
    id: str
    image_url: str
    vocabulary: Optional[str] = None
    created_at: str

class VocabularyQuestion(BaseModel):
    image_url: str
    correct_answer: str
    options: List[str]

class VocabularyGameResponse(BaseModel):
    questions: List[VocabularyQuestion]

class VocabularyAnswerRequest(BaseModel):
    answers: List[str]
    correct_answers: List[str]

class VocabularyAnswerResponse(BaseModel):
    score: int
    total: int
    percentage: float
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with game selection"""
    with open("static/index_modern.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/math", response_class=HTMLResponse)
async def math_game():
    """Math game for kids"""
    with open("static/math_game_modern.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/math/generate", response_model=MathGameResponse)
async def generate_math_questions(request: MathGameRequest):
    """Generate 10 random math questions"""
    questions = []
    max_num = min(request.max_number, 100)  # Cap at 100 for safety
    
    # Determine available operations based on selection
    if request.operations == "basic":
        available_operations = ['+', '-']
    else:  # "all"
        available_operations = ['+', '-', '*', '/']
    
    for i in range(10):
        # Random operation from available operations
        operation = random.choice(available_operations)
        
        if operation == '+':
            num1 = random.randint(1, max_num)
            num2 = random.randint(1, max_num)
            answer = num1 + num2
            question_text = f"{num1} + {num2} = ?"
        elif operation == '-':
            # Ensure positive result for kids
            num1 = random.randint(1, max_num)
            num2 = random.randint(1, max_num)
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            question_text = f"{num1} - {num2} = ?"
        elif operation == '*':
            # Keep numbers smaller for multiplication
            num1 = random.randint(1, min(12, max_num))
            num2 = random.randint(1, min(12, max_num))
            answer = num1 * num2
            question_text = f"{num1} × {num2} = ?"
        else:  # division
            # Generate division that results in whole numbers
            # Start with answer and multiply to get dividend
            answer = random.randint(1, min(20, max_num))  # Keep division results reasonable
            num2 = random.randint(2, min(12, max_num))  # Divisor (avoid 1 for meaningful division)
            num1 = answer * num2  # Dividend (ensures whole number result)
            question_text = f"{num1} ÷ {num2} = ?"
        
        # Generate 3 wrong answers
        wrong_answers = []
        for _ in range(3):
            attempts = 0
            while attempts < 20:  # Prevent infinite loops
                if operation == '/':
                    # For division, generate reasonable wrong answers
                    wrong = answer + random.randint(-5, 5)
                else:
                    wrong = answer + random.randint(-10, 10)
                
                if wrong != answer and wrong > 0 and wrong not in wrong_answers:
                    wrong_answers.append(wrong)
                    break
                attempts += 1
            
            # If we couldn't generate a unique wrong answer, create one manually
            if len(wrong_answers) < (len(wrong_answers) + 1):
                for offset in [-1, 1, -2, 2, -3, 3]:
                    candidate = answer + offset
                    if candidate > 0 and candidate not in wrong_answers and candidate != answer:
                        wrong_answers.append(candidate)
                        break
        
        # Ensure we have exactly 3 wrong answers
        while len(wrong_answers) < 3:
            candidate = answer + len(wrong_answers) + 1
            if candidate not in wrong_answers:
                wrong_answers.append(candidate)
        
        # Create options (1 correct + 3 wrong, shuffled)
        options = [answer] + wrong_answers[:3]
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

# Vocabulary game endpoints
@app.get("/vocabulary", response_class=HTMLResponse)
async def vocabulary_game():
    """Vocabulary game for kids"""
    with open("static/vocabulary_game_modern.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/vocabulary/config", response_class=HTMLResponse)
async def vocabulary_config():
    """Vocabulary configuration page"""
    with open("static/vocabulary_config_modern.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/vocabulary/items")
async def get_vocabulary_items():
    """Get all vocabulary items"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        result = supabase.table("vocabulary_items").select("*").execute()
        return {"items": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vocabulary/upload")
async def upload_vocabulary_image(file: UploadFile = File(...)):
    """Upload vocabulary image to Supabase storage"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        # Read file content
        content = await file.read()
        file_path = f"vocabulary_images/{file.filename}"
        
        # Upload to Supabase storage
        supabase.storage.from_("vocabulary-images").upload(file_path, content, {
            "content-type": file.content_type
        })
        
        # Get public URL
        public_url = supabase.storage.from_("vocabulary-images").get_public_url(file_path)
        
        # Save to database
        vocabulary_item = {
            "image_url": public_url,
            "vocabulary": None
        }
        
        result = supabase.table("vocabulary_items").insert(vocabulary_item).execute()
        
        return {"success": True, "item": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vocabulary/update/{item_id}")
async def update_vocabulary(item_id: str, vocabulary: str = Form(...)):
    """Update vocabulary for an image"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        result = supabase.table("vocabulary_items").update({
            "vocabulary": vocabulary
        }).eq("id", item_id).execute()
        
        return {"success": True, "item": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vocabulary/generate", response_model=VocabularyGameResponse)
async def generate_vocabulary_questions():
    """Generate 10 vocabulary questions"""
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase not configured")
    
    try:
        # Get all vocabulary items that have vocabulary assigned
        result = supabase.table("vocabulary_items").select("*").neq("vocabulary", None).execute()
        vocabulary_items = result.data
        
        if len(vocabulary_items) < 4:
            raise HTTPException(status_code=400, detail="Not enough vocabulary items. Need at least 4 items with vocabulary assigned.")
        
        # Generate 10 questions without duplicates
        questions = []
        used_items = set()  # Track used items to prevent duplicates
        available_items = vocabulary_items.copy()
        random.shuffle(available_items)  # Shuffle for randomness
        
        questions_to_generate = min(10, len(vocabulary_items))
        
        for i in range(questions_to_generate):
            # Pick the next available item as correct answer (ensures no duplicates)
            correct_item = available_items[i]
            used_items.add(correct_item["id"])
            
            # Pick 3 other items as wrong answers (excluding used items if possible)
            wrong_items = [item for item in vocabulary_items 
                          if item["id"] != correct_item["id"] and 
                          item["vocabulary"] != correct_item["vocabulary"]]  # Avoid duplicate vocabulary words
            
            # If we have fewer than 3 wrong items, use what we have
            wrong_answers = random.sample(wrong_items, min(3, len(wrong_items)))
            
            # Create options (1 correct + wrong answers, shuffled)
            options = [correct_item["vocabulary"]] + [item["vocabulary"] for item in wrong_answers]
            random.shuffle(options)
            
            questions.append(VocabularyQuestion(
                image_url=correct_item["image_url"],
                correct_answer=correct_item["vocabulary"],
                options=options
            ))
        
        return VocabularyGameResponse(questions=questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vocabulary/check", response_model=VocabularyAnswerResponse)
async def check_vocabulary_answers(request: VocabularyAnswerRequest):
    """Check vocabulary answers and provide motivational message"""
    correct_count = sum(1 for user_ans, correct_ans in zip(request.answers, request.correct_answers) 
                       if user_ans == correct_ans)
    total_questions = len(request.correct_answers)
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Motivational messages based on score
    if percentage == 100:
        message = "🌟 Perfect! You're a vocabulary superstar! 🌟"
    elif percentage >= 80:
        message = "🎉 Excellent work! You're amazing with words! 🎉"
    elif percentage >= 60:
        message = "👍 Great job! Keep learning new words! 👍"
    elif percentage >= 40:
        message = "💪 Good effort! Practice makes perfect! 💪"
    else:
        message = "🌈 Don't worry! Every word expert started somewhere. Try again! 🌈"
    
    return VocabularyAnswerResponse(
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
