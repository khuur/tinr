
def collisionDetection(object1, object2, be):
    # Returns True if object ARE IN eachother
    return False
    """
    if object1.name == object2.name:
        return False

    sum_r = object1.r + object2.r  # Sum of both radius
    distance = euclideanDistance(object1, object2)  # Actual distance between objects

    # if radius is larger than acutal distance, means that they are colideing
    return sum_r > distance
"""


def getImage(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def euclideanDistance(object1, object2):
    x1 = object1.x
    y1 = object1.y
    x2 = object2.x
    y2 = object2.y

    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


