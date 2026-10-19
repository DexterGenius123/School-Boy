import os
import math
from PIL import Image, ImageDraw

os.makedirs("assets/sprites", exist_ok=True)
os.makedirs("assets/backgrounds", exist_ok=True)

# 1. SHADOW
def create_shadow():
    w, h = 32, 14
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i in range(h // 2):
        alpha = int(140 * (1.0 - (i / (h / 2.0)) * 0.4))
        draw.ellipse([i * 2, i, w - 1 - i * 2, h - 1 - i], fill=(0, 0, 0, alpha))
    img.save("assets/sprites/shadow.png")

# 2. HIT EFFECT (Starburst retro sparks)
def create_hit_effects():
    w, h = 32, 32
    sheet = Image.new("RGBA", (w * 4, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    
    # Frame 0: Small initial bright flash
    cx, cy = 16, 16
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(255, 255, 255, 255))
    draw.line([cx-8, cy, cx+8, cy], fill=(255, 255, 100, 255), width=2)
    draw.line([cx, cy-8, cx, cy+8], fill=(255, 255, 100, 255), width=2)
    
    # Frame 1: Big starburst with yellow/red jagged spikes
    f1_x = 32 + 16
    draw.ellipse([f1_x-8, cy-8, f1_x+8, cy+8], fill=(255, 255, 0, 255))
    draw.ellipse([f1_x-4, cy-4, f1_x+4, cy+4], fill=(255, 255, 255, 255))
    spikes = [(0, 14), (14, 0), (0, -14), (-14, 0), (10, 10), (-10, 10), (10, -10), (-10, -10)]
    for dx, dy in spikes:
        draw.line([f1_x, cy, f1_x + dx, cy + dy], fill=(255, 120, 0, 255), width=2)
        draw.line([f1_x, cy, f1_x + int(dx*0.7), cy + int(dy*0.7)], fill=(255, 255, 200, 255), width=1)
        
    # Frame 2: Expanding fading ring and sparks
    f2_x = 64 + 16
    draw.ellipse([f2_x-11, cy-11, f2_x+11, cy+11], outline=(255, 200, 50, 200), width=2)
    draw.ellipse([f2_x-5, cy-5, f2_x+5, cy+5], outline=(255, 100, 0, 160), width=1)
    sparks = [(8, 12), (-11, 8), (12, -7), (-9, -11), (13, 2), (-12, -2)]
    for sx, sy in sparks:
        draw.rectangle([f2_x + sx, cy + sy, f2_x + sx + 1, cy + sy + 1], fill=(255, 255, 220, 220))
        
    # Frame 3: Dispersing dust particles
    f3_x = 96 + 16
    p_pts = [(10, 14), (-12, 11), (14, -8), (-13, -10), (0, 15), (0, -15)]
    for px, py in p_pts:
        draw.rectangle([f3_x + px, cy + py, f3_x + px + 1, cy + py + 1], fill=(255, 150, 50, 140))
        
    sheet.save("assets/sprites/hit_effect.png")

# 3. PICKUPS: Roast Chicken, Red Apple, Gold Bar
def create_pickups():
    # Chicken
    w, h = 24, 20
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 12, 21, 18], fill=(160, 170, 180, 255))
    draw.ellipse([4, 13, 19, 17], fill=(210, 220, 230, 255))
    draw.ellipse([5, 5, 18, 14], fill=(180, 80, 20, 255))
    draw.ellipse([7, 7, 16, 12], fill=(225, 120, 30, 255))
    draw.line([17, 7, 21, 5], fill=(240, 230, 210, 255), width=2)
    draw.point((22, 4), fill=(255, 255, 255, 255))
    draw.point((22, 6), fill=(255, 255, 255, 255))
    img.save("assets/sprites/pickup_chicken.png")
    
    # Apple
    img_apple = Image.new("RGBA", (18, 18), (0, 0, 0, 0))
    d = ImageDraw.Draw(img_apple)
    d.ellipse([3, 4, 14, 16], fill=(220, 20, 20, 255))
    d.ellipse([5, 6, 8, 10], fill=(255, 100, 100, 255))
    d.line([8, 1, 9, 4], fill=(100, 60, 20, 255), width=1)
    d.line([9, 2, 12, 1], fill=(50, 180, 40, 255), width=1)
    img_apple.save("assets/sprites/pickup_apple.png")
    
    # Gold Bar
    img_gold = Image.new("RGBA", (22, 16), (0, 0, 0, 0))
    dg = ImageDraw.Draw(img_gold)
    dg.polygon([(4, 4), (17, 4), (20, 12), (1, 12)], fill=(255, 210, 30, 255))
    dg.polygon([(4, 4), (17, 4), (15, 6), (6, 6)], fill=(255, 255, 150, 255))
    dg.line([(1, 12), (20, 12)], fill=(180, 130, 10, 255), width=1)
    img_gold.save("assets/sprites/pickup_gold.png")

# 4. BREAKABLE BARREL
def create_barrel():
    sheet = Image.new("RGBA", (64, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    
    # Intact wooden barrel
    draw.rectangle([5, 4, 26, 36], fill=(130, 75, 30, 255))
    draw.ellipse([4, 2, 27, 8], fill=(160, 95, 40, 255))
    draw.ellipse([5, 33, 26, 38], fill=(100, 55, 20, 255))
    for y_hoop in [8, 18, 28]:
        draw.line([4, y_hoop, 27, y_hoop], fill=(90, 95, 105, 255), width=2)
        draw.line([4, y_hoop-1, 27, y_hoop-1], fill=(140, 145, 160, 255), width=1)
    for x_p in [10, 16, 21]:
        draw.line([x_p, 4, x_p, 36], fill=(90, 50, 20, 255), width=1)
        
    # Broken barrel frame
    b_x = 32
    draw.polygon([(b_x+4, 15), (b_x+9, 36), (b_x+5, 36)], fill=(130, 75, 30, 255))
    draw.polygon([(b_x+10, 22), (b_x+17, 36), (b_x+12, 36)], fill=(110, 60, 25, 255))
    draw.polygon([(b_x+22, 18), (b_x+27, 36), (b_x+24, 36)], fill=(140, 80, 35, 255))
    draw.line([b_x+6, 30, b_x+26, 34], fill=(90, 95, 105, 255), width=2)
    draw.rectangle([b_x+7, 6, b_x+12, 10], fill=(160, 95, 40, 255))
    draw.rectangle([b_x+20, 4, b_x+25, 9], fill=(140, 80, 35, 255))
    
    sheet.save("assets/sprites/barrel.png")

# 5. GO! ARROW (Arcade blinking sign)
def create_go_sign():
    w, h = 60, 26
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w-1, h-1], outline=(0, 255, 120, 255), width=2)
    draw.rectangle([2, 2, w-3, h-3], fill=(0, 40, 20, 200))
    # G
    draw.rectangle([6, 5, 8, 20], fill=(0, 255, 120, 255))
    draw.rectangle([6, 5, 18, 7], fill=(0, 255, 120, 255))
    draw.rectangle([6, 18, 18, 20], fill=(0, 255, 120, 255))
    draw.rectangle([16, 12, 18, 20], fill=(0, 255, 120, 255))
    draw.rectangle([12, 12, 18, 14], fill=(0, 255, 120, 255))
    # O
    draw.rectangle([22, 5, 24, 20], fill=(0, 255, 120, 255))
    draw.rectangle([32, 5, 34, 20], fill=(0, 255, 120, 255))
    draw.rectangle([22, 5, 34, 7], fill=(0, 255, 120, 255))
    draw.rectangle([22, 18, 34, 20], fill=(0, 255, 120, 255))
    # ARROW
    draw.rectangle([40, 11, 48, 14], fill=(255, 220, 0, 255))
    draw.polygon([(48, 7), (55, 12), (48, 18)], fill=(255, 220, 0, 255))
    img.save("assets/sprites/go_arrow.png")

# 6. AXEL PORTRAIT (HUD)
def create_axel_portrait():
    w, h = 32, 32
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w-1, h-1], outline=(220, 180, 50, 255), width=1)
    draw.rectangle([1, 1, w-2, h-2], fill=(20, 20, 40, 255))
    draw.ellipse([8, 3, 23, 14], fill=(235, 190, 45, 255))
    draw.rectangle([7, 10, 24, 12], fill=(220, 30, 30, 255))
    draw.rectangle([9, 13, 22, 23], fill=(240, 180, 140, 255))
    draw.line([10, 14, 14, 14], fill=(80, 40, 20, 255))
    draw.line([17, 14, 21, 14], fill=(80, 40, 20, 255))
    draw.point((12, 16), fill=(40, 40, 100, 255))
    draw.point((19, 16), fill=(40, 40, 100, 255))
    draw.point((15, 18), fill=(200, 140, 100, 255))
    draw.line([13, 21, 18, 21], fill=(180, 90, 80, 255))
    draw.polygon([(6, 26), (25, 26), (28, 31), (3, 31)], fill=(30, 90, 200, 255))
    draw.polygon([(11, 26), (20, 26), (16, 31)], fill=(240, 180, 140, 255))
    img.save("assets/sprites/portrait_axel.png")

FRAME_W = 56
FRAME_H = 64

def draw_character_frame(draw, fx, fy, char_type, pose_type, anim_step=0):
    ox = fx + FRAME_W // 2
    oy = fy + FRAME_H - 6
    
    if char_type == "axel":
        skin = (245, 185, 145, 255)
        skin_dark = (200, 140, 100, 255)
        hair = (240, 195, 45, 255)
        headband = (220, 35, 35, 255)
        shirt = (35, 100, 215, 255)
        shirt_dark = (20, 60, 150, 255)
        pants = (60, 110, 180, 255)
        pants_dark = (35, 75, 135, 255)
        shoes = (230, 50, 50, 255)
        gloves = (40, 40, 50, 255)
    elif char_type == "brawler":
        skin = (225, 175, 135, 255)
        skin_dark = (180, 130, 90, 255)
        hair = (220, 40, 40, 255)
        headband = None
        shirt = (240, 240, 240, 255)
        shirt_dark = (170, 170, 175, 255)
        pants = (45, 140, 55, 255)
        pants_dark = (25, 90, 35, 255)
        shoes = (35, 35, 40, 255)
        gloves = (160, 40, 40, 255)
    elif char_type == "speedy":
        skin = (235, 190, 150, 255)
        skin_dark = (190, 145, 105, 255)
        hair = (255, 140, 20, 255)
        headband = (240, 220, 30, 255)
        shirt = (235, 210, 25, 255)
        shirt_dark = (180, 150, 10, 255)
        pants = (200, 40, 30, 255)
        pants_dark = (140, 20, 15, 255)
        shoes = (240, 240, 240, 255)
        gloves = (30, 30, 35, 255)

    bounce = 0
    if pose_type == "idle":
        bounce = 1 if (anim_step % 4 in [1, 2]) else 0
    elif pose_type == "walk":
        bounce = 2 if (anim_step in [1, 4]) else 0

    if pose_type in ["idle", "walk"]:
        if pose_type == "walk":
            cycle = anim_step % 6
            offsets = [(-4, 4), (-2, 2), (0, 0), (4, -4), (2, -2), (0, 0)]
            leg_offset, leg_back = offsets[cycle]
        else:
            leg_offset, leg_back = 2, -2

        draw.rectangle([ox - 5 + leg_back, oy - 22 + bounce, ox - 1 + leg_back, oy], fill=pants_dark)
        draw.rectangle([ox - 6 + leg_back, oy - 4, ox + leg_back, oy], fill=shoes)
        draw.rectangle([ox + 1 + leg_offset, oy - 22 + bounce, ox + 5 + leg_offset, oy], fill=pants)
        draw.rectangle([ox + leg_offset, oy - 4, ox + 6 + leg_offset, oy], fill=shoes)

        draw.rectangle([ox - 6, oy - 38 + bounce, ox + 6, oy - 22 + bounce], fill=shirt)
        draw.line([ox - 6, oy - 38 + bounce, ox - 6, oy - 22 + bounce], fill=shirt_dark)
        draw.line([ox, oy - 30 + bounce, ox + 2, oy - 24 + bounce], fill=shirt_dark)

        draw.rectangle([ox - 9, oy - 36 + bounce, ox - 6, oy - 26 + bounce], fill=skin_dark)
        draw.rectangle([ox - 10, oy - 26 + bounce, ox - 6, oy - 21 + bounce], fill=gloves)

        draw.rectangle([ox + 4, oy - 36 + bounce, ox + 8, oy - 28 + bounce], fill=skin)
        draw.rectangle([ox + 6, oy - 32 + bounce, ox + 11, oy - 26 + bounce], fill=gloves)

        hx, hy = ox, oy - 45 + bounce
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband:
            draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler":
            draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else:
            draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)
        draw.point((hx + 3, hy), fill=(30, 20, 20, 255))
        draw.point((hx + 4, hy + 2), fill=skin_dark)

    elif pose_type == "punch1":
        draw.rectangle([ox - 4, oy - 22, ox, oy], fill=pants_dark)
        draw.rectangle([ox + 2, oy - 22, ox + 7, oy], fill=pants)
        draw.rectangle([ox - 5, oy - 4, ox + 1, oy], fill=shoes)
        draw.rectangle([ox + 2, oy - 4, ox + 8, oy], fill=shoes)

        draw.rectangle([ox - 5, oy - 38, ox + 6, oy - 22], fill=shirt)
        reach = 14 if anim_step == 1 else 8
        draw.rectangle([ox + 4, oy - 36, ox + 8 + reach, oy - 31], fill=skin)
        draw.rectangle([ox + 7 + reach, oy - 37, ox + 13 + reach, oy - 30], fill=gloves)

        hx, hy = ox + 1, oy - 45
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)
        draw.point((hx + 3, hy), fill=(30, 20, 20, 255))

    elif pose_type == "punch2":
        draw.rectangle([ox - 6, oy - 22, ox - 1, oy], fill=pants_dark)
        draw.rectangle([ox + 1, oy - 22, ox + 6, oy], fill=pants)
        draw.rectangle([ox - 7, oy - 4, ox, oy], fill=shoes)
        draw.rectangle([ox + 1, oy - 4, ox + 7, oy], fill=shoes)

        draw.rectangle([ox - 5, oy - 37, ox + 7, oy - 22], fill=shirt)
        px = ox + 10 if anim_step == 1 else 6
        py = oy - 40 if anim_step == 1 else -32
        draw.line([ox + 4, oy - 32, px, py], fill=skin, width=4)
        draw.rectangle([px - 1, py - 3, px + 5, py + 3], fill=gloves)

        hx, hy = ox + 2, oy - 45
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)
        draw.point((hx + 3, hy), fill=(30, 20, 20, 255))

    elif pose_type == "finisher":
        draw.rectangle([ox - 4, oy - 22, ox + 1, oy], fill=pants_dark)
        draw.rectangle([ox - 5, oy - 4, ox + 1, oy], fill=shoes)

        draw.rectangle([ox - 6, oy - 37, ox + 5, oy - 22], fill=shirt)
        kick_reach = 18 if anim_step >= 1 else 10
        draw.rectangle([ox + 2, oy - 33, ox + 2 + kick_reach, oy - 26], fill=pants)
        draw.rectangle([ox + kick_reach, oy - 34, ox + 6 + kick_reach, oy - 25], fill=shoes)

        hx, hy = ox - 2, oy - 44
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)

    elif pose_type == "jump":
        draw.rectangle([ox - 5, oy - 30, ox + 3, oy - 16], fill=pants)
        draw.rectangle([ox - 4, oy - 17, ox + 4, oy - 12], fill=shoes)
        draw.rectangle([ox - 6, oy - 44, ox + 5, oy - 30], fill=shirt)
        draw.line([ox - 5, oy - 42, ox - 9, oy - 48], fill=skin, width=3)
        draw.line([ox + 5, oy - 42, ox + 9, oy - 48], fill=skin, width=3)

        hx, hy = ox, oy - 50
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)

    elif pose_type == "jump_kick":
        draw.rectangle([ox - 8, oy - 34, ox + 2, oy - 22], fill=shirt)
        draw.line([ox, oy - 24, ox + 18, oy - 14], fill=pants, width=6)
        draw.rectangle([ox + 16, oy - 16, ox + 22, oy - 10], fill=shoes)
        draw.line([ox - 4, oy - 24, ox - 10, oy - 20], fill=pants_dark, width=5)

        hx, hy = ox - 6, oy - 40
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)

    elif pose_type == "special":
        rot = anim_step * 120
        rad = math.radians(rot)
        dx = int(math.cos(rad) * 16)
        dy = int(math.sin(rad) * 8)
        draw.ellipse([ox - 22, oy - 38, ox + 22, oy - 10], outline=(255, 230, 80, 200), width=2)
        draw.rectangle([ox - 6, oy - 40, ox + 6, oy - 18], fill=shirt)
        draw.line([ox, oy - 30, ox + dx, oy - 30 + dy], fill=(255, 255, 255, 255), width=5)
        draw.line([ox, oy - 30, ox - dx, oy - 30 - dy], fill=gloves, width=5)
        draw.rectangle([ox - 4, oy - 18, ox + 4, oy], fill=pants)
        draw.rectangle([ox - 5, oy - 4, ox + 5, oy], fill=shoes)

        hx, hy = ox, oy - 46
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)

    elif pose_type == "hurt":
        draw.rectangle([ox - 7, oy - 22, ox - 2, oy], fill=pants_dark)
        draw.rectangle([ox - 1, oy - 22, ox + 4, oy], fill=pants)
        draw.rectangle([ox - 8, oy - 4, ox - 1, oy], fill=shoes)
        draw.rectangle([ox - 1, oy - 4, ox + 5, oy], fill=shoes)

        draw.polygon([(ox - 10, oy - 36), (ox + 1, oy - 36), (ox + 4, oy - 22), (ox - 6, oy - 22)], fill=shirt)

        hx, hy = ox - 6, oy - 44
        draw.ellipse([hx - 5, hy - 6, hx + 5, hy + 5], fill=skin)
        if headband: draw.line([hx - 5, hy - 1, hx + 5, hy - 1], fill=headband, width=2)
        if char_type == "brawler": draw.rectangle([hx - 2, hy - 11, hx + 2, hy - 4], fill=hair)
        else: draw.ellipse([hx - 6, hy - 9, hx + 5, hy - 2], fill=hair)
        draw.line([hx + 1, hy - 1, hx + 4, hy + 2], fill=(220, 40, 40, 255))
        draw.line([hx + 1, hy + 2, hx + 4, hy - 1], fill=(220, 40, 40, 255))

    elif pose_type == "knockdown":
        if anim_step == 0:
            draw.polygon([(ox - 18, oy - 22), (ox + 8, oy - 26), (ox + 6, oy - 16), (ox - 16, oy - 12)], fill=shirt)
            draw.line([ox + 8, oy - 25, ox + 22, oy - 22], fill=pants, width=6)
            draw.rectangle([ox + 20, oy - 24, ox + 26, oy - 18], fill=shoes)
            hx, hy = ox - 23, oy - 20
            draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=skin)
        elif anim_step == 1:
            draw.polygon([(ox - 16, oy - 14), (ox + 6, oy - 18), (ox + 4, oy - 8), (ox - 14, oy - 4)], fill=shirt)
            draw.line([ox + 6, oy - 16, ox + 18, oy - 12], fill=pants, width=5)
            draw.rectangle([ox + 16, oy - 14, ox + 21, oy - 9], fill=shoes)
            hx, hy = ox - 20, oy - 12
            draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=skin)
        else:
            draw.rectangle([ox - 14, oy - 8, ox + 6, oy - 2], fill=shirt)
            draw.rectangle([ox + 6, oy - 8, ox + 18, oy - 2], fill=pants)
            draw.rectangle([ox + 18, oy - 9, ox + 23, oy - 2], fill=shoes)
            hx, hy = ox - 20, oy - 5
            draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=skin)

def generate_character_sheet(char_type, filename):
    cols, rows = 8, 4
    sheet = Image.new("RGBA", (cols * FRAME_W, rows * FRAME_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    
    frames = [
        (0, 0, "idle", 0), (1, 0, "idle", 1), (2, 0, "idle", 2), (3, 0, "idle", 3),
        (4, 0, "walk", 0), (5, 0, "walk", 1), (6, 0, "walk", 2), (7, 0, "walk", 3),
        (0, 1, "walk", 4), (1, 1, "walk", 5),
        (2, 1, "punch1", 0), (3, 1, "punch1", 1),
        (4, 1, "punch2", 0), (5, 1, "punch2", 1),
        (6, 1, "finisher", 0), (7, 1, "finisher", 1),
        (0, 2, "finisher", 2),
        (1, 2, "jump", 0),
        (2, 2, "jump_kick", 0), (3, 2, "jump_kick", 1),
        (4, 2, "special", 0), (5, 2, "special", 1), (6, 2, "special", 2), (7, 2, "special", 0),
        (0, 3, "hurt", 0), (1, 3, "hurt", 1),
        (2, 3, "knockdown", 0), (3, 3, "knockdown", 1), (4, 3, "knockdown", 2),
        (5, 3, "knockdown", 2),
        (6, 3, "idle", 0), (7, 3, "idle", 0)
    ]
    
    for c, r, pose, step in frames:
        draw_character_frame(draw, c * FRAME_W, r * FRAME_H, char_type, pose, step)
        
    sheet.save(filename)

# 8. NEON CITY STREET BACKGROUNDS
def create_city_backgrounds():
    w_sky, h_sky = 480, 140
    sky = Image.new("RGBA", (w_sky, h_sky), (12, 12, 30, 255))
    dsky = ImageDraw.Draw(sky)
    
    for y in range(h_sky):
        r = int(10 + (y / h_sky) * 20)
        g = int(12 + (y / h_sky) * 25)
        b = int(32 + (y / h_sky) * 45)
        dsky.line([0, y, w_sky, y], fill=(r, g, b, 255))
        
    dsky.ellipse([370, 15, 415, 60], fill=(255, 245, 220, 240))
    dsky.ellipse([378, 22, 408, 52], fill=(255, 255, 240, 255))
    
    buildings = [
        (0, 45, 35, 140, (18, 22, 48, 255)),
        (30, 25, 75, 140, (14, 18, 40, 255)),
        (70, 50, 110, 140, (20, 25, 55, 255)),
        (105, 15, 150, 140, (12, 15, 36, 255)),
        (145, 40, 185, 140, (22, 28, 58, 255)),
        (180, 20, 230, 140, (15, 20, 42, 255)),
        (225, 48, 270, 140, (25, 30, 62, 255)),
        (265, 30, 315, 140, (16, 20, 45, 255)),
        (310, 55, 350, 140, (20, 25, 55, 255)),
        (345, 35, 390, 140, (14, 18, 40, 255)),
        (385, 45, 435, 140, (24, 30, 60, 255)),
        (430, 20, 480, 140, (13, 16, 38, 255)),
    ]
    for x0, y0, x1, y1, color in buildings:
        dsky.rectangle([x0, y0, x1, y1], fill=color)
        mid = (x0 + x1) // 2
        dsky.line([mid, y0 - 10, mid, y0], fill=color, width=2)
        dsky.point((mid, y0 - 11), fill=(255, 50, 50, 255))
        for wy in range(y0 + 8, y1 - 10, 8):
            for wx in range(x0 + 4, x1 - 4, 6):
                if (wx * 7 + wy * 13) % 5 in [0, 2]:
                    dsky.point((wx, wy), fill=(255, 240, 150, 200))
                elif (wx * 11 + wy * 3) % 7 == 0:
                    dsky.point((wx, wy), fill=(0, 240, 255, 180))

    sky.save("assets/backgrounds/skyline.png")

    w_mid, h_mid = 960, 140
    mid_img = Image.new("RGBA", (w_mid, h_mid), (0, 0, 0, 0))
    dmid = ImageDraw.Draw(mid_img)
    
    dmid.rectangle([0, 20, w_mid, 140], fill=(28, 30, 45, 255))
    for by in range(25, 140, 6):
        dmid.line([0, by, w_mid, by], fill=(22, 24, 38, 255))
        shift = 8 if (by // 6) % 2 == 0 else 0
        for bx in range(shift, w_mid, 16):
            dmid.line([bx, by, bx, by + 5], fill=(22, 24, 38, 255))

    # BAR sign
    dmid.rectangle([50, 35, 160, 75], fill=(15, 15, 25, 255), outline=(255, 0, 140, 255), width=2)
    dmid.rectangle([48, 33, 162, 77], outline=(255, 0, 140, 100), width=1)
    dmid.rectangle([65, 42, 68, 68], fill=(255, 60, 180, 255))
    dmid.rectangle([68, 42, 80, 45], fill=(255, 60, 180, 255))
    dmid.rectangle([68, 54, 78, 56], fill=(255, 60, 180, 255))
    dmid.rectangle([68, 65, 80, 68], fill=(255, 60, 180, 255))
    dmid.rectangle([78, 45, 81, 54], fill=(255, 60, 180, 255))
    dmid.rectangle([78, 56, 81, 65], fill=(255, 60, 180, 255))
    dmid.rectangle([88, 42, 91, 68], fill=(255, 60, 180, 255))
    dmid.rectangle([98, 42, 101, 68], fill=(255, 60, 180, 255))
    dmid.rectangle([91, 42, 98, 45], fill=(255, 60, 180, 255))
    dmid.rectangle([91, 54, 98, 56], fill=(255, 60, 180, 255))
    dmid.rectangle([108, 42, 111, 68], fill=(255, 60, 180, 255))
    dmid.rectangle([111, 42, 122, 45], fill=(255, 60, 180, 255))
    dmid.rectangle([111, 54, 120, 56], fill=(255, 60, 180, 255))
    dmid.rectangle([120, 45, 123, 54], fill=(255, 60, 180, 255))
    dmid.line([116, 56, 123, 68], fill=(255, 60, 180, 255), width=2)
    dmid.polygon([(135, 45), (150, 45), (142, 57)], outline=(0, 240, 255, 255), width=2)
    dmid.line([142, 57, 142, 67], fill=(0, 240, 255, 255), width=2)
    dmid.line([136, 67, 148, 67], fill=(0, 240, 255, 255), width=2)

    # ARCADE sign
    dmid.rectangle([340, 30, 500, 75], fill=(10, 15, 30, 255), outline=(0, 230, 255, 255), width=2)
    dmid.rectangle([338, 28, 502, 77], outline=(0, 230, 255, 90), width=1)
    dmid.rectangle([350, 55, 375, 68], fill=(220, 40, 40, 255))
    dmid.line([362, 55, 362, 42], fill=(200, 200, 200, 255), width=3)
    dmid.ellipse([357, 36, 367, 44], fill=(255, 220, 0, 255))
    # Pixel text ARCADE
    dmid.rectangle([385, 42, 490, 68], fill=(0, 20, 50, 200))
    dmid.line([390, 65, 395, 45], fill=(0, 240, 255, 255), width=2)
    dmid.line([395, 45, 400, 65], fill=(0, 240, 255, 255), width=2)
    dmid.line([392, 55, 398, 55], fill=(0, 240, 255, 255), width=2)

    # MOTEL sign
    dmid.rectangle([680, 25, 810, 80], fill=(20, 10, 15, 255), outline=(255, 50, 50, 255), width=2)
    dmid.rectangle([678, 23, 812, 82], outline=(255, 50, 50, 80), width=1)
    # M O T E L
    dmid.rectangle([695, 35, 795, 55], fill=(40, 10, 10, 255))
    dmid.line([700, 50, 700, 38], fill=(255, 60, 60, 255), width=2)
    dmid.line([700, 38, 705, 45], fill=(255, 60, 60, 255), width=2)
    dmid.line([705, 45, 710, 38], fill=(255, 60, 60, 255), width=2)
    dmid.line([710, 38, 710, 50], fill=(255, 60, 60, 255), width=2)

    doors = [220, 560, 860]
    for dx in doors:
        dmid.rectangle([dx, 60, dx + 40, 140], fill=(15, 25, 45, 255), outline=(80, 90, 110, 255), width=2)
        dmid.line([dx + 35, 95, dx + 35, 105], fill=(220, 200, 50, 255), width=2)

    mid_img.save("assets/backgrounds/buildings.png")

    w_road, h_road = 960, 140
    road = Image.new("RGBA", (w_road, h_road), (0, 0, 0, 0))
    droad = ImageDraw.Draw(road)
    
    droad.rectangle([0, 0, w_road, 35], fill=(65, 68, 78, 255))
    droad.line([0, 35, w_road, 35], fill=(120, 125, 140, 255), width=2)
    droad.line([0, 37, w_road, 37], fill=(30, 32, 38, 255), width=2)
    for tx in range(0, w_road, 32):
        droad.line([tx, 0, tx, 35], fill=(50, 53, 62, 255), width=1)
        
    droad.rectangle([0, 38, w_road, 140], fill=(34, 36, 42, 255))
    for y_tex in range(40, 140, 4):
        for x_tex in range(0, w_road, 8):
            if (x_tex * 3 + y_tex * 7) % 11 == 0:
                droad.point((x_tex, y_tex), fill=(44, 46, 54, 255))

    dash_y = 88
    for lx in range(10, w_road, 60):
        droad.rectangle([lx, dash_y, lx + 36, dash_y + 3], fill=(220, 190, 40, 220))
        
    droad.line([0, 138, w_road, 138], fill=(20, 22, 26, 255), width=2)
    
    for mh_x in [180, 520, 840]:
        droad.ellipse([mh_x, 105, mh_x + 36, 120], fill=(25, 27, 30, 255))
        droad.ellipse([mh_x + 2, 107, mh_x + 34, 118], outline=(55, 58, 66, 255), width=2)
        droad.line([mh_x + 8, 112, mh_x + 28, 112], fill=(55, 58, 66, 255), width=2)

    road.save("assets/backgrounds/road.png")

    w_lamp, h_lamp = 32, 90
    lamp = Image.new("RGBA", (w_lamp, h_lamp), (0, 0, 0, 0))
    dlamp = ImageDraw.Draw(lamp)
    dlamp.rectangle([13, 75, 19, 88], fill=(30, 35, 45, 255))
    dlamp.rectangle([11, 86, 21, 90], fill=(50, 55, 68, 255))
    dlamp.rectangle([14, 15, 18, 75], fill=(55, 60, 75, 255))
    dlamp.line([14, 15, 14, 75], fill=(80, 88, 105, 255), width=1)
    dlamp.arc([14, 6, 28, 24], 180, 360, fill=(55, 60, 75, 255), width=3)
    dlamp.rectangle([21, 14, 29, 18], fill=(40, 45, 55, 255))
    dlamp.polygon([(22, 18), (28, 18), (29, 26), (21, 26)], fill=(255, 245, 150, 255))
    dlamp.ellipse([18, 14, 32, 28], outline=(255, 230, 100, 120), width=2)
    lamp.save("assets/backgrounds/streetlamp.png")

print("Generating all retro beat 'em up assets...")
create_shadow()
create_hit_effects()
create_pickups()
create_barrel()
create_go_sign()
create_axel_portrait()
generate_character_sheet("axel", "assets/sprites/player.png")
generate_character_sheet("brawler", "assets/sprites/enemy_brawler.png")
generate_character_sheet("speedy", "assets/sprites/enemy_speedy.png")
create_city_backgrounds()
print("All assets successfully created!")
