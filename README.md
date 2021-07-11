# This Repository is a grape chunk detector used with images.
The functionalities are:

- ## Detect grape chunks

- ## Calculate the distance between most left chunk and most right chunk

- ## Present informations of the distance calculated, the number of chunks detected and the number of chunks per pixel

### There are three main files in this repository:

1) grapeChunk_detector_training.ipynb -> is the script used do train the dataset
2) grape_detector.py -> contains the inference logic to use with the test images
3) grape_detector.exe -> the detector executable file for Windows


 ### grapeChunk_detector_training.ipynb: 
 
  It has the step by step for the training process. You can open it using Google Collaboratory.
  
  For this custom detector I used **Darknet and YOLOv4 architecture model.**
  
  The folder structure on Drive in Collaboratory:
  
  ![project_structure_LI](https://user-images.githubusercontent.com/50181082/125208118-08ad0e00-e267-11eb-8f8a-702ee3aabd7b.jpg)
  
  ![project_structure_2_LI](https://user-images.githubusercontent.com/50181082/125207953-039b8f00-e266-11eb-87e5-2ce42457c20f.jpg)
  
  ![project_structure_3](https://user-images.githubusercontent.com/50181082/125208016-6db43400-e266-11eb-9991-82357827667b.PNG)
  
  ![project_structure_4](https://user-images.githubusercontent.com/50181082/125208022-7442ab80-e266-11eb-9315-aa0be8ff45c4.PNG)


  The files used to configure the custom detector are:
  
  - **obj folder** -> contains the dataset with images and labels. The dataset contains 291 for training and validation and for the inference it was separated 9 imagens
  just as example. 
  
  The dataset, with images and labels are available at the following link:
  
  https://drive.google.com/drive/folders/13UH_Anz2HmUIr0MLWJEDesky8Pm3K8NZ?usp=sharing

  - **obj.data file** -> contains data training information which are:
  
    - number of classes
  
    - path for training
  
    - path for validation
  
    - the names of the classes
  
    - path to save the weights
  
  See an example below:
  
  ![image](https://user-images.githubusercontent.com/50181082/125205235-a0a2fb80-e257-11eb-9f50-3177e54495e2.png)

  - **obj.names** -> define the names of the classes
  
  The name of class is "uva" which is the portuguese translation for grape

  - **yolov4-custom.cfg** -> custom cfg file defines variables for training process
  
  The configuration variables are:
  
    - batch size = 64
  
    - max_batches = (classes * 2000) = 6000 -> it corresponds to the number of complete iterations over the training set.
  Here we have just one class, but the minimun recomended for max_batches are 6000, to achieve good performance.
  
    - network size width=416 and height=416
  
    - filters=(classes + 5)x3 = 18 in the 3 [convolutional] before each [yolo] layer
  
  Examples: 
  
  ![custom_cfg1](https://user-images.githubusercontent.com/50181082/125205790-5d965780-e25a-11eb-8e15-8d2b48e7efdc.PNG)

  ![custom_cfg2](https://user-images.githubusercontent.com/50181082/125205784-57a07680-e25a-11eb-8045-b8f85f96f27c.PNG)


  - **process.py** -> creates the *train.txt* and *test.txt* that defines which images will be used for training and which will be used for validation.
  
  ### grape_detector.py and grape_detector.exe  
  
  Both files are a python GUI to run detection of grape chunks on test images.
  
  For that, the **yolov4-custom_best.weights** and **yolov4-custom.cfg** files are needed, which are the trained weights of the grape chunk detector and
  the model configuration file.
  
  grape_detector.py has comments that explain the code
  
  Usage:
  
  Run any of them and a image viewer will open:
  
  ![detector_1](https://user-images.githubusercontent.com/50181082/125206338-237a8500-e25d-11eb-98cb-3ec637d24ee2.PNG)
  
  Then click on "Browse" and chose the folder in which has test images.
  
  **IMPORTANT:** for this application, only **.png** images will work.
  
  A list of your images will show up:
  
  ![detector_2](https://user-images.githubusercontent.com/50181082/125206437-abf92580-e25d-11eb-9ad0-68ade98265b6.PNG)
  
  Choose an image and click on "Detect" button to start the inference and analyse the results:
  
  ![detector_3](https://user-images.githubusercontent.com/50181082/125206505-0c886280-e25e-11eb-9a76-bb46ae5fdf16.PNG)
  
  ![detector_4](https://user-images.githubusercontent.com/50181082/125206613-802a6f80-e25e-11eb-93a6-b514fec9f5a2.PNG)


  To exit the program, just click on "Exit" button.

