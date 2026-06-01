import global_values as g
import graphics as gfx
import pygame as p
import random
import asyncio
import os

import levels
import cameras
import players
import controls
import entities
import actions
import sounds
import gesture_input



import platform
if platform.system().lower() == "emscripten":
    platform.window.onbeforeunload = None

p.mixer.init()
sounds.load_sounds()
g.channel_list = sounds.ChannelList()
p.mixer.music.set_volume(0.5)

g.global_pipe = actions.Pipe("global")

g.screen = p.Surface((g.WIDTH, g.HEIGHT))
# Cửa sổ to hơn, tỉ lệ 16:9
DISPLAY_FLAGS = p.RESIZABLE | p.DOUBLEBUF

def resize_window(width, height):
    width = max(g.MIN_WINDOW_WIDTH, int(width))
    height = max(g.MIN_WINDOW_HEIGHT, int(height))
    g.WINDOW_WIDTH = width
    g.WINDOW_HEIGHT = height
    g.SCREEN_WIDTH = width
    g.SCREEN_HEIGHT = height
    g.full_screen = p.display.set_mode((g.WINDOW_WIDTH, g.WINDOW_HEIGHT), DISPLAY_FLAGS)

resize_window(g.WINDOW_WIDTH, g.WINDOW_HEIGHT)

gfx.Spritesheet("player_ss", 16,32)
gfx.Spritesheet("basic_enemy_ss", 16,32)
gfx.Spritesheet("recover_enemy_ss", 16,32)
gfx.Spritesheet("large_enemy_ss", 48,48)
gfx.Spritesheet("spider_enemy_ss", 32,16)

gfx.Spritesheet("structure_16_32_ss", 16,32)
gfx.Spritesheet("structure_32_32_ss", 32,32)
gfx.Spritesheet("structure_32_24_ss", 32,24)
gfx.Spritesheet("corpse_ss", 32, 32)
gfx.Spritesheet("button_ss", 8,8)
gfx.Spritesheet("med_button_ss", 12,12)
gfx.Spritesheet("large_button_ss", 32,16)
gfx.Spritesheet("end_ss", 64,64)

p.font.init()
g.fonts = {
    "font1_1": p.font.Font(os.path.join(g.FONTS_DIR, "Lo-Res 9 Narrow.ttf"), 9),
    "font_small": p.font.Font(os.path.join(g.FONTS_DIR, "Lo-Res 9 Narrow.ttf"), 7)
}

g.game_clock = p.time.Clock()



if random.random() < 0.2:
    p.display.set_caption("Heckrostation")
else:
    p.display.set_caption("Necrostation")
p.display.set_icon(gfx.load_image("icon"))


#menu
def choose_input_mode(mode):
    g.input_mode = mode
    if mode == "gesture":
        gesture_input.start()
        gesture_input.set_enabled(True)
        g.gesture_status = "Gesture webcam mode"
    else:
        gesture_input.set_enabled(False)
        g.gesture_status = ""
    start_game()

def start_game():
    reset()
    p.mixer.music.fadeout(500)
    g.active_states = set(("main",))
    g.current_level = g.levels["Cryo I"]
    levels.change_level(g.current_level, show_text=False)

    if not g.start_slides_shown:
        g.start_slides_shown = True
        controls.StartScreenControl()

def go_to_menu():
    reset()
    gesture_input.set_enabled(False)
    g.input_mode = "keyboard"
    g.active_states = set(("mainmenu",))
    sounds.play_main_music()

g.pause_control = None

def pause_game():
    """Dừng game, hien menu pause"""
    if "main" not in g.active_states:
        return
    if g.player.dead or g.player.fully_dead:
        return
    g.active_states = set(("pause",))
    g.player.control_locks += 1
    if g.pause_control and not g.pause_control.deleted:
        g.pause_control.delete()
    g.pause_control = controls.PauseMenuControl(start_game, go_to_menu)


g.player = players.Player()
# GIỮ NGUYÊN camera offset gốc vì WIDTH/HEIGHT không đổi
g.camera = cameras.Camera(g.player, (-32, -48 + 3))

def reset():
    #reset game
    for entity in g.elements.get("class_Entity", [])[:]:
        if entity != g.player:
            entity.delete()

    g.levels = {}

    for file_name in os.listdir(g.LEVELS_DIR):
        if file_name.endswith(".json") and not file_name.startswith("nolevel_"):
            levels.Level(file_name[:-5])

    for level in g.levels.values():
        level.linkup()
    g.power_diverted = False

    #reset elements:
    for popup in g.elements.get("class_Popup", []):
        popup.delete()
    for screen_control in g.elements.get("class_TextScreenControl", []) + g.elements.get("class_GraphicsScreenControl", []):
        screen_control.delete()

    #reset sound
    g.channel_list.stop_sounds()

    #reset player
    g.player.health = g.player.max_health
    g.player.dead = False
    g.player.fully_dead = False
    g.player.inventory.clear()
    g.player.x = 0
    g.player.control_locks = 0
    g.player.visible_override = None


def load_game():
    pass


#MAINMENU
controls.MainMenuControl()
rect = p.Rect(0, 0, 32, 16)
rect.centerx = g.screen_rect.centerx
rect.centery = 52
ss_anims = g.spritesheets["large_button_ss"].anims
controls.LabeledButton(rect, "START", lambda: setattr(g, "active_states", set(("modemenu",))), ss_anims[1][0], ss_anims[1][1], ss_anims[1][2], set(("mainmenu",)))

# HOW TO PLAY button
rect_htp = rect.copy()
rect_htp.centery = 64
def show_how_to_play():
    bg_surf = gfx.get_surface("text_screen_background")
    bg_rect = p.Rect(0, 0, bg_surf.get_width(), bg_surf.get_height())
    bg_rect.center = g.screen_rect.center
    controls.TextScreenControl(bg_rect, "font1_1", HOW_TO_PLAY_TEXT, set(("mainmenu",)), scroll_space=200)

HOW_TO_PLAY_TEXT = """KEYBOARD:

A/D
 Move
LClick
 Fire
RClick
 Interact
E/Space
 Interact near
I
 Inventory
1-8
 Item slots
ESC
 Pause
G+H
 Heal (cheat)
G+T
 Minigun (cheat)

GESTURE:

Open hand
 Move pointer
Fist
 Attack
Index up
 Interact
Thumbs up
 Next item
Thumbs dn
 Prev item
Peace
 Inventory
F2
 Toggle cam"""

controls.LabeledButton(rect_htp, "HOW TO PLAY", show_how_to_play, ss_anims[2][0], ss_anims[2][1], ss_anims[2][2], set(("mainmenu",)))

rect = rect.copy()
rect.y -= 16

#INPUT MODE MENU
controls.InputModeMenuControl()
rect = p.Rect(0, 0, 32, 16)
rect.centerx = g.screen_rect.centerx
rect.centery = 42
controls.LabeledButton(rect, "KEYS", lambda: choose_input_mode("keyboard"), ss_anims[1][0], ss_anims[1][1], ss_anims[1][2], set(("modemenu",)))

rect = rect.copy()
rect.centery = 58
controls.LabeledButton(rect, "HAND", lambda: choose_input_mode("gesture"), ss_anims[1][0], ss_anims[1][1], ss_anims[1][2], set(("modemenu",)))

#GAMEOVER
controls.GameOverControl()
rect = p.Rect(0, 0, 32, 16)
rect.centerx = g.screen_rect.centerx
rect.centery = 48
controls.Button(rect, go_to_menu, ss_anims[2][0], ss_anims[2][1], ss_anims[2][2], set(("gameover", "end")))

#END
g.end_screen = controls.EndScreenControl()

#background
controls.BackgroundControl("space_background", set(("main",)))

#main
rect = p.Rect(0, 0, g.WIDTH, 8)
controls.GraphicsControl(rect, "controls_background", set(("main",)))

rect = p.Rect(0,0,15,8)
controls.MapControl(rect, set(("main",)))

rect = p.Rect(rect.right+1, 0, 32, 8)
controls.ItemControl(rect, set(("main",)))

rect = p.Rect(0, 0, 12, 8)
rect.topright = g.screen_rect.topright
controls.HealthControl(rect, set(("main",)))

rect = p.Rect(0, 0, 8, 8)
rect.bottomleft = g.screen_rect.bottomleft
def enter_inventory():
    g.active_states = set(("inventory",))
    g.player.control_locks += 1

def exit_menu():
    g.active_states = set(("main",))
    g.player.control_locks -= 1

g.inv_button = controls.Button(rect, enter_inventory, g.spritesheets["button_ss"].anims[0][0], g.spritesheets["button_ss"].anims[0][1], g.spritesheets["button_ss"].anims[0][2], set(("main",)))

#inventory
inventory_control = controls.InventoryControl(g.player.inventory, g.screen_rect, set(("inventory",)))

rect = p.Rect(0, 0, 8, 8)
rect.bottomleft = g.screen_rect.bottomleft
controls.Button(rect, exit_menu, g.spritesheets["button_ss"].anims[1][0], g.spritesheets["button_ss"].anims[1][1], g.spritesheets["button_ss"].anims[1][2], set(("inventory",)))

def handle_input():
    global RUNNING

    def press_accept_popup():
        for popup in reversed(g.elements.get("class_Popup", [])):
            if popup.active and getattr(popup, "show_accept", False):
                popup.button_accept.press()
                return True
        return False

    def press_pointed_button():
        best_button = None
        best_dist = None
        for button in reversed(g.elements["class_Button"]):
            if not button.active:
                continue
            if button.rect.collidepoint((g.mx, g.my)):
                button.press()
                return True
            dx = button.rect.centerx - g.mx
            dy = button.rect.centery - g.my
            dist = (dx * dx) + (dy * dy)
            if best_dist is None or dist < best_dist:
                best_button = button
                best_dist = dist
        if best_button and best_dist <= 16 * 16:
            best_button.press()
            return True
        return False

    def select_pointed_or_nearest_inventory_slot():
        best_index = None
        best_dist = None
        for index, slot in enumerate(g.player.inventory.slots):
            if not slot:
                continue
            col = index % 6
            row = index // 6
            x = 2 + (col * 12) + 5
            y = 10 + (row * 22) + 5
            dx = x - g.mx
            dy = y - g.my
            dist = (dx * dx) + (dy * dy)
            if best_dist is None or dist < best_dist:
                best_index = index
                best_dist = dist
        if best_index is not None:
            g.player.inventory.select_index(best_index)
            return True
        return False

    def select_inventory_step(step):
        slots = g.player.inventory.slots
        if not slots:
            return
        start = g.player.inventory.selected_index
        if start is None:
            start = 0 if step > 0 else len(slots) - 1
        for offset in range(1, len(slots) + 1):
            index = (start + (offset * step)) % len(slots)
            if slots[index]:
                g.player.inventory.select_index(index)
                return

    def handle_gesture_action(action):
        if action == gesture_input.ACTION_ATTACK:
            if press_pointed_button():
                return
            if "inventory" in g.active_states:
                select_pointed_or_nearest_inventory_slot()
            elif "main" in g.active_states:
                g.player.attack()
        elif action == gesture_input.ACTION_CONTEXT:
            if "inventory" in g.active_states:
                exit_menu()
            elif "main" in g.active_states:
                enter_inventory()
        elif action == gesture_input.ACTION_CONFIRM_ITEM:
            if press_pointed_button():
                return
            if "inventory" in g.active_states and inventory_control.highlighted_slot is not None:
                g.player.inventory.select_index(inventory_control.highlighted_slot)
            elif "inventory" in g.active_states:
                select_pointed_or_nearest_inventory_slot()
            elif "main" in g.active_states:
                interact(closest=True)
        elif action == gesture_input.ACTION_PREV_ITEM:
            if "main" in g.active_states or "inventory" in g.active_states:
                select_inventory_step(-1)
        elif action == gesture_input.ACTION_NEXT_ITEM:
            if "main" in g.active_states or "inventory" in g.active_states:
                select_inventory_step(1)

    def interact(closest=False):
        command_triggered = False
        clicked_structure = None
        if g.current_level:
            if closest:
                closest_dist = None
                for structure in g.current_level.structures:
                    if structure.can_interact:
                        dist = abs(g.player.rect.centerx - structure.rect.centerx)
                        if closest_dist is None or dist < closest_dist:
                            closest_dist = dist
                            clicked_structure = structure
            else:
                for structure in g.current_level.structures:
                    if structure.can_interact and structure.rect.collidepoint((g.tmx, g.tmy)):
                        if not clicked_structure or (clicked_structure.rect.w*clicked_structure.rect.h) > (structure.rect.w*structure.rect.h):
                            clicked_structure = structure

            if clicked_structure:
                clicked_structure.interact()
                command_triggered = True

        if not command_triggered and not closest:
            if not g.player.control_locks:
                g.player_targeting = True
                g.player.set_target_x(g.tmx)
        return command_triggered

    for event in p.event.get():
        if event.type == p.QUIT:
            RUNNING = False
        elif event.type == p.VIDEORESIZE:
            resize_window(event.w, event.h)

        if event.type == gesture_input.ACTION_EVENT:
            handle_gesture_action(event.gesture_action)

        if event.type == p.MOUSEBUTTONDOWN:
            if event.button == 3:
                interact()

            elif event.button == 1:
                button_pressed = False
                seen_rects = set()
                for button in reversed(g.elements["class_Button"]):
                    if button.active and button.rect.collidepoint((g.mx, g.my)):
                        rect_key = (button.rect.x, button.rect.y, button.rect.w, button.rect.h)
                        if rect_key in seen_rects:
                            continue
                        seen_rects.add(rect_key)
                        button_pressed = True
                        button.press()
                        break

                if "inventory" in g.active_states:
                    if inventory_control.highlighted_slot is not None:
                        g.player.inventory.select_index(inventory_control.highlighted_slot)
                        button_pressed = True

                if not button_pressed:
                    if "main" in g.active_states:
                        g.player.attack()

        elif event.type == p.KEYDOWN:
            if event.key == p.K_ESCAPE:
                if "main" in g.active_states:
                    pause_game()
                elif "pause" in g.active_states:
                    # ESC lần nữa = chơi tiếp
                    if g.pause_control and not g.pause_control.deleted:
                        g.pause_control.resume()

            elif event.key == p.K_i:
                if "main" in g.active_states:
                    enter_inventory()
                elif "inventory" in g.active_states:
                    exit_menu()

            elif event.key == p.K_e or event.key == p.K_SPACE:
                button_pressed = False
                seen_rects = set()
                for button in reversed(g.elements["class_Button"]):
                    if button.active and button.rect.collidepoint((g.mx, g.my)):
                        rect_key = (button.rect.x, button.rect.y, button.rect.w, button.rect.h)
                        if rect_key in seen_rects:
                            continue
                        seen_rects.add(rect_key)
                        button_pressed = True
                        button.press()
                        break

                if not button_pressed:
                    interact(closest=True)

            elif p.K_1 <= event.key <= p.K_9:
                # Không xử lý phím số khi đang mở keypad
                keypad_open = bool(g.elements.get("class_Keypad_Popup", []))
                if ("main" in g.active_states or "inventory" in g.active_states) and not keypad_open:
                    index = event.key - p.K_1
                    g.player.inventory.select_index(index)

            elif event.key == p.K_F2:
                if g.input_mode == "gesture":
                    gesture_input.toggle()

        elif event.type == p.MOUSEWHEEL:
            for text in g.elements.get("class_TextScreenControl", []):
                if event.y > 0:
                    text.scroll_up()
                else:
                    text.scroll_down()


    g.keys = p.key.get_pressed()
    g.ml, g.mm, g.mr = p.mouse.get_pressed()

    if g.input_mode == "gesture" and gesture_input.is_enabled():
        g.mx, g.my = gesture_input.get_pointer_position(g.WIDTH, g.HEIGHT)
    else:
        g.mx, g.my = p.mouse.get_pos()
        g.mx *= (g.WIDTH / g.SCREEN_WIDTH)
        g.my *= (g.HEIGHT / g.SCREEN_HEIGHT)
        g.mx = max(0, min(g.WIDTH - 1, g.mx))
        g.my = max(0, min(g.HEIGHT - 1, g.my))

    g.tmx = g.mx + g.camera.x
    g.tmy = g.my + g.camera.y

    def key_held(key):
        return g.keys[key] or (g.input_mode == "gesture" and key in gesture_input._virtual_keys_held)

    if key_held(p.K_a):
        g.player.move(-g.player.speed*g.dt, 0)
        if g.player.target_x:
            g.player.set_target_x(None)
            g.player_targeting = False
    if key_held(p.K_d):
        g.player.move(g.player.speed*g.dt, 0)
        if g.player.target_x:
            g.player.set_target_x(None)
            g.player_targeting = False

    if g.mr and g.player_targeting:
        g.player.set_target_x(g.tmx)
    else:
        g.player_targeting = False

def update():
    if g.player.fully_dead and "gameover" not in g.active_states:
        g.active_states = set(("gameover",))
        g.channel_list.stop_sounds()
        p.mixer.music.fadeout(500)
        g.current_level = None

    i = 0
    while i < len(g.pipe_list):
        g.pipe_list[i].update()
        i += 1

    g.channel_list.update()

    in_main = "main" in g.active_states
    for element in g.element_list:
        if isinstance(element, entities.Entity):
            if in_main:
                if element.level == g.current_level:
                    element.update()
                else:
                    element.update_inactive()
            else:
                continue

        elif isinstance(element, controls.Control):
            if g.active_states.isdisjoint(element.active_states):
                element.active = False
                continue
            else:
                element.active = True
                element.update()

        else:
            element.update()

def sort_entity(entity):
    return entity.z_index

def draw():
    if "main" in g.active_states:
        if g.current_level:
            if g.current_level.show_space:
                for control in g.elements.get("class_BackgroundControl", []):
                    control.draw()

        if g.current_level:
            g.current_level.draw()

            for entity in sorted(g.elements.get("class_Entity", []), key=sort_entity):
                if entity.level != g.current_level:
                    continue
                if entity.visible_override is not False:
                    entity.draw()

    for control in g.elements.get("class_Control", []):
        if (control.visible_override is not False) and not g.active_states.isdisjoint(control.active_states) and not isinstance(control, controls.BackgroundControl):
            control.draw()

    for pipe in g.pipes.values():
        pipe.draw()

    if g.input_mode == "gesture" and gesture_input.is_enabled():
        gesture = gesture_input.get_last_gesture() or "NO HAND"
        gfx.draw_text("font_small", f"HAND: {gesture}", (2, g.HEIGHT - 8), colour="white")
        p.draw.circle(g.screen, g.convert_colour("lightblue"), (int(g.mx), int(g.my)), 2, 1)


def draw_webcam_panel():
    if g.input_mode != "gesture":
        return

    margin = 10
    camera_box = p.Rect(
        g.WINDOW_WIDTH - g.WEBCAM_OVERLAY_WIDTH - margin,
        margin,
        g.WEBCAM_OVERLAY_WIDTH,
        g.WEBCAM_OVERLAY_HEIGHT,
    )
    p.draw.rect(g.full_screen, (24, 24, 28), camera_box)
    p.draw.rect(g.full_screen, (233, 239, 236), camera_box, 2)

    camera_surf = gesture_input.get_camera_surface()
    if camera_surf:
        scaled = p.transform.scale(camera_surf, (camera_box.w, camera_box.h))
        g.full_screen.blit(scaled, camera_box)
    else:
        body_font = p.font.Font(os.path.join(g.FONTS_DIR, "Lo-Res 9 Narrow.ttf"), 18)
        message = gesture_input.get_status()
        surf = body_font.render(message, False, (233, 239, 236))
        g.full_screen.blit(surf, surf.get_rect(center=camera_box.center))

    small_font = p.font.Font(os.path.join(g.FONTS_DIR, "Lo-Res 9 Narrow.ttf"), 14)
    enabled = "ON" if gesture_input.is_enabled() else "OFF"
    left_gesture, right_gesture = gesture_input.get_hand_gestures()
    status_text = f"CAM {enabled}  L:{left_gesture}  R:{right_gesture}"
    status_surf = small_font.render(status_text, False, (233, 239, 236))
    bg_rect = status_surf.get_rect()
    bg_rect.topleft = (camera_box.left, camera_box.bottom + 4)
    bg_rect.inflate_ip(8, 6)
    p.draw.rect(g.full_screen, (24, 24, 28), bg_rect)
    g.full_screen.blit(status_surf, (bg_rect.left + 4, bg_rect.top + 3))




go_to_menu()
RUNNING = True
async def main():
    while RUNNING:
        g.screen.fill(g.convert_colour("black"))
        handle_input()
        update()
        draw()

        g.full_screen.fill((0, 0, 0))
        scaled_game = p.transform.scale(g.screen, (g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        g.full_screen.blit(scaled_game, (0, 0))
        draw_webcam_panel()

        p.display.flip()

        await asyncio.sleep(0)

        g.dt = g.game_clock.tick(g.FPS) / 1000
        g.dt = min(0.0333, g.dt)


    def quit_game():
        p.display.quit()
        import sys
        sys.exit()
    quit_game()


if __name__ == "__main__":
    asyncio.run(main())
