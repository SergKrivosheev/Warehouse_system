from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.cursor import Cursor
from ursina.ursinastuff import _destroy
import time
import copy


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.fps_counter.enabled = False
        window.fullscreen = False
        EditorCamera()
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray, collider="box")  # plane
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, 0)
        self.cursor = Cursor(parent=camera.ui)
        self.player = FirstPersonController()
        self.t = 0

        self.src_coord = Vec3(x=0, y=0, z=2)
        self.dst_coord = Vec3(x=2, y=4, z=0)
        self.free_cube = Vec3(x=0, y=1, z=2)

        # self.high = 0
        # self.width = 0
        # self.depth = 0
        self.CUBES = list()
        self.start_screen()
        # self.load_game()

    def start_screen(self):

        self.player.disable()
        self.inp_hi = InputField(y=+.12, label='high', default_value='5', max_lines=1, character_limit=5)
        self.inp_wi = InputField(y=+.18, label='width', default_value='5', max_lines=1, character_limit=5)
        self.inp_de = InputField(y=+.24, label='depth', default_value='5', max_lines=1, character_limit=5)

        self.start_screen_layout = Button(on_click=self.load_game, text='go')

    def start_screen_off(self):
        self.inp_hi.visible = False
        self.inp_wi.visible = False
        self.inp_de.visible = False

        self.high = int(self.inp_hi.text)
        self.width = int(self.inp_wi.text)
        self.depth = int(self.inp_de.text)

        self.player.enable()

        self.start_screen_layout.visible = False

    def load_game(self):

        self.start_screen_off()

        for x in range(0, self.width):
            for y in range(0, self.high):
                for z in range(0, self.depth):
                    if self.free_cube.x == x and self.free_cube.y == y and self.free_cube.z == z:
                        continue
                    cube = Button(position=Vec3(x=x, y=y, z=z), color=color.orange, highlight_color=color.lime,
                                  model='cube', origin_y=0.5, parent=scene, texture='assets/wood'
                                  )
                    self.CUBES.append(cube)


    def moving(self):
        # free space is always under src cube

        # find index of src
        for i in range(0, len(self.CUBES)):
            if self.CUBES[i].position == self.src_coord:
                cube_index = i
                break


        # y
        if self.CUBES[cube_index].y > self.dst_coord.y:
            delta_y = -1
        else:
            delta_y = 1

        if self.CUBES[cube_index].z < self.width:
            delta_z = 1
        else:
            delta_z = -1

        while(self.CUBES[cube_index].y != self.dst_coord.y):

            # src cube move into free space
            src_pos_prev = self.CUBES[cube_index].position
            self.CUBES[cube_index].position = Vec3(x=src_pos_prev.x, y=src_pos_prev.y + delta_y, z=src_pos_prev.z)
            # 1 cube
            above_rl = Vec3(x=src_pos_prev.x, y=src_pos_prev.y, z=src_pos_prev.z + delta_z)
            for i in range(0, len(self.CUBES)):
                if self.CUBES[i].position == above_rl:
                    self.CUBES[i].position = src_pos_prev
                    break

            # 2 cube
            rl = Vec3(x=self.CUBES[cube_index].x, y=self.CUBES[cube_index].y, z=self.CUBES[cube_index].z + delta_z)
            for i in range(0, len(self.CUBES)):
                if self.CUBES[i].position == rl:
                    self.CUBES[i].position = above_rl
                    break

            # 3 cube
            under_rl = Vec3(x=self.CUBES[cube_index].x, y=self.CUBES[cube_index].y + delta_y, z=self.CUBES[cube_index].z + delta_z)
            for i in range(0, len(self.CUBES)):
                if self.CUBES[i].position == under_rl:
                    self.CUBES[i].position = rl
                    break

            # 4 cube under
            under_src = Vec3(x=self.CUBES[cube_index].x, y=self.CUBES[cube_index].y + delta_y, z=self.CUBES[cube_index].z)
            for i in range(0, len(self.CUBES)):
                if self.CUBES[i].position == under_src:
                    self.CUBES[i].position = under_rl
                    break

        self.t = 1


    def input(self, key, is_raw=False):
        '''if key == 'a' and len(self.CUBES):
            self.CUBES[0].x = self.CUBES[0].x + 1'''

        if key == 'v':
            prev_free_cube = self.CUBES[0].position
            self.CUBES[0].position = self.free_cube
            self.free_cube = prev_free_cube

        if key == 'r':
            # self.CUBES.remove(self.CUBES[0])
            _destroy(self.CUBES[0], force_destroy=True)
            self.CUBES.remove(self.CUBES[0])
            # self.CUBES[0].disabled = True

        if key == 'x':
            print(self.CUBES[1].x, self.CUBES[1].y, self.CUBES[1].z, sep=' ')
            self.CUBES[1].x += 1
            time.sleep(1)

        if key == 'y':
            print(self.CUBES)
            print(self.CUBES[1].x, self.CUBES[1].y, self.CUBES[1].z, sep = " ")
            self.CUBES[1].y += 0.5

        if key == 'z':
            print(self.CUBES[1].x, self.CUBES[1].y, self.CUBES[1].z, sep=' ')
            self.CUBES[1].z += 1

        if key == 'a':
            camera.x -= 1

        if key == "d":
            camera.x += 1

        if key == "w":
            camera.rotation_y += 1

        if key == "s":
            camera.rotation_y -= 1

        if key == "p":
            if self.t == 0:
                self.moving()

        super().input(key, is_raw)



    def select_box(self):
        print()


if __name__ == '__main__':
    # input_field = InputField()
    game = Game()

    game.run()
