# CIS667-21F-Project  

[project_state](project_state.py) contains the domain implementation of Dots and Boxes.  
[project_ai](project_ai.py) contains the tree-based AI while NN not applied for a better evaluator function.  
[project_play](project_play.py) contains interactive domain program.  
[project_data](project_data.py) contains programs to generate training data for neural network.  
[project_NN](project_NN.py) contains neural network training and tree+NN AI testing.  
[project_play_NN](project_play_NN.py) contains interactive domain program (adding neural network AI).  

Dependencies required: numpy, time, copy, pandas.  

To run the interactive domain program: Run [project_play](project_play.py).  
			1) Enter a number to choose a size.  
			2) Enter a number to choose Player A, then B.  
			3) To start the game or let AI player to perform action, press ENTER.  
			
To run the computer experiments: Run [project_ai](project_ai.py). (More than 5 hours for 100 games for each size)
