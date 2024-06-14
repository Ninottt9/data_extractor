from random import randint
import cv2
import sys
import os
import traceback
      
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image_path, output_folder, display=True):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to load image at {image_path}")

    # Convert image to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = FACE_CASCADE.detectMultiScale(image_gray, scaleFactor=1.16, minNeighbors=5, minSize=(25, 25), flags=0)

    # Iterate through detected faces
    for i, (x, y, w, h) in enumerate(faces):
        # Extract the face region
        sub_img = image[y-10:y+h+10, x-10:x+w+10]

        # Generate output file name
        output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(image_path))[0]}_extracted_img_{i}.png")

        # Save the extracted face image
        cv2.imwrite(output_file, sub_img)

        # Draw rectangle around the face on the original image
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)

    # Display the image with rectangles around detected faces
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
