# Flappy Bird NEAT AI

This project is a CSCI218 coursework submission that implements the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to teach an AI agent how to play the Flappy Bird game. The agent learns through generations of evolution, improving its ability to navigate through obstacles without direct programming.

## 🎮 Project Overview
- A basic Flappy Bird clone is developed using `pygame`.
- AI control is implemented using `neat-python`, evolving neural networks to play the game.
- The neural network receives game state inputs and decides whether the bird should flap or not.

## 🧠 Technologies Used
- Python 3.6+
- Pygame (for game rendering and loop)
- NEAT-Python (for neuroevolution)

## 🗂️ File Structure
```
├── assets/                # Image assets (bg.png, pipe.png, bird frames, etc.)
├── neat-config/           # NEAT algorithm configuration file
├── flappy_bird.py         # Main script that trains the AI
├── github_version.py      # (Optional) Cleaned-up version for publication
├── requirements.txt       # Required Python libraries
├── README.md              # Project overview and instructions
├── Report.pdf             # Formal report for the project
```

## ⚙️ Setup Instructions
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the training program:
    ```bash
    python flappy_bird.py
    ```

3. Modify the config file in `neat-config/config_file.txt` to tweak training behavior.

## 📄 Report
See `Report.pdf` for in-depth documentation of the project, including technical overview and results.

## 👨‍💻 Authors
- Mikaeel Faraz Safdar
- Mohammad Qudaih
- Haifa Shkhedem
- Surya John Prabhu
- Abhinandan Ajit Kumar
