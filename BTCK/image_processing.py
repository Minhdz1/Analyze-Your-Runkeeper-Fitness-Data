import cv2
import pytesseract

# Thiết lập đường dẫn tới file tesseract.exe (chỉ cần thiết cho Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_numbers_from_image(image_path):
    # Đọc hình ảnh từ đường dẫn
    image = cv2.imread(image_path)

    # Chuyển đổi hình ảnh sang ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Phát hiện và làm mờ cạnh
    edges = cv2.Canny(gray, 100, 200)

    # Tìm tất cả các contours trong hình ảnh
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Lặp qua tất cả các contours và trích xuất văn bản từ hình ảnh
    numbers = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = gray[y:y+h, x:x+w]
        config = '--psm 6'  # Mode 6: Assume a single uniform block of text
        number = pytesseract.image_to_string(roi, config=config)
        numbers.append(number.strip())

    return numbers
