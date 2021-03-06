import math
import cv2
import PySimpleGUI as sg
import os.path
import numpy as np


def calculate_distance(boxes):
	'''Function to calculate the distance between the most left
	chunk and the most right chunk.
	'''
	min = 10000
	max = 0

	#gets the most left and most right x coordinate value
	for box in boxes:
		if box[0] < min:
			min = box[0]
			chunk1 = box

		if box[0] > max:
			max = box[0]
			chunk2 = box

	point_chunk2_x = chunk2[0] + chunk2[2]   #most right x coordinate
	point_chunk2_y = chunk2[1] + chunk2[3]/2 #height of most right bounding box divided by two
	point_chunk1_x = chunk1[0]               #most left x coordinate
	point_chunk1_y = chunk1[1] + chunk1[3]/2 #height of most left bounding box divided by two

	#calculate distance
	distance = math.sqrt((point_chunk2_x - point_chunk1_x) ** 2 + (point_chunk2_y - point_chunk1_y))

	#print("Calculated Distance: ", distance)

	return distance, point_chunk1_x, point_chunk1_y, point_chunk2_x, point_chunk2_y

if __name__ == "__main__":
	'''Building the Image Viewer ########################################################'''
	# First the window layout in 2 columns
	file_list_column = [
		[
			sg.Text("Image Folder"),
			sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
			sg.FolderBrowse(),
		],
		[
			sg.Listbox(
				values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
			)
		],
	]

	image_viewer_column = [
		[sg.Text("Choose an image from list on left:")],
		[sg.Text(size=(40, 1), key="-TOUT-")],
		[sg.Image(key="-IMAGE-")],
	]

	# ----- Full layout -----
	layout = [
		[
			sg.Column(file_list_column),
			sg.VSeperator(),
			sg.Column(image_viewer_column),
		],
		[sg.Button("Detect")],
		[sg.Button("Exit")]
	]

	window = sg.Window("Grape Detection Viewer", layout)
	'''#############################################################################'''


	cfg = "yolov4-custom.cfg"                   #config file
	weights = "yolov4-custom_best.weights"      #trained weights
	input_size = (416, 416)                     #net input size

	#configure the network
	net = cv2.dnn_DetectionModel(cfg, weights)
	net.setInputSize(input_size)
	net.setInputScale(1.0 / 255)
	net.setInputSwapRB(True)

	#Application loop
	while True:
		event, values = window.read()
		#if the button Exit are pressed or the window closed, the application ends
		if event == "Exit" or event == sg.WIN_CLOSED:
			break

		# Folder name was filled in, make a list of files in the folder
		if event == "-FOLDER-":
			folder = values["-FOLDER-"]
			try:
				# Get list of files in folder
				file_list = os.listdir(folder)
			except:
				file_list = []

			fnames = [
				f
				for f in file_list
				if os.path.isfile(os.path.join(folder, f))
				   and f.lower().endswith((".png", ".gif"))
			]
			window["-FILE LIST-"].update(fnames)

		elif event == "-FILE LIST-":  # A file was chosen from the listbox
			try:
				filename = os.path.join(
					values["-FOLDER-"], values["-FILE LIST-"][0]
				)
				window["-TOUT-"].update(filename)
				window["-IMAGE-"].update(filename=filename) #update the window with the chosen image
			except:
				pass

		#if the button Detect is pressed, the inference starts on the selected image
		elif event == "Detect":
			image = cv2.imread(filename)
			classes, confidences, boxes = net.detect(image, confThreshold=0.1, nmsThreshold=0.1)	#make inference

			with open('obj.names', 'rt') as f:
				names = f.read().rstrip('\n').split('\n')

			#calls the function to calculate distance
			dist, p1_x, p1_y, p2_x, p2_y = calculate_distance(boxes)

			#plot all the bounding boxes detected with its confidences
			for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
				label = '%.2f' % confidence
				label = '%s: %s' % (names[classId], label)
				labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
				left, top, width, height = box
				top = max(top, labelSize[1])
				cv2.rectangle(image, box, color=(0, 255, 0), thickness=3)
				cv2.rectangle(image, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv2.FILLED)
				cv2.putText(image, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

			color_line = (0,0,255)
			color_text = (255,255,255)

			#plot the line indicating the distance between the most left chunk and the most right
			cv2.line(image, (int(p1_x),int(p1_y)), (int(p2_x),int(p2_y)), color_line, 2)

			#plot informations about the detection
			cv2.putText(image, "Approximate distance in pixels: " + str(np.round(dist)), (10, 30) , cv2.FONT_HERSHEY_SIMPLEX, 1, color_text, 2)
			cv2.putText(image, "Number of Chunks detected : " + str(len(boxes)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, color_text, 2)
			cv2.putText(image, "Chunks per pixel rate: " + str(np.round(len(boxes)/np.round(dist), 4)), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, color_text, 2)

			#update the image variable on the GUI application
			imgbytes = cv2.imencode(".png", image)[1].tobytes()
			window["-IMAGE-"].update(data=imgbytes)

			#cv2.imshow("inference window", image)
			#cv2.waitKey(0)

	window.close()   #close the image viewer