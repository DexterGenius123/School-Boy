import os
import math
from PIL import Image, ImageDraw

FRAME_W = 56
FRAME_H = 64

# Authentic palette matching the uploaded character
SKIN = (222, 168, 138, 255)
SKIN_DARK = (175, 122, 96, 255)
SKIN_LIGHT = (242, 192, 165, 255)

HAIR = (96, 82, 52, 255)
HAIR_DARK = (62, 52, 34, 255)
HAIR_LIGHT = (138, 118, 76, 255)

BLAZER = (38, 44, 72, 255)
BLAZER_DARK = (24, 28, 48, 255)
BLAZER_LIGHT = (58, 68, 110, 255)

SHIRT = (220, 230, 245, 255)
TIE = (175, 25, 30, 255)
TIE_DARK = (115, 15, 20, 255)

PANTS = (100, 105, 110, 255)
PANTS_DARK = (65, 70, 75, 255)
PANTS_LIGHT = (130, 135, 140, 255)

SHOES = (28, 30, 36, 255)
SHOES_LIGHT = (55, 58, 68, 255)

BACKPACK = (125, 80, 40, 255)
BACKPACK_DARK = (85, 50, 25, 255)
BACKPACK_STRAP = (105, 65, 32, 255)

GLASSES_FRAME = (20, 20, 25, 255)
GLASSES_LENS = (235, 245, 255, 230)
OUTLINE = (20, 22, 28, 255)

def draw_student_frame(draw, fx, fy, pose_type, anim_step=0):
    ox = fx + FRAME_W // 2
    oy = fy + FRAME_H - 6  # Ground feet anchor
    
    bounce = 0
    if pose_type == "idle":
        bounce = 1 if (anim_step in [1, 2]) else 0
    elif pose_type == "walk":
        bounce = 2 if (anim_step in [1, 4]) else 0

    # Helper: draw head with hair, glasses, tie
    def draw_head(hx, hy, eye_state="normal"):
        # Neck
        draw.rectangle([hx - 2, hy + 4, hx + 2, hy + 8], fill=SKIN_DARK)
        # Head base
        draw.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=SKIN, outline=OUTLINE)
        # Hair base
        draw.ellipse([hx - 7, hy - 9, hx + 6, hy - 2], fill=HAIR)
        draw.rectangle([hx - 7, hy - 6, hx - 4, hy], fill=HAIR) # sideburn
        # Spiky hair strands
        draw.polygon([(hx - 6, hy - 7), (hx - 3, hy - 11), (hx, hy - 8)], fill=HAIR)
        draw.polygon([(hx - 1, hy - 8), (hx + 3, hy - 11), (hx + 6, hy - 6)], fill=HAIR_LIGHT)
        draw.polygon([(hx - 4, hy - 9), (hx - 1, hy - 12), (hx + 2, hy - 8)], fill=HAIR)
        
        # Glasses & Face
        if eye_state == "hurt":
            draw.line([hx + 1, hy - 1, hx + 5, hy + 3], fill=(210, 30, 30, 255), width=2)
            draw.line([hx + 1, hy + 3, hx + 5, hy - 1], fill=(210, 30, 30, 255), width=2)
            draw.rectangle([hx + 1, hy, hx + 6, hy + 3], outline=GLASSES_FRAME, width=1)
        else:
            # Round anime glasses
            draw.rectangle([hx + 1, hy - 2, hx + 5, hy + 2], outline=GLASSES_FRAME, width=1)
            draw.rectangle([hx + 2, hy - 1, hx + 4, hy + 1], fill=GLASSES_LENS)
            draw.point((hx + 3, hy), fill=(35, 35, 45, 255)) # Pupil
            draw.line([hx, hy - 1, hx + 1, hy - 1], fill=GLASSES_FRAME) # Bridge

    if pose_type in ["idle", "walk"]:
        if pose_type == "walk":
            cycle = anim_step % 6
            offsets = [(-4, 4), (-2, 2), (0, 0), (4, -4), (2, -2), (0, 0)]
            leg_front, leg_back = offsets[cycle]
        else:
            leg_front, leg_back = 2, -2

        # BACKPACK
        draw.rectangle([ox - 12, oy - 37 + bounce, ox - 6, oy - 22 + bounce], fill=BACKPACK, outline=OUTLINE)
        draw.rectangle([ox - 11, oy - 35 + bounce, ox - 7, oy - 24 + bounce], fill=BACKPACK_DARK)
        draw.line([ox - 12, oy - 28 + bounce, ox - 6, oy - 28 + bounce], fill=(160, 110, 60, 255), width=1)

        # LEGS (Grey trousers)
        draw.rectangle([ox - 5 + leg_back, oy - 22 + bounce, ox - 1 + leg_back, oy], fill=PANTS_DARK, outline=OUTLINE)
        draw.rectangle([ox - 6 + leg_back, oy - 5, ox + leg_back, oy], fill=SHOES, outline=OUTLINE)
        draw.rectangle([ox + 1 + leg_front, oy - 22 + bounce, ox + 5 + leg_front, oy], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox + leg_front, oy - 5, ox + 6 + leg_front, oy], fill=SHOES, outline=OUTLINE)

        # TORSO (Blazer, white shirt, red tie)
        draw.rectangle([ox - 6, oy - 38 + bounce, ox + 6, oy - 22 + bounce], fill=BLAZER, outline=OUTLINE)
        draw.line([ox - 6, oy - 38 + bounce, ox - 6, oy - 22 + bounce], fill=BLAZER_DARK)
        draw.polygon([(ox - 2, oy - 38 + bounce), (ox + 3, oy - 38 + bounce), (ox, oy - 30 + bounce)], fill=SHIRT)
        draw.line([ox, oy - 37 + bounce, ox, oy - 27 + bounce], fill=TIE, width=2)
        draw.point((ox + 2, oy - 26 + bounce), fill=(225, 195, 55, 255)) # Gold button

        # BACK ARM
        draw.rectangle([ox - 8, oy - 35 + bounce, ox - 5, oy - 26 + bounce], fill=BLAZER_DARK)
        draw.rectangle([ox - 8, oy - 26 + bounce, ox - 5, oy - 22 + bounce], fill=SKIN_DARK)

        # FRONT ARM (ready combat guard pose)
        draw.rectangle([ox + 4, oy - 35 + bounce, ox + 8, oy - 27 + bounce], fill=BLAZER)
        draw.rectangle([ox + 6, oy - 31 + bounce, ox + 11, oy - 26 + bounce], fill=SKIN, outline=OUTLINE)

        # HEAD
        draw_head(ox, oy - 45 + bounce)

    elif pose_type == "punch1":
        # Straight schoolboy jab
        draw.rectangle([ox - 11, oy - 36, ox - 5, oy - 22], fill=BACKPACK, outline=OUTLINE)
        draw.rectangle([ox - 4, oy - 22, ox, oy], fill=PANTS_DARK, outline=OUTLINE)
        draw.rectangle([ox + 2, oy - 22, ox + 7, oy], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox - 5, oy - 5, ox + 1, oy], fill=SHOES, outline=OUTLINE)
        draw.rectangle([ox + 2, oy - 5, ox + 8, oy], fill=SHOES, outline=OUTLINE)

        # Torso
        draw.rectangle([ox - 5, oy - 38, ox + 6, oy - 22], fill=BLAZER, outline=OUTLINE)
        draw.polygon([(ox - 2, oy - 38), (ox + 3, oy - 38), (ox, oy - 30)], fill=SHIRT)
        draw.line([ox, oy - 37, ox, oy - 27], fill=TIE, width=2)

        # Extended punch arm
        reach = 14 if anim_step == 1 else 8
        draw.rectangle([ox + 4, oy - 36, ox + 8 + reach, oy - 30], fill=BLAZER, outline=OUTLINE)
        draw.rectangle([ox + 8 + reach, oy - 36, ox + 14 + reach, oy - 30], fill=SKIN, outline=OUTLINE)

        draw_head(ox + 1, oy - 45)

    elif pose_type == "punch2":
        # Backpack / heavy hook strike
        draw.rectangle([ox - 6, oy - 22, ox - 1, oy], fill=PANTS_DARK, outline=OUTLINE)
        draw.rectangle([ox + 1, oy - 22, ox + 6, oy], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox - 7, oy - 5, ox, oy], fill=SHOES, outline=OUTLINE)
        draw.rectangle([ox + 1, oy - 5, ox + 7, oy], fill=SHOES, outline=OUTLINE)

        draw.rectangle([ox - 5, oy - 37, ox + 7, oy - 22], fill=BLAZER, outline=OUTLINE)
        draw.polygon([(ox - 2, oy - 37), (ox + 3, oy - 37), (ox, oy - 30)], fill=SHIRT)
        draw.line([ox, oy - 36, ox, oy - 27], fill=TIE, width=2)

        # Swung backpack forward
        px = ox + 14 if anim_step == 1 else ox + 8
        py = oy - 36 if anim_step == 1 else oy - 31
        draw.line([ox + 4, oy - 32, px, py], fill=BLAZER, width=4)
        draw.rectangle([px - 2, py - 6, px + 10, py + 6], fill=BACKPACK, outline=OUTLINE)
        draw.line([px - 2, py, px + 10, py], fill=(160, 110, 60, 255), width=1)

        draw_head(ox + 2, oy - 45)

    elif pose_type == "finisher":
        # Full high roundhouse kick
        draw.rectangle([ox - 4, oy - 22, ox + 1, oy], fill=PANTS_DARK, outline=OUTLINE)
        draw.rectangle([ox - 5, oy - 5, ox + 1, oy], fill=SHOES, outline=OUTLINE)

        draw.rectangle([ox - 6, oy - 37, ox + 5, oy - 22], fill=BLAZER, outline=OUTLINE)
        draw.line([ox - 1, oy - 36, ox - 1, oy - 27], fill=TIE, width=2)

        # Extended kicking leg horizontally
        kick_reach = 18 if anim_step >= 1 else 10
        draw.rectangle([ox + 2, oy - 33, ox + 2 + kick_reach, oy - 26], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox + kick_reach, oy - 34, ox + 6 + kick_reach, oy - 25], fill=SHOES, outline=OUTLINE)

        # Flying tie effect
        draw.line([ox + 3, oy - 32, ox + 8, oy - 34], fill=TIE, width=2)

        draw_head(ox - 2, oy - 44)

    elif pose_type == "jump":
        # Tucked in air
        draw.rectangle([ox - 10, oy - 38, ox - 5, oy - 26], fill=BACKPACK, outline=OUTLINE)
        draw.rectangle([ox - 5, oy - 30, ox + 3, oy - 16], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox - 4, oy - 17, ox + 4, oy - 12], fill=SHOES, outline=OUTLINE)
        draw.rectangle([ox - 6, oy - 44, ox + 5, oy - 30], fill=BLAZER, outline=OUTLINE)
        draw.line([ox, oy - 42, ox, oy - 34], fill=TIE, width=2)
        # Arms raised
        draw.line([ox - 5, oy - 42, ox - 9, oy - 48], fill=BLAZER, width=3)
        draw.line([ox + 5, oy - 42, ox + 9, oy - 48], fill=BLAZER, width=3)

        draw_head(ox, oy - 50)

    elif pose_type == "jump_kick":
        # Flying dropkick
        draw.rectangle([ox - 10, oy - 36, ox - 4, oy - 24], fill=BACKPACK, outline=OUTLINE)
        draw.rectangle([ox - 8, oy - 34, ox + 2, oy - 22], fill=BLAZER, outline=OUTLINE)
        draw.line([ox, oy - 24, ox + 18, oy - 14], fill=PANTS, width=6)
        draw.rectangle([ox + 16, oy - 16, ox + 22, oy - 10], fill=SHOES, outline=OUTLINE)
        draw.line([ox - 4, oy - 24, ox - 10, oy - 20], fill=PANTS_DARK, width=5)

        draw_head(ox - 6, oy - 40)

    elif pose_type == "special":
        # 360 Spin attack (Spinning backpack whirlwind)
        rot = anim_step * 90
        rad = math.radians(rot)
        dx = int(math.cos(rad) * 18)
        dy = int(math.sin(rad) * 8)
        # Cyan energy swirl
        draw.ellipse([ox - 22, oy - 38, ox + 22, oy - 10], outline=(100, 190, 255, 230), width=2)
        draw.rectangle([ox - 6, oy - 40, ox + 6, oy - 18], fill=BLAZER, outline=OUTLINE)
        # Spinning backpack
        draw.rectangle([ox + dx - 4, oy - 30 + dy - 4, ox + dx + 4, oy - 30 + dy + 4], fill=BACKPACK, outline=OUTLINE)
        draw.line([ox, oy - 30, ox + dx, oy - 30 + dy], fill=BACKPACK_STRAP, width=2)

        draw.rectangle([ox - 4, oy - 18, ox + 4, oy], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox - 5, oy - 5, ox + 5, oy], fill=SHOES, outline=OUTLINE)

        draw_head(ox, oy - 46)

    elif pose_type == "hurt":
        # Reeled back, glasses askew
        draw.rectangle([ox - 11, oy - 34, ox - 5, oy - 22], fill=BACKPACK, outline=OUTLINE)
        draw.rectangle([ox - 7, oy - 22, ox - 2, oy], fill=PANTS_DARK, outline=OUTLINE)
        draw.rectangle([ox - 1, oy - 22, ox + 4, oy], fill=PANTS, outline=OUTLINE)
        draw.rectangle([ox - 8, oy - 5, ox - 1, oy], fill=SHOES, outline=OUTLINE)
        draw.rectangle([ox - 1, oy - 5, ox + 5, oy], fill=SHOES, outline=OUTLINE)

        draw.polygon([(ox - 10, oy - 36), (ox + 1, oy - 36), (ox + 4, oy - 22), (ox - 6, oy - 22)], fill=BLAZER, outline=OUTLINE)
        draw.line([ox - 4, oy - 35, ox - 1, oy - 26], fill=TIE, width=2)

        draw_head(ox - 6, oy - 44, eye_state="hurt")

    elif pose_type == "knockdown":
        if anim_step == 0:
            draw.polygon([(ox - 18, oy - 22), (ox + 8, oy - 26), (ox + 6, oy - 16), (ox - 16, oy - 12)], fill=BLAZER, outline=OUTLINE)
            draw.line([ox + 8, oy - 25, ox + 22, oy - 22], fill=PANTS, width=6)
            draw.rectangle([ox + 20, oy - 24, ox + 26, oy - 18], fill=SHOES, outline=OUTLINE)
            draw.rectangle([ox - 22, oy - 22, ox - 16, oy - 14], fill=BACKPACK, outline=OUTLINE)
            hx, hy = ox - 23, oy - 20
            draw_head(hx, hy, eye_state="hurt")
        elif anim_step == 1:
            draw.polygon([(ox - 16, oy - 14), (ox + 6, oy - 18), (ox + 4, oy - 8), (ox - 14, oy - 4)], fill=BLAZER, outline=OUTLINE)
            draw.line([ox + 6, oy - 16, ox + 18, oy - 12], fill=PANTS, width=5)
            draw.rectangle([ox + 16, oy - 14, ox + 21, oy - 9], fill=SHOES, outline=OUTLINE)
            draw.rectangle([ox - 20, oy - 14, ox - 14, oy - 8], fill=BACKPACK, outline=OUTLINE)
            hx, hy = ox - 20, oy - 12
            draw_head(hx, hy, eye_state="hurt")
        else:
            draw.rectangle([ox - 14, oy - 8, ox + 6, oy - 2], fill=BLAZER, outline=OUTLINE)
            draw.rectangle([ox + 6, oy - 8, ox + 18, oy - 2], fill=PANTS, outline=OUTLINE)
            draw.rectangle([ox + 18, oy - 9, ox + 23, oy - 2], fill=SHOES, outline=OUTLINE)
            draw.rectangle([ox - 16, oy - 10, ox - 10, oy - 4], fill=BACKPACK, outline=OUTLINE)
            hx, hy = ox - 20, oy - 5
            draw_head(hx, hy, eye_state="hurt")

def generate_student_sheet(filename):
    cols, rows = 8, 4
    sheet = Image.new("RGBA", (cols * FRAME_W, rows * FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    
    frames = [
        # Row 0: Idle (4), Walk (4)
        (0, 0, "idle", 0), (1, 0, "idle", 1), (2, 0, "idle", 2), (3, 0, "idle", 3),
        (4, 0, "walk", 0), (5, 0, "walk", 1), (6, 0, "walk", 2), (7, 0, "walk", 3),
        
        # Row 1: Walk (2), Punch1 (2), Punch2 (2), Finisher (2)
        (0, 1, "walk", 4), (1, 1, "walk", 5),
        (2, 1, "punch1", 0), (3, 1, "punch1", 1),
        (4, 1, "punch2", 0), (5, 1, "punch2", 1),
        (6, 1, "finisher", 0), (7, 1, "finisher", 1),
        
        # Row 2: Finisher (1), Jump (1), JumpKick (2), Special (4)
        (0, 2, "finisher", 2),
        (1, 2, "jump", 0),
        (2, 2, "jump_kick", 0), (3, 2, "jump_kick", 1),
        (4, 2, "special", 0), (5, 2, "special", 1), (6, 2, "special", 2), (7, 2, "special", 3),
        
        # Row 3: Hurt (2), Knockdown (3), Dead (1), Idle (2)
        (0, 3, "hurt", 0), (1, 3, "hurt", 1),
        (2, 3, "knockdown", 0), (3, 3, "knockdown", 1), (4, 3, "knockdown", 2),
        (5, 3, "knockdown", 2),
        (6, 3, "idle", 0), (7, 3, "idle", 0)
    ]
    
    for c, r, pose, step in frames:
        draw_student_frame(draw, c * FRAME_W, r * FRAME_H, pose, step)
        
    sheet.save(filename)
    print(f"Saved student hero sprite sheet to {filename}")

if __name__ == "__main__":
    generate_student_sheet("assets/sprites/player.png")
