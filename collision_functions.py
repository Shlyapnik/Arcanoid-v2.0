from game_functions import collide_circle_rect

BallWall, BallPlatform, BallBlock, NoColl = range(4)

def keep_nearest_blocks(arg):
    arg.nearest = list()
    for block in arg.blocks.sprites():
        width, height = block.rect.width / 2, block.rect.height / 2
        max_len_from_center = sum([width ** 2, height ** 2]) ** 0.5
        ness_dist = max_len_from_center + arg.radius * 2 + arg.ball.alpha_velocity

        dist = sum([
            (block.rect.centerx - arg.ball.rect.centerx) ** 2,
            (block.rect.centery - arg.ball.rect.centery) ** 2
        ]) ** 0.5

        if dist < ness_dist:
            arg.nearest.append(block)

class Collision:
    def __init__(self, type_coll):
        self.top_wall = False
        self.left_wall = False
        self.right_wall = False
        self.bottom_wall = False

        self.block = None

        self.type = type_coll

        self.point_coll = [-1, -1]

def get_coll_state(arg, alpha):
    b_point, e_point, radius = arg.ball.fake_update(alpha)
    ball_vec = [e_point[i] - b_point[i] for i in range(2)]
    b_rect, e_rect = arg.platform.fake_update(alpha)
    blocks = arg.nearest.copy()

    coll_state = []

    # Проверка на коллизии шар/блоки
    # if len(blocks) != 0:
    #     print(len(blocks))
    for block in blocks:
        state = Collision(BallBlock)
        state.point_coll = collide_circle_rect(e_point, block.rect, radius)

        coll_flag = False
        if (norm(ball_vec) > 0.001 and 
            collide_thick_segment_rect([b_point, e_point], block.rect, radius)):
            coll_flag = True

        if state.point_coll != [-1, -1] or coll_flag:
            state.block = block
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
        

        coll_flag = False
        for rect in [b_rect, e_rect]:
            if (norm(ball_vec) > 0.001 and 
                collide_thick_segment_rect([b_point, e_point], rect, radius)):
                coll_flag = True

        if state.point_coll != [-1, -1] or coll_flag:
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

    # if len(coll_state) != 0:
    #     print("Length of coll = {}".format(len(coll_state)))

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
            

            # print("old vel {}".format(arg.ball.velocity))
            # new_vel = [new_vel[i] + old_vel[i] for i in range(2)]
            # new_vel = normalize(new_vel)
            arg.platform.freeze()
            arg.ball.velocity = new_vel
            # print("new vel {}".format(arg.ball.velocity))

        elif state.type == BallBlock:
            if state.point_coll == [-1, -1]:
                print("What the fuck!!!")

            vel = arg.ball.velocity
            # print(state.point_coll)
            basis = [state.point_coll[i] - arg.ball.center[i] for i in range(2)]

            basis = normalize(basis)

            projection = sum([vel[i] * basis[i] for i in range(2)])
            # print(vel)
            # print("old_vel = {}".format(vel))
            new_vel = [vel[i] - 2.0 * projection * basis[i] for i in range(2)]
            # print("Not normlized vel = {}".format(new_vel))
            new_vel = normalize(new_vel)
            # print("new_vel = {}".format(new_vel))
            arg.blocks.remove(state.block)

            arg.ball.velocity = new_vel

def sum_vec(a, b):
    result = [a[i] + b[i] for i in range(min(len(a), len(b)))]

    return result


def make_line(p1, p2):
    # print("p1-p2")
    # print(p1)
    # print(p2)
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = - a * p1[0] - b * p1[1]

    return [a, b, c]

def place_in_line(line, point):
    result = line[0] * point[0] + line[1] * point[1] + line[2]

    return result

def collide_seg_seg(first, second):
    # print("first-second")
    # print(first)
    # print(second)
    first_line = make_line(*first)
    second_line = make_line(*second)

    first_place_in = [place_in_line(first_line, second[i]) for i in range(2)]
    second_place_in = [place_in_line(second_line, first[i]) for i in range(2)]

    result = False
    if (first_place_in[0] * first_place_in[1] < 0 and
        second_place_in[0] * second_place_in[1] < 0):
        result = True

    return result



def collide_thick_segment_rect(segment, rect, thick):
    vec = [segment[1][i] - segment[0][i] for i in range(2)]
    vec = normalize(vec)

    rect_segs = []
    xs = [rect.left, rect.right]
    ys = [rect.bottom, rect.top]
    rect_segs.append([[xs[0], ys[0]], [xs[0], ys[1]]])
    rect_segs.append([[xs[0], ys[0]], [xs[1], ys[0]]])
    rect_segs.append([[xs[1], ys[1]], [xs[0], ys[1]]])
    rect_segs.append([[xs[1], ys[1]], [xs[1], ys[0]]])

    seg_segs = []
    normal = [vec[1] * thick, -vec[0] * thick]
    tps = [sum_vec(segment[i], normal) for i in range(2)]

    normal = [-item for item in normal]
    bps = [sum_vec(segment[i], normal) for i in range(2)]

    seg_segs.append([bps[0], bps[1]])
    seg_segs.append([tps[0], tps[1]])
    seg_segs.append([bps[0], tps[0]])
    seg_segs.append([bps[1], tps[1]])
    # seg_segs.append([[bps[0], tps[0]], [bps[0], [tps[1]]]])
    # seg_segs.append([[bps[0], tps[0]], [bps[1], [tps[0]]]])
    # seg_segs.append([[bps[1], tps[1]], [bps[0], [tps[1]]]])
    # seg_segs.append([[bps[1], tps[1]], [bps[1], [tps[0]]]])

    result = False
    for rect_seg in rect_segs:
        for seg_seg in seg_segs:
            if collide_seg_seg(rect_seg, seg_seg):
                result = True
                break
        if result:
            break
    
    return result
