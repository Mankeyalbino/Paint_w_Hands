# Paint_w_Hands
Recreation of a basic paint like app with python and mediapipe to control with your hands.

![Paint](./Imagenes/Imagen5.png)

# Controls
This program is controlled by exclusively one hand, the cursor being the index finger and by making gestures as complementary indications. When you initiate the program put your hand in range of the camera's vision. Ypu will see some key points painted over the white canvas with interconnected lines. Adiotionally you will see that the index finger has the outline of a circle which radius indicates the thickness of the cursor.
** You can exit the program by entering the "esc" key at any moment **

## Selecting an action
To select an action close in the cursor (index finger) to the action button of your desire and when is under it extend your thumb and close it. By extending your thumb while the cursor is under a button, the action it´s counted as a click. If the action is active you can see that the button has a green border around it. You can also do a hold action instead of closing your thumb, so it dosen´t apply the action to the canvas, until you only have the index finger extended.

![Gesture-ref](./Imagenes/Imagen1.jpg)  

![Border-ref](./Imagenes/Border-ref.jpg)

## Selecting a color
You select a color the same way you select an action just make sure that your index finger is under the color box that you desire, extend your thumb and then close it. When a color is active you can see that there's a gray border around it's box. You can also do a hold action instead of closing your thumb, so it dosen´t apply the action to the canvas, until you only have the index finger extended.


## Hold
If the active action is painting or erasing, the action will be applied to the canvas once you only have the index finger extended. So for that to not hapen you can open your hand like you would when giving a high five.

![Hold-ref](Imgen2.jpg)

## Unselect an action 
If you want to deactivate an action just make a fist.

![Fist-ref](Imagen3.jpg)

## Actions applied with only index finger and selected by a click

### Paint (Pintar)
It leaves a trail of the selected color where your index finger passes.

### Eraser (Borrar)
It erases the color painted in the canvas where the index finger is passing through, leaving the space in blank.

### Thickness+ and Thickness- (Grosor+ y Grosor-)
Increases or decreases the effective radius of the cursor.

### Save
Saves the canvas in the directory where the program is allocated with the following name "Lienzo#.jpg", where # indicates the number of the exported canvas.

### HideUI
Hides the elements of the UI only leaving the option to Unhide it.

### Unhide
When you hide the UI, this option becomnes available and when clicked, it returns the UI elements.

### Clear
Clears the canvas.

## Actions selected by click, and applied by the index finger and the pinky
Some actions requires confirmation or gestures so the program knows when to place an object in screen.

![Gesto2-ref](Imagen3.jpg)

### Bucket
Once you select the bucket action hover the cursor over the space you want to fill and by extending the pinky finger the action is applied.

### Line, rectangle/square and circle (Línea, rectángulo/cuadrado y círculo)
These three actionshave two phases, the placement of the origin and the extention of the object. The thickness of the outlines or borders are afected by the radius of the cursor.

Starting with the line once it's active put the cursor where you want to place the initial point of the line and extend your pinky, once you do, you will see a preview of the placement of the line by moving your index finger around. Once you're satisfied by the placement close your pinky finger, and you will see it placed in the canvas.

The rectangle is the same sequence only that the first point you place is the right upper corner and the second is the left lower corner.

When it comes to the circle it's also the same sequence, only that the first point you place is the origin of the circle and then you extend the radius of it.


** DISCLAIMER **
You may use this program in whatever fashion you desire, only make sure to give the author credits and if you may like send pictures of where you use it, so I can put them in the fridge like a proud father.








