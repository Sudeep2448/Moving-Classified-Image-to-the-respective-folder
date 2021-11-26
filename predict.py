from tensorflow.keras.models import load_model
import argparse
import pickle
import cv2
import GUI
import pathlib
import os
import random
catcount=0
dogcount=0
pandacount=0
elephantcount=0
tigercount=0
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",help="path to input image we are going to classify")
ap.add_argument("-m", "--model",help="path to trained Keras model")
ap.add_argument("-l", "--picklefile",help="path to label binarizer")
ap.add_argument("-w", "--width", type=int, default=64,	help="target spatial dimension width")
ap.add_argument("-e", "--height", type=int, default=64,	help="target spatial dimension height")
ap.add_argument("-f", "--flatten", type=int, default=-1,	help="whether or not we should flatten the image")
args = vars(ap.parse_args())

list_=GUI.fpath

# load the input image and resize it to the target spatial dimensions
lengthoflist=len(list_)
print("lengthoflist=" , lengthoflist)
for i in range(0,lengthoflist):
	args["image"] = list_[lengthoflist-1]
	lengthoflist-=1
	print(args["image"])
	args["model"] = "output/smallvggnet.model"
	args["picklefile"] = "output/smallvggnet_lb.pickle"
	image = cv2.imread(args["image"])
	output = image.copy()
	image = cv2.resize(image, (args["width"], args["height"]))

	# scale the pixel values to [0, 1]
	image = image.astype("float") / 255.0

	# check to see if we should flatten the image and add a batch
	# dimension
	if args["flatten"] > 0:
		image = image.flatten()
		image = image.reshape((1, image.shape[0]))

	# otherwise, we must be working with a CNN -- don't flatten the
	# image, simply add the batch dimension
	else:
		image = image.reshape((1, image.shape[0], image.shape[1],
							   image.shape[2]))

	# load the model and label binarizer
	print("[INFO] loading network and label binarizer...")
	model = load_model(args["model"])
	lb = pickle.loads(open(args["picklefile"], "rb").read())

	# make a prediction on the image
	preds = model.predict(image)

	# find the class label index with the largest corresponding
	# probability
	i = preds.argmax(axis=1)[0]
	label = lb.classes_[i]

	path = pathlib.Path.home() / 'Desktop'
	path = r'{}'.format(path) + r"\{}".format(label)  # c://user//desktop//dog
	checkfolder = os.path.isdir(path)  # false
	if not checkfolder:
		os.makedirs(path)  # creates the folder dog
	img = cv2.imread(args["image"], 1)  # d://downloads//dog
	for i in range(0, 100):
		rannum = random.randint(0, 10000)
		if (not os.path.exists("{}{}.jpg".format(label, rannum) or os.path.exists("{}{}.png".format(label, rannum)))):
			cv2.imwrite(os.path.join(path, "{}{}.jpg".format(label, rannum)), img)
			break

	# draw the class label + probability on the output image
	text = "{}: {:.2f}%".format(label, preds[0][i] * 100)
	cv2.putText(output, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
		(0, 0, 255), 2)
