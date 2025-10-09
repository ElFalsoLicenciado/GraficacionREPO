import cv2
import numpy as np

# Function to generate Fibonacci sequence up to n terms
def fibonacci(n):
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq

# Parameters
terms = 15  # how many Fibonacci numbers to show
fib_seq = fibonacci(terms)
width, height = 800, 600

# Create white background
img = np.ones((height, width, 3), dtype=np.uint8) * 255

# Display Fibonacci numbers one by one
y = 50
for i, num in enumerate(fib_seq):
    # Clear background
    img[:] = 255
    
    # Write current Fibonacci number
    cv2.putText(img, f"F({i}) = {num}", (50, y), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0, 0, 0), 3, cv2.LINE_AA)

    cv2.imshow("Fibonacci Series", img)
    
    # Wait a bit before showing next
    if cv2.waitKey(1000) & 0xFF == 27:  # ESC to exit
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
