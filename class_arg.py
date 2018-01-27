MenuS, GameS = range(2)

class Arg:
    def __init__(self):
        self.screen = None
        self.game_area = None
        self.stats = None
        self.menu = []

        self.bot = None
        self.population = None

        self.settings = None
        self.mouse_pos = None
        self.collided = False

        self.time = 1
        self.speed_count = 0
        self.fps_count = 0

        self.wide_button_flag = False
        self.radius = 0
        self.image_name = None
        self.top_space = 0
        self.left_space = 0

        self.menu_width = 300
        self.menu_height = 300

        # Меню с номером ноль это начальное меню (ещё нет но через десяток строк появится)
        self.id_menu = 0
        self.prev_id_menu = 0
        self.state_flag = MenuS


