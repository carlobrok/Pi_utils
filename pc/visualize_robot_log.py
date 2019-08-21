import pygame
import time


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




pygame.init()

pygame.display.set_caption("Kamel log visualization")
icon = pygame.image.load("/home/carlo/git/Pi_utils/pc/kamel_log_visualizer_icon.png")
pygame.display.set_icon(icon)


(width, height) = (1280, 720)
(robot_width, robot_height) = (360, 400)
(robot_x, robot_y) = (100, (height-robot_height)/2)

screen = pygame.display.set_mode((width, height))

light_gray = (220, 220, 220)
dark_gray = (100,100,100)
background_color = light_gray


platte_img = pygame.image.load("/home/carlo/git/Pi_utils/pc/holzplatte.jpg")
platte_image =  pygame.transform.scale(platte_img, (robot_width, robot_height))

dig_sen_img = pygame.image.load("/home/carlo/git/Pi_utils/pc/ir_digital_sharp.jpg")
dig_sen_hor_l = pygame.transform.scale(dig_sen_img, (42,20))
dig_sen_hor_r = pygame.transform.rotate(dig_sen_hor_l, 180)
dig_sen_ver = pygame.transform.rotate(dig_sen_hor_l, -90)

dig_sen_offset = 5

#dig_sen_image = pygame.image.load("myimage.bmp")
#dig_sen_rect = dig_sen_image.get_rect()





m_time_start = time.time()

running = True
while running:
    m_time = time.time() - m_time_start

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()

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

    pygame.display.update()
    #print(m_time)
