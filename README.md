# 🌈 Kidsedu - Educational Games for Kids 🚀

Kidsedu is a FastAPI-based educational platform featuring interactive games designed to make learning fun for kids. Currently includes Math Game and English Vocabulary Game.

## ✨ Features

### 🧮 Math Game
- **Interactive arithmetic problems**: Addition, subtraction, and multiplication
- **Customizable difficulty levels**: Choose maximum numbers (5-100)
- **Multiple-choice questions**: Visual feedback and progress tracking
- **Motivational messages**: Encouraging feedback based on performance
- **Confetti celebrations**: For good scores!

### 📚 English Vocabulary Game
- **Custom image-based vocabulary learning**: Upload your own images
- **Automatic image optimization**: Images resized to 30% of original size for faster loading
- **Supabase integration**: Cloud storage for images and vocabulary data
- **Bulk vocabulary assignment**: Type vocabularies for all images at once
- **Visual learning approach**: Learn words through pictures
- **Configuration interface**: Assign vocabulary words to uploaded images
- **Duplicate-free questions**: No repeated vocabulary items in a single game
- **Same scoring system**: Consistent experience across games

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Supabase account (for vocabulary game)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Kidsedu.git
cd Kidsedu
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Configure Supabase (for vocabulary game):**
   - Create a Supabase project at [supabase.com](https://supabase.com)
   - Copy `.env.template` to `.env`
   - Fill in your Supabase URL and anon key:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Set up Supabase database:**
   - Run the SQL commands from `supabase_schema.sql` in your Supabase SQL editor
   - This creates the `vocabulary_items` table and storage bucket

5. Run the application:
```bash
python main.py
```

6. Open your browser and navigate to `http://localhost:8001`

## 🎮 How to Play

### Math Game
1. **Choose Difficulty**: Select the maximum number for your math problems (5-100)
2. **Start Playing**: Click "Start Playing!" to begin
3. **Solve Problems**: Choose the correct answer from 4 multiple choice options
4. **Track Progress**: Watch the colorful progress bar fill up as you complete questions
5. **See Results**: Get your score and motivational message at the end

### Vocabulary Game
1. **First time setup:**
   - Go to "Configure Vocabulary" from the home page
   - Upload images (JPG, PNG, etc.) - they'll be automatically resized to 30%
   - **Option 1 - Bulk Assignment:** Use the "Quick Assignment" section to type vocabularies for all images at once
   - **Option 2 - Individual Assignment:** Assign vocabulary words to each image individually
   - Save your vocabulary

2. **Playing the game:**
   - Go to "Play Vocabulary Game"
   - Look at the image and choose the correct vocabulary word
   - Answer 10 unique questions (no duplicates) and see your score!

## 🛠️ API Endpoints

### Math Game
- `GET /math` - Math game page
- `POST /math/generate` - Generate 10 random math questions
- `POST /math/check` - Check answers and get results

### Vocabulary Game
- `GET /vocabulary` - Vocabulary game page
- `GET /vocabulary/config` - Configuration page
- `GET /vocabulary/items` - Get all vocabulary items
- `POST /vocabulary/upload` - Upload new image
- `POST /vocabulary/update/{item_id}` - Update vocabulary for image
- `POST /vocabulary/generate` - Generate 10 vocabulary questions
- `POST /vocabulary/check` - Check answers and get score

### General
- `GET /` - Home page with game selection
- `GET /health` - Health check endpoint

## 🚀 Deployment

### CapRover Deployment

This project is configured for automatic deployment with CapRover:

1. **Prerequisites**: 
   - CapRover instance running on your VPS
   - Git webhook configured to trigger builds on push

2. **Configuration Files**:
   - `captain-definition` - CapRover deployment configuration
   - `Dockerfile` - Container configuration optimized for Kidsedu
   - Runs on port 8001 (different from other services)

3. **Auto-deployment**: 
   - Push to GitHub repository triggers automatic build and deployment
   - Lightweight container without Chrome/Selenium dependencies
   - Built-in health checks and logging

4. **Access**: 
   - Production: `https://your-caprover-domain.com`
   - Local development: `http://localhost:8001`

### Docker Deployment

```bash
# Build the container
docker build -t kidsedu .

# Run the container
docker run -p 8001:8001 kidsedu
```

## 🎨 Game Features

### Visual Elements
- **Rainbow gradient background** with smooth animations
- **Bouncing title** and floating math symbols
- **Colorful buttons** with hover effects and animations
- **Progress bar** with shimmer effects
- **Confetti celebration** for good scores (70%+)

### Educational Benefits
- **Basic Arithmetic**: Addition, subtraction, multiplication
- **Mental Math**: Quick calculation practice
- **Problem Solving**: Multiple choice decision making
- **Positive Reinforcement**: Encouraging feedback system

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with animations and gradients
- **Responsive**: Mobile-first design approach

## 📝 Development

### Project Structure
```
Kidsedu/
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies  
├── README.md                        # Project documentation
├── .env.template                    # Environment variables template
├── supabase_schema.sql             # Database schema for vocabulary game
├── CLAUDE.md                       # Project instructions
└── static/
    ├── index.html                  # Home page with game selection
    ├── math_game.html              # Math game interface
    ├── math_game.css               # Shared styles and animations
    ├── vocabulary_game.html        # Vocabulary game interface
    └── vocabulary_config.html      # Vocabulary configuration page
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Support

If you encounter any issues or have suggestions for improvement, please open an issue on GitHub.

---

**Made with ❤️ for kids who love learning math!** 🎓✨