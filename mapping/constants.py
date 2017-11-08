# Plotting constants
MAX_INTENSITY = 1
POINT_RADIUS = 10

# Color constants
TRANSPARENCY = 0.7
DEFAULT_GRADIENT = None
BLUE_GRADIENT = [(0, 0, 0, 0), (0, 0, 128, TRANSPARENCY),
                 (0, 0, 255, TRANSPARENCY)]
YELLOW_GRADIENT = [(0, 0, 0, 0), (128, 128, 0, TRANSPARENCY),
                   (255, 255, 0, TRANSPARENCY)]
RED_GRADIENT = [(0, 0, 0, 0), (128, 0, 0, TRANSPARENCY),
                (255, 0, 0, TRANSPARENCY)]
GREEN_GRADIENT = [(0, 0, 0, 0), (0, 128, 0, TRANSPARENCY),
                  (0, 255, 0, TRANSPARENCY)]
GRAY_GRADIENT = [(0, 0, 0, 0), (192, 192, 192, TRANSPARENCY),
                 (128, 128, 128, TRANSPARENCY)]
ORANGE_GRADIENT = [(0, 0, 0, 0), (204, 102, 0, TRANSPARENCY),
                   (255, 128, 0, TRANSPARENCY)]
PURPLE_GRADIENT = [(0, 0, 0, 0), (153, 51, 255, TRANSPARENCY),
                   (102, 0, 204, TRANSPARENCY)]
CYAN_GRADIENT = [(0, 0, 0, 0), (0, 255, 255, TRANSPARENCY),
                 (0, 204, 204, TRANSPARENCY)]
MAGENTA_GRADIENT = [(0, 0, 0, 0), (255, 0, 255, TRANSPARENCY),
                    (204, 0, 204, TRANSPARENCY)]
COLOR_GRADIENTS = {"blue": BLUE_GRADIENT, "yellow": YELLOW_GRADIENT,
                   "red": RED_GRADIENT, "green": GREEN_GRADIENT,
                   "gray": GRAY_GRADIENT, "orange": ORANGE_GRADIENT,
                   "purple": PURPLE_GRADIENT, "cyan": CYAN_GRADIENT,
                   "magenta": MAGENTA_GRADIENT, "default": DEFAULT_GRADIENT}
