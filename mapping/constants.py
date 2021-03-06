# Plotting constants
MAX_INTENSITY = 1
POINT_RADIUS = 10

# Color constants
POINT_TRANSPARENCY = 0.8
LAYER_TRANSPARENCY = 0.3
DEFAULT_GRADIENT = None
BLUE_GRADIENT = [(0, 0, 0, 0), (0, 0, 128, POINT_TRANSPARENCY),
                 (0, 0, 255, POINT_TRANSPARENCY)]
YELLOW_GRADIENT = [(0, 0, 0, 0), (128, 128, 0, POINT_TRANSPARENCY),
                   (255, 255, 0, POINT_TRANSPARENCY)]
RED_GRADIENT = [(0, 0, 0, 0), (128, 0, 0, POINT_TRANSPARENCY),
                (255, 0, 0, POINT_TRANSPARENCY)]
GREEN_GRADIENT = [(0, 0, 0, 0), (0, 128, 0, POINT_TRANSPARENCY),
                  (0, 255, 0, POINT_TRANSPARENCY)]
GRAY_GRADIENT = [(0, 0, 0, 0), (192, 192, 192, POINT_TRANSPARENCY),
                 (128, 128, 128, POINT_TRANSPARENCY)]
ORANGE_GRADIENT = [(0, 0, 0, 0), (204, 102, 0, POINT_TRANSPARENCY),
                   (255, 128, 0, POINT_TRANSPARENCY)]
PURPLE_GRADIENT = [(0, 0, 0, 0), (153, 51, 255, POINT_TRANSPARENCY),
                   (102, 0, 204, POINT_TRANSPARENCY)]
CYAN_GRADIENT = [(0, 0, 0, 0), (0, 255, 255, POINT_TRANSPARENCY),
                 (0, 204, 204, POINT_TRANSPARENCY)]
MAGENTA_GRADIENT = [(0, 0, 0, 0), (255, 0, 255, POINT_TRANSPARENCY),
                    (204, 0, 204, POINT_TRANSPARENCY)]
COLOR_GRADIENTS = {"blue": BLUE_GRADIENT, "yellow": YELLOW_GRADIENT,
                   "red": RED_GRADIENT, "green": GREEN_GRADIENT,
                   "gray": GRAY_GRADIENT, "orange": ORANGE_GRADIENT,
                   "purple": PURPLE_GRADIENT, "cyan": CYAN_GRADIENT,
                   "magenta": MAGENTA_GRADIENT}
COLOR_GRADIENTS_LIST = [BLUE_GRADIENT, YELLOW_GRADIENT, RED_GRADIENT,
                        GREEN_GRADIENT, GRAY_GRADIENT, ORANGE_GRADIENT,
                        PURPLE_GRADIENT, CYAN_GRADIENT, MAGENTA_GRADIENT]

# CSV file keys-columns translator
CSV_FORMAT_TRANSLATOR = {"Population": 1,
                         "Density": 2,
                         "Area": 3}
