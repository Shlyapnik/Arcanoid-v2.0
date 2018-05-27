from game_functions import collide_circle_rect

BallWall, BallPlatform, BallBlock, NoColl = range(4)

def keep_nearest_blocks(arg):
    arg.nearest = list()
    for block in arg.blocks.sprites():
        arg.nearest.append(block)

class Collision:
    def __init__(self, type_coll):
        self.top_wall = False
        self.left_wall = False
        self.right_wall = False
        self.bottom_wall = False

        self.block = False

        self.type = type_coll

        self.point_coll = [-1, -1]

def get_coll_state(arg, alpha):
    b_point, e_point, radius = arg.ball.fake_update(alpha)
    b_rect, e_rect = arg.platform.fake_update(alpha)
    blocks = arg.nearest.copy()

    coll_state = []
    # Проверка на коллизии шар/блоки
    for block in blocks:
        state = Collision(BallBlock)
        state.point_coll = collide_circle_rect(e_point, block.rect, radius)

        if state.point_coll != [-1, -1]:
            coll_state.append(state)
            
    
    # Проверка на коллизии шар/платформа
    if arg.ball.thrown:
        state = Collision(BallPlatform)

        for circle in [b_point, e_point]:
            for rect in [b_rect, e_rect]:
                state.point_coll = collide_circle_rect(circle, rect, radius)

                if state.point_coll != [-1, -1]:
                    break
            
            if state.point_coll != [-1, -1]:
                break
        
        if state.point_coll != [-1, -1]:
            coll_state.append(state)
                

    # Проверка на коллизии шар/стены
    state = Collision(BallWall)
    left_wall, right_wall = 0, arg.game_area.rect.width
    top_wall, bottom_wall =  0, arg.game_area.rect.height

    if e_point[0] - radius < left_wall:
        state.left_wall = True

    if e_point[0] + radius >= right_wall:
        state.right_wall = True

    if e_point[1] - radius < top_wall:
        state.top_wall = True
    
    # if e_point[1] - radius > bottom_wall:
    #     state.bottom_wall = True

    if state.top_wall or state.left_wall or state.right_wall or state.bottom_wall:
        coll_state.append(state)

    # Проверка на коллизии платформа/стены (Но это не точно)


    return coll_state

def check_for_coll(arg, alpha):
    coll_state = get_coll_state(arg, alpha)

    return len(coll_state) != 0


def real_update(arg, alpha):
    arg.platform.update(alpha)
    arg.ball.update(alpha)

def norm(vec):
    result = 0

    result = sum(item ** 2 for item in vec) ** 0.5

    return result

def normalize(vec):
    mod_vec = norm(vec)

    result_vec = [item / mod_vec for item in vec]

    return result_vec

def detect_coll_and_change(arg, eps):
    coll_state = get_coll_state(arg, eps)

    if len(coll_state) != 0:
        print("Length of coll = {}".format(len(coll_state)))

    for state in coll_state:
        if state.type == NoColl:
            return
        elif state.type == BallWall:
            if state.top_wall:
                arg.ball.velocity[1] *= -1
            
            if state.left_wall or state.right_wall:
                arg.ball.velocity[0] *= -1

            # if state.bottom_wall:
            #     arg.wasted = True

        elif state.type == BallPlatform:
            # old_vel = arg.ball.velocity
            new_vel = [state.point_coll[i] - arg.platform.center[i] for i in range(2)]
            new_vel[0] /= 2
            new_vel = normalize(new_vel)

            if arg.ball.center[1] > arg.platform.center[1] + 2:
                new_vel[1] += 0.2
                new_vel = normalize(new_vel)
            

            print("old vel {}".format(arg.ball.velocity))
            # new_vel = [new_vel[i] + old_vel[i] for i in range(2)]
            # new_vel = normalize(new_vel)
            arg.platform.freeze()
            arg.ball.velocity = new_vel
            print("new vel {}".format(arg.ball.velocity))

        elif state.type == BallBlock:
            if state.point_coll == [-1, -1]:
                print("What the fuck!!!")

            vel = arg.ball.velocity
            print(state.point_coll)
            basis = [state.point_coll[i] - arg.ball.center[i] for i in range(2)]

            basis = normalize(basis)

            projection = sum([vel[i] * basis[i] for i in range(2)])
            # print(vel)
            print("old_vel = {}".format(vel))
            new_vel = [vel[i] - 2.0 * projection * basis[i] for i in range(2)]
            # print("Not normlized vel = {}".format(new_vel))
            new_vel = normalize(new_vel)
            print("new_vel = {}".format(new_vel))

            arg.ball.velocity = new_vel
