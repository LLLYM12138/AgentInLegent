import json
from legent import Environment, Action, Observation, ResetInfo, Controller, TaskCreator, TrajectorySaver, save_image
import os

# 'user.jpg','First Floor Cloakroom1.jpg', 'First Floor Cloakroom2.jpg',
#          'First Floor Living Room and Kitchen.jpg', 'Second Floor Bathroom1.jpg',
#          'Second Floor Bathroom2.jpg', 'Second Floor Bedroom1.jpg', 'Second Floor Bedroom2.jpg',
#          'Second Floor Cloakroom1.jpg', 'Second Floor Cloakroom2.jpg', 'Second Floor Corridor.jpg
# list1 = ['100.jpg', '101.jpg', '11.jpg', '110.jpg', '114.jpg', '13.jpg', '14.jpg',
#          '140.jpg', '141.jpg', '143.jpg', '144.jpg', '145.jpg', '16.jpg', '171.jpg',
#          '172.jpg', '175.jpg', '180.jpg', '182.jpg', '183.jpg', '184.jpg', '185.jpg',
#          '186.jpg', '188.jpg', '191.jpg', '192.jpg', '193.jpg', '194.jpg', '201.jpg',
#          '205.jpg', '206.jpg', '207.jpg', '208.jpg', '217.jpg', '218.jpg', '220.jpg',
#          '228.jpg', '229.jpg', '230.jpg', '241.jpg', '268.jpg', '272.jpg', '273.jpg',
#          '274.jpg', '279.jpg', '283.jpg', '284.jpg', '309.jpg', '310.jpg', '311.jpg',
#          '317.jpg', '319.jpg', '324.jpg', '328.jpg', '329.jpg', '333.jpg', '334.jpg',
#          '335.jpg', '337.jpg', '343.jpg', '344.jpg', '365.jpg', '373.jpg', '381.jpg',
#          '382.jpg', '388.jpg', '39.jpg', '405.jpg', '406.jpg', '410.jpg', '43.jpg',
#          '44.jpg', '48.jpg', '51.jpg', '6.jpg', '66.jpg', '67.jpg', '7.jpg', '71.jpg',
#          '78.jpg', '79.jpg', '8.jpg', '80.jpg', '81.jpg', '9.jpg', '93.jpg', '95.jpg',
#          '96.jpg', '99.jpg']


def get_room(pos):
    if -6.18 <= pos[0] <= 1.3 and pos[1] <= 2.5 and -5.01 <= pos[2] <= 2.60:
        room = "First Floor Living Room and Kitchen"  #
    elif -6.18 <= pos[0] <= -1.25 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 5.01:
        room = "First Floor Bathroom1"  #
    elif -1.25 <= pos[0] <= 3.65 and pos[1] <= 2.5 and 2.60 <= pos[2] <= 5.01:
        room = "First Floor Cloakroom1"
    elif 1.3 <= pos[0] <= 6.18 and pos[1] <= 2.5 and -5.01 <= pos[2] <= 0:
        room = "First Floor Bedroom1"  #
    elif 1.3 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 0 <= pos[2] <= 2.6:
        room = "First Floor Cloakroom2"  #
    elif 3.65 <= pos[0] <= 6.18 and pos[1] <= 2.5 and 2.6 <= pos[2] <= 5.01:
        room = "First Floor Bathroom2"  #
    elif -1.2 <= pos[0] <= 6.18 and pos[1] >= 2.5 and 0 <= pos[2] <= 5.01:
        room = "Second Floor Bedroom1"  #
    elif 3.67 <= pos[0] <= 6.18 and pos[1] >= 2.5 and -5.01 <= pos[2] <= 0:
        room = "Second Floor Bathroom1"
    elif -6.18 <= pos[0] <= -3.75 and pos[1] >= 2.5 and 2.6 <= pos[2] <= 5.01:
        room = "Second Floor Cloakroom1"
    elif (-3.75 <= pos[0] <= -1.2 and pos[1] >= 2.5 and -2.45 <= pos[2] <= 5.01) or \
            (-6.18 <= pos[0] <= -1.2 and pos[1] >= 2.5 and -2.45 <= pos[2] <= -0.15):
        room = "Second Floor Corridor"
    elif -1.2 <= pos[0] <= 3.67 and pos[1] >= 2.5 and -5.01 <= pos[2] <= 0:
        room = "Second Floor Bedroom2"  #
    elif -3.75 <= pos[0] <= -1.2 and pos[1] >= 2.5 and -5.01 <= pos[2] <= -2.45:
        room = "Second Floor Cloakroom2"  #
    elif -6.18 <= pos[0] <= -3.75 and pos[1] >= 2.5 and -5.01 <= pos[2] <= -2.45:
        room = "Second Floor Bathroom2"  #
    return room


robot = {
    "First Floor Living Room and Kitchen": [-1.1976431608200073, 0.1319998800754547, -4.5299391746521],
    "First Floor Bathroom1": [-0.18878842890262604, 0.1319998800754547, 0.2309245765209198],
    "First Floor Cloakroom1": [2.641841173171997, 0.13199952244758606, 4.531292915344238],
    "First Floor Bedroom1": [5.847576141357422, 0.1319998800754547, -4.481896877288818],
    "First Floor Cloakroom2": [2.2042901515960693, 0.13199952244758606, 2.1048526763916016],
    "First Floor Bathroom2": [4.261860370635986, 0.13199976086616516, 3.703007698059082],
    "Second Floor Corridor": [-2.5636794567108154, 3.131999969482422, 0.13945524394512177],
    "Second Floor Bedroom1": [0.5606305003166199, 3.1319994926452637, 4.489130020141602],
    "Second Floor Bathroom1": [5.850497722625732, 3.1319994926452637, -1.0864429473876953],
    "Second Floor Bedroom2": [3.361269474029541, 3.131999969482422, -2.1504874229431152],
    "Second Floor Bathroom2": [-5.835768222808838, 3.490466594696045, -4.6003031730651855],
    "Second Floor Cloakroom1":[-4,3.14,4]
}

open_list = ['open_95.jpg', 'open_134.jpg', 'open_309.jpg', 'open_26.jpg', 'open_144.jpg',
             'open_59.jpg', 'open_129.jpg', 'open_154.jpg', 'open_238.jpg', 'open_226.jpg',
             'open_156.jpg', 'open_413.jpg', 'open_416.jpg', 'open_143.jpg', 'open_132.jpg',
             'open_53.jpg', 'open_354.jpg', 'open_355.jpg', 'open_141.jpg', 'open_97.jpg',
             'open_135.jpg', 'open_412.jpg', 'open_235.jpg', 'open_222.jpg', 'open_58.jpg',
             'open_54.jpg', 'open_221.jpg', 'open_411.jpg', 'open_96.jpg', 'open_24.jpg',
             'open_310.jpg', 'open_225.jpg', 'open_45.jpg', 'open_25.jpg', 'open_155.jpg']
grab_list = ['grab_396.jpg', 'grab_358.jpg', 'grab_138.jpg', 'grab_24.jpg', 'grab_118.jpg', 'grab_221.jpg',
             'grab_267.jpg', 'grab_25.jpg', 'grab_394.jpg', 'grab_369.jpg', 'grab_356.jpg', 'grab_97.jpg',
             'grab_122.jpg', 'grab_236.jpg', 'grab_353.jpg', 'grab_411.jpg', 'grab_200.jpg', 'grab_412.jpg',
             'grab_167.jpg', 'grab_54.jpg', 'grab_119.jpg', 'grab_92.jpg', 'grab_108.jpg', 'grab_243.jpg',
             'grab_26.jpg', 'grab_154.jpg', 'grab_107.jpg', 'grab_234.jpg', 'grab_312.jpg', 'grab_397.jpg',
             'grab_120.jpg', 'grab_395.jpg', 'grab_380.jpg', 'grab_156.jpg', 'grab_168.jpg', 'grab_173.jpg',
             'grab_131.jpg', 'grab_242.jpg', 'grab_370.jpg', 'grab_111.jpg', 'grab_150.jpg', 'grab_58.jpg',
             'grab_276.jpg', 'grab_316.jpg', 'grab_153.jpg', 'grab_371.jpg', 'grab_398.jpg', 'grab_235.jpg',
             'grab_209.jpg', 'grab_155.jpg', 'grab_233.jpg', 'grab_104.jpg', 'grab_137.jpg', 'grab_103.jpg',
             'grab_134.jpg', 'grab_355.jpg', 'grab_151.jpg', 'grab_49.jpg', 'grab_222.jpg', 'grab_416.jpg',
             'grab_90.jpg', 'grab_210.jpg', 'grab_264.jpg', 'grab_59.jpg', 'grab_149.jpg', 'grab_413.jpg',
             'grab_22.jpg', 'grab_219.jpg', 'grab_53.jpg', 'grab_225.jpg', 'grab_387.jpg', 'grab_226.jpg',
             'grab_128.jpg', 'grab_132.jpg', 'grab_336.jpg', 'grab_129.jpg', 'grab_146.jpg', 'grab_238.jpg',
             'grab_354.jpg', 'grab_379.jpg', 'grab_130.jpg', 'grab_211.jpg', 'grab_392.jpg', 'grab_148.jpg',
             'grab_105.jpg', 'grab_152.jpg', 'grab_64.jpg', 'grab_135.jpg', 'grab_212.jpg', 'grab_237.jpg',
             'grab_91.jpg', 'grab_357.jpg', 'grab_106.jpg', 'grab_109.jpg', 'grab_372.jpg', 'grab_401.jpg',
             'grab_393.jpg', 'grab_174.jpg', 'grab_332.jpg', 'grab_265.jpg', 'grab_368.jpg', 'grab_147.jpg',
             'grab_384.jpg', 'grab_244.jpg', 'grab_414.jpg', 'grab_94.jpg', 'grab_199.jpg', 'grab_415.jpg',
             'grab_142.jpg', 'grab_348.jpg', 'grab_127.jpg', 'grab_63.jpg', 'grab_139.jpg', 'grab_45.jpg',
             'grab_126.jpg']
list1 = ['100.jpg', '101.jpg', '11.jpg', '110.jpg', '114.jpg', '13.jpg', '14.jpg',
         '140.jpg', '141.jpg', '143.jpg', '144.jpg', '145.jpg', '16.jpg', '171.jpg',
         '172.jpg', '175.jpg', '180.jpg', '182.jpg', '183.jpg', '184.jpg', '185.jpg',
         '186.jpg', '188.jpg', '191.jpg', '192.jpg', '193.jpg', '194.jpg', '201.jpg',
         '205.jpg', '206.jpg', '207.jpg', '208.jpg', '217.jpg', '218.jpg', '220.jpg',
         '228.jpg', '229.jpg', '230.jpg', '241.jpg', '268.jpg', '272.jpg', '273.jpg',
         '274.jpg', '279.jpg', '283.jpg', '284.jpg', '309.jpg', '310.jpg', '311.jpg',
         '317.jpg', '319.jpg', '324.jpg', '328.jpg', '329.jpg', '333.jpg', '334.jpg',
         '335.jpg', '337.jpg', '343.jpg', '344.jpg', '365.jpg', '373.jpg', '381.jpg',
         '382.jpg', '388.jpg', '39.jpg', '405.jpg', '406.jpg', '410.jpg', '43.jpg',
         '44.jpg', '48.jpg', '51.jpg', '6.jpg', '66.jpg', '67.jpg', '7.jpg', '71.jpg',
         '78.jpg', '79.jpg', '8.jpg', '80.jpg', '81.jpg', '9.jpg', '93.jpg', '95.jpg',
         '96.jpg', '99.jpg']
list2 = [39, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 61, 63, 64, 65, 66, 67, 68, 69, 70, 72, 74]
#47, 69, 70,72,
list2 =[10, 68, 389, 50, 70, 216, 4, 69, 196, 55, 322, 390, 187, 361, 166, 165, 113,
        40, 23, 318, 72, 181, 121, 41, 3, 124, 57, 169, 123, 203, 176, 27, 19, 271,
        2, 350, 56, 170, 82, 84, 163, 42, 15, 164, 112, 85, 391, 83, 161, 162, 275]
list2 = [87,42,330,402,40,399]
if __name__ == "__main__":
    with open("json/scene.json", 'r') as file:
        scene = json.load(file)
    photo_type = "object"

    env = Environment(env_path='auto')
    for object in list2:
        object = str(object)+".jpg"
        print(object)
        room = get_room(scene["instances"][int(object[:-4])]["position"])
        scene["agent"]["position"] = robot[room]
        obs: Observation = env.reset(ResetInfo(scene))

        saver = TrajectorySaver()
        task = {"solution": [f"goto({object[5:-4]})","interact()"], "task": "goto"}
        for i in range(8):
            try:
                controller = Controller(env, [f"goto({object[:-4]})","interact()"])
                traj = controller.collect_trajectory(task)
                if traj:
                    print(f'Complete task "{object}".', end=' ')
                    break
                else:
                    env.reset(ResetInfo(scene=scene))
                    if i >= 7:
                        print(f'Complete task "{object}" failed.', end=' ')
                        break

            except TypeError as e:
                if i >= 7:
                    print(e, end=' ')
                    break

        if photo_type == "object":
            action = Action()
            obs = env.step(action)
            # pos = [i for i in obs.game_states['player']['position'].values]
            # if get_room(pos) != "First Floor Bedroom1":
            #     print(scene["instances"][int(object[:-4])]["prefab"],"fail")
            #     continue
            action = Action()
            save_image(obs.image, os.path.join("D:\LYM python homework\legent", object))
            obs = env.step(action)
        elif photo_type == "open":
            action = Action()
            obs = env.step(action)
            #open
            action = Action(grab=True)
            obs = env.step(action)
            action = Action()
            save_image(obs.image, os.path.join("D:\LYM python homework\legent\KG\KG_test_3\image", object))
            obs = env.step(action)
        elif photo_type == "grab":
            action = Action()
            obs = env.step(action)
            # grab
            for _ in range(3):
                action = Action(grab=True)
                obs = env.step(action)
                if obs.game_states["agent_grab_instance"] == int(object[5:-4]):
                    break

            action = Action()
            if obs.game_states["agent_grab_instance"] == int(object[5:-4]):
                save_image(obs.image, os.path.join("D:\\LYM python homework\\legent",object))
            else:
                save_image(obs.image, os.path.join("D:\\LYM python homework\\legent",object))
            obs = env.step(action)


        obs: Observation = env.reset(ResetInfo(scene))
        print("\n")