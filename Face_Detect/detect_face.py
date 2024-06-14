from random import randint
import cv2
import sys
import os
import traceback
      
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image_path, output_folder, display=True):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to load image at {image_path}")

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    try:
        faces = FACE_CASCADE.detectMultiScale(image_gray, scaleFactor=1.16, minNeighbors=5, minSize=(25, 25), flags=0)
    except cv2.error as e:
        print(f"OpenCV Error: {e}")
        return

    # Initialize variables to keep track of the largest face
    max_area = 0
    max_face = None

    # Iterate through detected faces to find the largest one
    for (x, y, w, h) in faces:
        face_area = w * h
        if face_area > max_area:
            max_area = face_area
            max_face = (x, y, w, h)

    # If a face was found, extract and save it
    if max_face is not None:
        x, y, w, h = max_face
        sub_img = image[y-10:y+h+10, x-10:x+w+10]
        output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(image_path))[0]}_extracted_img.png")
        cv2.imwrite(output_file, sub_img)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)

    if display:
        cv2.imshow("Faces Found", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
	
	if not "Extracted" in os.listdir("."):
		os.mkdir("Extracted")
    
	if len(sys.argv) < 2:
		print("Usage: python Detect_face.py 'image path'")
		sys.exit()

	if os.path.isdir(sys.argv[1]):
		for image in os.listdir(sys.argv[1]):
			try:
				print ("Processing.....",os.path.abspath(os.path.join(sys.argv[1],image)))
				detect_faces(os.path.abspath(os.path.join(sys.argv[1],image)),False)
			except Exception:
				print ("Could not process ",os.path.abspath(os.path.join(sys.argv[1],image)))
	else:
		detect_faces(sys.argv[1])
