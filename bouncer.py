import cv2
import os
from google.cloud import vision

# 1. TELL PYTHON WHERE YOUR PASSWORD IS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/sidra/smart_bin/key.json.json"

# 2. CONNECT TO GOOGLE CLOUD
print("Connecting to Google Cloud...")
client = vision.ImageAnnotatorClient()

# 3. TURN ON THE WEBCAM
print("Starting up the Smart Bin...")
cap = cv2.VideoCapture(0) 

# --- NEW: Variables to store what we draw on the screen ---
status_text = "Press SPACE to Scan"
status_color = (255, 255, 255) # Start with White

print("✅ READY! Hold up some trash and press SPACEBAR. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    
    # --- NEW: Draw a border around the video feed ---
    # cv2 uses BGR (Blue, Green, Red) colors instead of RGB
    height, width, _ = frame.shape
    cv2.rectangle(frame, (0, 0), (width, height), status_color, 15)
    
    # --- NEW: Write the status text directly on the video feed ---
    cv2.putText(frame, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, status_color, 3)
    
    # Show the upgraded video feed
    cv2.imshow('Smart Bin Sentry', frame)
    
    key = cv2.waitKey(1)
    
    if key == 32:
        status_text = "Scanning..."
        status_color = (0, 255, 255) # Yellow while thinking
        
        # We have to update the window immediately to show "Scanning..."
        cv2.putText(frame, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, status_color, 3)
        cv2.imshow('Smart Bin Sentry', frame)
        cv2.waitKey(1) 
        
        cv2.imwrite('trash_pic.jpg', frame)
        
        # --- SEND TO GOOGLE CLOUD VISION ---
        with open('trash_pic.jpg', 'rb') as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        label_names = [label.description.lower() for label in labels]
        print(f"Google sees: {label_names}")
        
        # --- THE BOUNCER LOGIC ---
        allowed_paper_words = ['paper', 'cardboard', 'document', 'box', 'packaging', 'newspaper', 'receipt']
        is_paper = any(word in label_names for word in allowed_paper_words)
        
        # --- NEW: Change the screen colors based on the result! ---
        if is_paper:
            status_text = "GREEN LIGHT: PAPER ALLOWED!"
            status_color = (0, 255, 0) # Green
            print("🟢 GREEN LIGHT")
        else:
            status_text = "RED LIGHT: WRONG BIN!"
            status_color = (0, 0, 255) # Red
            print("🔴 RED LIGHT")
            
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()