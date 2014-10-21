Introduction
==============

Game engine prototype using Python, PyOpenGL, Pyglet and NumPy. It is mainly a study project.

### Features
* controllable FPS camera
* full ground collisions and gravity
* dynamic rendering distance
* dynamic world generation
* simple scripting
* asynchronous data generation


### Dependencies
* Python 2.7 (2.7.3, 2.7.6 tested)
* PyOpenGL 3.1.0
* Pyglet 1.1.4
* NumPy 1.8.1

System supports OpenGL 2.1 and above.

#### Installing dependencies
```$ pip install -r requirements.txt```

### Run program
```$ ./run.py```


### Controls
##### Normal controls
You can remap normal controls in global settings.ini file or override global settings in user.ini file.

Key | Action
---|---
UP | forward
DOWN | backward
LEFT | step left
RIGHT | step right
Space | jump

##### Development controls

Key | Action
---|---
1 | full rendering
2 | lines rendering
6 | toggle fullscreen
7 | toggle gravity
8 | move up
9 | move down


### Screenshots
phase 3

![phase 3](/imgs/img5.png)

phase 2

![](/imgs/img4.png)

phase 1

![](/imgs/img2.png)

![](/imgs/img1.png)

![](/imgs/img3.png)
