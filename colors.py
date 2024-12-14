class Colors:
    dark_grey = (26, 31, 40)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.white, cls.dark_blue, cls.light_blue]
    