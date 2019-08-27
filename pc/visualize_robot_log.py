import pygame
import time
import os
import tarfile
import tkinter as tk
from tkinter import filedialog


sen_log_name = 'sensor.log'
deb_log_name = 'debug.log'
beh_log_name = 'behavior.log'
cam_log_name = 'camera.log'


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def drop_shadow_rect(screen, rect, offset, shadow_color, background_color):
    for i in range(1, offset):
        shadow_rect = (rect[0] + offset-i, rect[1] + offset-i, rect[2], rect[3])  # offset new rectangle x=-1, y=-1, starting with rectangle wich is furthest away, ending with nearest rectangle

        color = (int(background_color[0] + i/offset * (shadow_color[0] - background_color[0])), int(background_color[1] + i/offset * (shadow_color[1] - background_color[1])), int(background_color[2] + i/offset * (shadow_color[2] - background_color[2])))
        # change color linear from background_color to shadow_color by 1 step every loop

        pygame.draw.rect(screen, color, shadow_rect) # draw every shadow rect

def drop_shadow_hard_rect(screen, rect, offset, shadow_color):
    for i in range(1, offset):
        shadow_rect = (rect[0] + i, rect[1] + i, rect[2], rect[3])  # offset new rectangle x=+1, y=+1, starting with nearest rectangle
        pygame.draw.rect(screen, color, shadow_rect) # draw every shadow rect

def draw_text(text, screen, position = (0,0), size = 20, color = (0, 0, 0)):
    font = pygame.font.SysFont('opensans', size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)

def open_tar():
    tk_root = tk.Tk()
    tk_root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("Tar files", "*.tar.gz")])
    if file_path:
        return tarfile.open(file_path, encoding='utf-8'), file_path
    else:
        return None, None

def read_tar_logs(tar_file):
    sen_data = []
    beh_data = []
    deb_data = []
    cam_data = []

    for member in tar_file.getmembers():
        f = tar_file.extractfile(member)

        lines = [line.split() for line in f]

        print(lines)

        for line in lines:
            for byte_literal in line:
                byte_literal = byte_literal.decode("utf-8")

        print(lines)


        """if member.name == deb_log_name:
            deb_data = f.readlines()
        elif member.name == sen_log_name:
            sen_data = f.readlines()
        elif member.name == beh_log_name:
            beh_data = f.readlines()
        elif member.name == cam_log_name:
            cam_data = f.readlines()
"""
    tar_file.close()

    return beh_data, cam_data, deb_data, sen_data


def main():

    pygame.display.set_caption("Kamel log visualization")
    icon = pygame.image.load(os.getcwd() + "/kamel_log_visualizer_icon.png")
    pygame.display.set_icon(icon)


    (width, height) = (1280, 720)
    (robot_width, robot_height) = (360, 400)
    (robot_x, robot_y) = (100, (height-robot_height)/2)

    rect_log_button = pygame.Rect((width / 2 - 100, 20, 135, 20))

    screen = pygame.display.set_mode((width, height))

    light_gray = (220, 220, 220)
    dark_gray = (100, 100, 100)
    light_orange = (250, 141, 32)
    light_green = (130, 222, 64)
    background_color = light_gray


    platte_img = pygame.image.load(os.getcwd() + "/holzplatte.jpg")
    platte_image =  pygame.transform.scale(platte_img, (robot_width, robot_height))

    dig_sen_img = pygame.image.load(os.getcwd() + "/ir_digital_sharp.jpg")
    dig_sen_hor_l = pygame.transform.scale(dig_sen_img, (42,20))
    dig_sen_hor_r = pygame.transform.rotate(dig_sen_hor_l, 180)
    dig_sen_ver = pygame.transform.rotate(dig_sen_hor_l, -90)

    dig_sen_offset = 5

    ana_sen_img = pygame.image.load(os.getcwd() + "/ir_analog_sharp.jpg")
    ana_sen_img.set_colorkey((255,255,255))
    ana_sen_img = pygame.transform.scale(ana_sen_img, (74, 30))

    tou_sen_img = pygame.image.load(os.getcwd() + "/endschalter.jpg")
    tou_sen_img.set_colorkey((255,255,255))
    tou_sen_img = pygame.transform.scale(tou_sen_img, (60, 30))
    tou_sen_img_l = pygame.transform.rotate(tou_sen_img, 180)
    tou_sen_img_l = pygame.transform.flip(tou_sen_img_l, True, False)
    tou_sen_img_r = pygame.transform.rotate(tou_sen_img, 180)


    logs_archive = None
    logs_archive_path = ""
    logs_read = False


    m_time_start = time.time()

    running = True
    while running:
        m_time = time.time() - m_time_start

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_log_button.collidepoint(event.pos):
                    t_archive, t_archive_path = open_tar()
                    if t_archive != None and logs_archive == None and t_archive_path != logs_archive_path:
                        logs_archive = t_archive
                        logs_archive_path = t_archive_path
                        read_tar_logs(logs_archive)
                        print("New file selected: " + logs_archive_path)


        screen.fill(background_color)

        #pygame.draw.rect(screen, dark_gray,(robot_x + 10, robot_y + 10, robot_width, robot_height))
        drop_shadow_rect(screen, (robot_x, robot_y, robot_width, robot_height), 7, dark_gray, light_gray)
        screen.blit(platte_image, (robot_x, robot_y))

        screen.blit(dig_sen_hor_l, (robot_x + dig_sen_offset, robot_y + dig_sen_offset))
        screen.blit(dig_sen_ver, (robot_x + 50 + dig_sen_offset, robot_y + dig_sen_offset))
        screen.blit(dig_sen_ver, (robot_x + robot_width - 70 - dig_sen_offset, robot_y + dig_sen_offset))
        screen.blit(dig_sen_hor_r, (robot_x + robot_width - 42 - dig_sen_offset, robot_y + dig_sen_offset))

        screen.blit(dig_sen_hor_l, (robot_x + dig_sen_offset, robot_y + robot_height - 20 - dig_sen_offset))
        screen.blit(dig_sen_hor_r, (robot_x + robot_width - 42 - dig_sen_offset, robot_y + robot_height - 20 - dig_sen_offset))

        screen.blit(ana_sen_img, (robot_x + robot_width / 2 - 74/2, robot_y + 5))
        screen.blit(tou_sen_img_l, (robot_x + 45, robot_y + robot_height - 18))
        screen.blit(tou_sen_img_r, (robot_x + robot_width - 60 - 45, robot_y + robot_height - 18))

        drop_shadow_rect(screen, rect_log_button, 5, dark_gray, light_gray)
        if logs_archive == None:
            pygame.draw.rect(screen, light_orange, rect_log_button)
            draw_text("Select file", screen, position = (rect_log_button[0] + 15, rect_log_button[1]- 5))
        else:
            pygame.draw.rect(screen, light_green, rect_log_button)
            draw_text("File selected: " , screen, position = (rect_log_button[0] + 5, rect_log_button[1] - 5))
            draw_text(logs_archive_path, screen, size = 18, position = (rect_log_button[0] + rect_log_button[2] + 10, rect_log_button[1] - 3))


        pygame.display.update()
        #print(m_time)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
