# CIS667-21F-Project  

[project_state](project_state.py) contains the domain implementation of Dots and Boxes.  
[project_ai](project_ai.py) contains the tree-based AI while NN not applied for a better evaluator function.  
[project_play](project_play.py) contains interactive domain program.  
[project_data](project_data.py) contains programs to generate training data for neural network.  
Game stats and utilities saved in [samples](samples.xlsx) and [evaluate](evaluate.xlsx) respectively.  
The above 2 files are required to run [project_NN](project_NN.py) and [project_play_NN](project_play_NN.py).    
[project_NN](project_NN.py) contains neural network training and tree+NN AI testing.  
[project_play_NN](project_play_NN.py) contains interactive domain program (adding neural network AI).  

Dependencies required: numpy, time, copy, pandas, pytorch.  

To run the interactive domain program: Run [project_play](project_play.py).  
			1) Enter a number to choose a size.  
			2) Enter a number to choose Player A, then B.  
			3) To start the game or let AI player to perform action, press ENTER.  
  
To run the interactive domain program with NN AI: Run [project_play_NN](project_play_NN.py).  
			1) Wait for NN training.  
			2) Enter a number to choose Player A, then B.  
			3) To start the game or let AI player to perform action, press ENTER.
  
To run the computer experiments: Run [project_ai](project_ai.py). (More than 5 hours for 100 games for each size)  
To generate training data: Run [project_data](project_data.py).  
To run NN training and experiments: Run [project_NN](project_NN.py).
