import cv2
import pytesseract
from pytesseract import Output


def process_file(image):
    #path = 'test1.jpg'
    #image = cv2.imread(path)

    print('The shape of the image is:')
    print(image.shape)

    show_img_wait_key(image)
    cropped = crop_file(image)
    show_img_wait_key(cropped)
    get_user_name(cropped)


def show_img_wait_key(img):
    cv2.imshow("image", img)
    # Maintain output window until user presses a key
    cv2.waitKey(0)
    # Destroying present windows on screen
    cv2.destroyAllWindows()


def crop_file(image):
    # (2400, 1080, 3)
    # 1280, 576, 3)

    original_height = image.shape[0]
    original_width = image.shape[1]

    x1 = int(100 * original_height / 2400)
    x2 = int(175 * original_height / 2400)
    y1 = int(270 * original_width / 1080)
    y2 = int(830 * original_width / 1080)

    # cropped_user_logo = image[110:200, 150:230].copy()
    cropped_user_name = image[x1:x2, y1:y2].copy()
    return cropped_user_name


def pytesseract_read_img(img):
    print('Start reading image with pytesseract')
    #pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

    # configuring parameters for tesseract
    custom_config = r'--oem 3 --psm 6'
    # now feeding image to tesseract
    details = pytesseract.image_to_data(img, output_type=Output.DICT, config=custom_config, lang='eng')
    print(details.keys())
    print(details)
    return details


def get_user_name(user_name_img):
    details = pytesseract_read_img(user_name_img)
    print('Text from image:')
    print(details['text'])
    # print(details)
    conf_threshold = 30  # this is the confidence from 0 to 100 from pytesseract
    text_list = [details['text'][i] for i, item in enumerate(details['conf']) if int(item) > conf_threshold]
    parsed_text = ''.join(text_list)

    print(parsed_text)
    return parsed_text