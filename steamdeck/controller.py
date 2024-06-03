import pygame
import sys
import serial

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 800
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 36

BUTTON_INDICATOR_WIDTH = 30 
BUTTON_INDICATOR_HEIGHT = 30 
BUTTON_INDICATOR_COLOR = (0, 255, 0)

JOYSTICK_RADIUS = 50 
INDICATOR_RADIUS = 10
BAR_WIDTH = 20
BAR_HEIGHT = 100

# A
BUTTON_0_POS = pygame.Rect(1136 - BUTTON_INDICATOR_WIDTH/2, 281 - BUTTON_INDICATOR_HEIGHT/2, BUTTON_INDICATOR_WIDTH, BUTTON_INDICATOR_HEIGHT)

# B
BUTTON_1_POS = pygame.Rect(1168 - BUTTON_INDICATOR_WIDTH/2, 247 - BUTTON_INDICATOR_HEIGHT/2, BUTTON_INDICATOR_WIDTH, BUTTON_INDICATOR_HEIGHT)

# X
BUTTON_2_POS = pygame.Rect(1101 - BUTTON_INDICATOR_WIDTH/2, 248 - BUTTON_INDICATOR_HEIGHT/2, BUTTON_INDICATOR_WIDTH, BUTTON_INDICATOR_HEIGHT)

# Y
BUTTON_3_POS = pygame.Rect(1136 - BUTTON_INDICATOR_WIDTH/2, 212 - BUTTON_INDICATOR_HEIGHT/2, BUTTON_INDICATOR_WIDTH, BUTTON_INDICATOR_HEIGHT)

# LB
BUTTON_4_POS = pygame.Rect(187 - 125/2, 170 - 20/2, 125, 20)

# RB
BUTTON_5_POS = pygame.Rect(1092 - 125/2, 170 - 20/2, 125, 20)

# Select
BUTTON_6_POS = pygame.Rect(206 - BUTTON_INDICATOR_WIDTH/2, 202 - BUTTON_INDICATOR_HEIGHT/2, BUTTON_INDICATOR_WIDTH, BUTTON_INDICATOR_HEIGHT)

# Start
BUTTON_7_POS = pygame.Rect(1073 - BUTTON_INDICATOR_WIDTH/2, 202 - BUTTON_INDICATOR_HEIGHT/2, BUTTON_INDICATOR_WIDTH, BUTTON_INDICATOR_HEIGHT)

# BUTTON 8 (center)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Joystick Input Display')

controller_img = pygame.image.load('./steamdeck/controller.png')
controller_img = pygame.transform.scale(controller_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
controller_rect = controller_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


font = pygame.font.Font(None, FONT_SIZE)

pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("No joysticks found")
    pygame.quit()
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Function to display text
def display_text(text, position):
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, position)

# Function to highlight controller areas
def highlight_area(rect, color):
    highlight_surface = pygame.Surface(rect.size)
    highlight_surface.fill(color)
    highlight_surface.set_alpha(128)  # Transparency
    screen.blit(highlight_surface, rect.topleft)

# Function to draw joystick position
def draw_joystick_position(x, y, base_x, base_y):
    # Draw the fixed circle
    pygame.draw.circle(screen, (160, 160, 160), (base_x, base_y), JOYSTICK_RADIUS)

    # Calculate the position of the small indicator circle
    indicator_x = base_x + int(x * JOYSTICK_RADIUS)
    indicator_y = base_y + int(y * JOYSTICK_RADIUS)

    # Draw the small indicator circle
    pygame.draw.circle(screen, (0, 255, 0), (indicator_x, indicator_y), INDICATOR_RADIUS)

# Function to draw vertical bar
def draw_vertical_bar(value, base_x, base_y):
    # Calculate the height of the bar
    bar_height = (value + 1) / 2 * BAR_HEIGHT
    bar_rect = pygame.Rect(base_x, base_y - bar_height, BAR_WIDTH, bar_height)
    pygame.draw.rect(screen, (0, 255, 0), bar_rect)

# Initialize Serial connection
try:
    ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
except serial.SerialException as e:
    print(f"Serial error: {e}")
    sys.exit(1)

# Main loop
def main():
    clock = pygame.time.Clock()

    left_axis_x_old = 0    
    left_axis_y_old = 0
    left_trigger_axis_old = 0
    
    right_axis_x_old = 0    
    right_axis_y_old = 0
    right_trigger_axis_old = 0

    button0_on = False
    button1_on = False
    button2_on = False
    button3_on = False
    button4_on = False
    button5_on = False
    button6_on = False
    button7_on = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BG_COLOR)

        # Draw the controller image
        screen.blit(controller_img, controller_rect)

        # Example areas to highlight based on joystick input
        if joystick.get_button(0) and not button0_on:
            highlight_area(BUTTON_0_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B0ON\n')
            button0_on = True

        if not joystick.get_button(0) and button0_on:
            ser.write(b'B0OFF\n')
            button0_on = False
            
        if joystick.get_button(1) and not button1_on:
            highlight_area(BUTTON_1_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B1ON\n')
            button1_on = True

        if not joystick.get_button(1) and button1_on:
            ser.write(b'B1OFF\n')
            button1_on = False

        if joystick.get_button(2) and not button2_on:
            highlight_area(BUTTON_2_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B2ON\n')
            button2_on = True

        if not joystick.get_button(2) and button2_on:
            ser.write(b'B2OFF\n')
            button2_on = False

        if joystick.get_button(3) and not button3_on:
            highlight_area(BUTTON_3_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B3ON\n')
            button3_on = True

        if not joystick.get_button(3) and button3_on:
            ser.write(b'B3OFF\n')
            button3_on = False
            
        if joystick.get_button(4) and not button4_on:
            highlight_area(BUTTON_4_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B4ON\n')
            button4_on = True

        if not joystick.get_button(4) and button4_on:
            ser.write(b'B4OFF\n')
            button4_on = False
            
        if joystick.get_button(5) and not button5_on:
            highlight_area(BUTTON_5_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B5ON\n')
            button5_on = True
            
        if not joystick.get_button(5) and button5_on:
            ser.write(b'B5OFF\n')
            button5_on = False
            
        if joystick.get_button(6) and not button6_on:
            highlight_area(BUTTON_6_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B6ON\n')
            button6_on = True

        if not joystick.get_button(6) and button6_on:
            ser.write(b'B6OFF\n')
            button6_on = False
            
        if joystick.get_button(7) and not button7_on:
            highlight_area(BUTTON_7_POS, BUTTON_INDICATOR_COLOR)  
            ser.write(b'B7ON\n')
            button7_on = True

        if not joystick.get_button(7) and button7_on:
            ser.write(b'B7OFF\n')
            button7_on = False
            
        # Add more button/axis mappings here...

        left_axis_x = round(joystick.get_axis(0), 2)
        if left_axis_x != left_axis_x_old and abs(left_axis_x - left_axis_x_old) > 0.05:
            ser.write(f"LX{left_axis_x}\n".encode())
            left_axis_x_old = left_axis_x

        left_axis_y = round(joystick.get_axis(1), 2)
        if left_axis_y != left_axis_y_old and abs(left_axis_y - left_axis_y_old) > 0.05:
            ser.write(f"LY{left_axis_y}\n".encode())
            left_axis_y_old = left_axis_y

        left_trigger_axis = round(joystick.get_axis(2), 2)
        if left_trigger_axis != left_trigger_axis_old and abs(left_trigger_axis - left_trigger_axis_old) > 0.05:
            ser.write(f"LT{left_trigger_axis}\n".encode())
            left_trigger_axis_old = left_trigger_axis

        right_axis_x = round(joystick.get_axis(3), 2)
        if right_axis_x != right_axis_x_old and abs(right_axis_x - right_axis_x_old) > 0.05:
            ser.write(f"RX{right_axis_x}\n".encode())
            right_axis_x_old = right_axis_x

        right_axis_y = round(joystick.get_axis(4), 2)
        if right_axis_y != right_axis_y_old and abs(right_axis_y - right_axis_y_old) > 0.05:
            ser.write(f"RY{right_axis_y}\n".encode())
            right_axis_y_old = right_axis_y

        right_trigger_axis = round(joystick.get_axis(5), 2)
        if right_trigger_axis != right_trigger_axis_old and abs(right_trigger_axis - right_trigger_axis_old) > 0.05:
            ser.write(f"RT{right_trigger_axis}\n".encode())
            right_trigger_axis_old = right_trigger_axis

        draw_joystick_position(left_axis_x, left_axis_y, 254, 266)
        draw_vertical_bar(left_trigger_axis, 20, 376)

        draw_joystick_position(right_axis_x, right_axis_y, 1025, 267)
        draw_vertical_bar(right_trigger_axis, 1238, 376)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

if __name__ == '__main__':
    main()
