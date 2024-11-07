import glob

import cv2

screen_sizes = {
    "general_screen": (640, 360),
    "stream_screen": (1280, 720),
    "ovv_screen": (320, 180),
}


def resize_image(cv_img, size):
    """
    Resize an image to a specific size.

    Args:
        cv_img (np.ndarray): The image to resize.
        size (tuple): The target size of the image.

    Returns:
        np.ndarray: The resized image.
    """
    cv_img = cv2.resize(cv_img, size, interpolation=cv2.INTER_AREA)
    return cv_img


# glob all images in the assets/pictures folder
# each image resize to 3 different sizes in the screen_sizes dict
# save the resized images in the assets/pictures/resized folder, named as original_name_new_size.jpg

if __name__ == "__main__":
    images = glob.glob("./assets/pictures/*.jpg")
    for image in images:
        cv_img = cv2.imread(image)
        for screen_name, size in screen_sizes.items():
            resized_img = resize_image(cv_img, size[::])
            cv2.imwrite(
                f"./assets/pictures/resized/{image.split('/')[-1].split('.')[0]}_{'x'.join([str(e) for e in screen_sizes[screen_name]])}.jpg",
                resized_img,
            )
