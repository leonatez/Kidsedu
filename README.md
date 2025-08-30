# 🌈 Kidsedu - Educational Games for Kids 🚀

A fun and colorful web-based math game designed specifically for children to learn and practice basic arithmetic operations in an engaging way.

## ✨ Features

- **🧮 Interactive Math Game**: Addition, subtraction, and multiplication problems
- **🎨 Colorful UI**: Kid-friendly design with animations and effects
- **🏆 Progress Tracking**: Visual progress bar and scoring system
- **🎉 Motivational Feedback**: Encouraging messages based on performance
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices
- **🎯 Customizable Difficulty**: Choose maximum numbers for problems

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

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

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:8001`

## 🎮 How to Play

1. **Choose Difficulty**: Select the maximum number for your math problems (5-100)
2. **Start Playing**: Click "Start Playing!" to begin
3. **Solve Problems**: Choose the correct answer from 4 multiple choice options
4. **Track Progress**: Watch the colorful progress bar fill up as you complete questions
5. **See Results**: Get your score and motivational message at the end
6. **Play Again**: Challenge yourself with a new set of questions!

## 🛠️ API Endpoints

- `GET /` - Home page with math game
- `GET /math` - Direct access to math game
- `POST /math/generate` - Generate 10 random math questions
- `POST /math/check` - Check answers and get results
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
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── static/
    ├── math_game.html     # Game interface
    └── math_game.css      # Styling and animations
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