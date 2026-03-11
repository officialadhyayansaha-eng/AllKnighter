# Chess Engine + Neural Evaluation

A simple chess engine implemented in Python with legal move generation for all pieces and a basic evaluation function.  
The project also includes a neural network–based position evaluation model built with PyTorch.

## Features

- 8×8 board representation and piece state tracking
- Legal move generation for:
  - Pawn
  - Knight
  - Bishop
  - Rook
  - Queen
  - King
- Capture handling and pawn promotion
- Material-based evaluation function
- Command-line interface for playing moves
- Neural network position evaluation using PyTorch
- Chess position encoding using a **12×8×8 tensor representation**

## Running the Engine

```bash
python allknighter.py
```

Enter moves in the format:

```
PIECE_NAME INITIAL FINAL
```

Example:

```
Pawn [4,1] [4,3]
```

## Future Improvements
- En passant detection
- Minimax search
- Alpha–beta pruning
- Check / checkmate detection
- Improved evaluation functions
- Self-play training for neural evaluation
