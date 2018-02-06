

def keep_nearest_blocks(arg):
    arg.nearest = list()
    for block in arg.blocks.sprites():
        arg.nearest.append(block)


def check_for_coll(arg, alpha):
    b_point, e_point, radius = arg.ball.fake_update(alpha)
    b_rect, e_rect = arg.platform.fake_update(alpha)
    blocks = arg.nearest.copy()

    # Проверка на коллизии шар/блоки
    

    # Проверка на коллизии шар/платформа


    # Проверка на коллизии шар/стены
    

    # Проверка на коллизии платформа/стены (Но это не точно)


    return False


def real_update(arg, alpha):
    arg.ball.update(alpha)
    arg.platform.update(alpha)


def detect_coll_and_change(arg):
    pass