# Dynamic Chess Analyzer

Dynamic Chess Analyzer is a computer-vision-based chess analysis system that tracks moves played on a physical chessboard using a webcam and analyzes the game using the Stockfish chess engine.

## Features

- Webcam-based physical chessboard input
- Manual four-corner board calibration
- Perspective transformation using OpenCV
- 8x8 chessboard grid processing
- Frame-difference-based move detection
- Legal move inference using python-chess
- Stockfish UCI integration
- Best move recommendation
- Position evaluation
- Centipawn-loss calculation
- Move classification
- Best-move arrow visualization
- FEN generation
- PGN export
- JSON analysis report

## Technologies

- Python
- OpenCV
- NumPy
- python-chess
- Stockfish
- python-dotenv

## Architecture

Physical Chessboard  
→ Webcam  
→ OpenCV  
→ Perspective Transformation  
→ 8x8 Grid  
→ Frame Difference  
→ Changed Squares  
→ Legal Move Inference  
→ python-chess  
→ Stockfish  
→ Move Evaluation  
→ Report Generation

## Setup

Create and activate a Python 3.12 virtual environment.

Install dependencies:

```bash
pip install -r requirements.txt