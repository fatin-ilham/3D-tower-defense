# Authors:
# 22301068 - Mushfique Tajwar
# 22301130 - Aryan Rayeen Rahman
# 22301327 - Md. Obaidullah Ahrar

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Map Configuration
MAP_SIZE          = 1500
ZONE              = 600
FORTRESS_ZONE     = 250

# Viewpoint Settings
cam_pos           = (0, 600, 600)
cam_angle         = 0
cam_dist          = 600
cam_height        = 550
cam_min_h         = 400
cam_max_h         = 1400

# Game States
god_mode          = False
visor_on          = False
match_over        = False
wave_halt         = False
reward_selected   = False
fps_mode          = False

# Hero Stats
hero_pos          = [0, 0, 0]
hero_spd          = 10
points            = 0
hp                = 100
hero_rot          = 5
max_hp            = 100

# Weapon System
turret_rot        = 180
turret_pos        = [30, 15, 80]
projectiles       = []
failed_shots      = 0
shot_limit        = 50

# Hostiles
hostiles          = []
spawn_count       = 5
foe_spd           = 0.025
pulse_scale       = 1.0
pulse_timer       = 0
wave_sizes        = [5, 7, 9, 11, 13, 15, 17, 19, 21]

# Hostile Projectiles
foe_projectiles   = []
foe_shot_cd       = {}
foe_dmg           = 1
foe_fire_cd       = 300

# Defense System
defenses          = []
def_projectiles   = []
def_fire_cd       = {}
def_range         = 600
def_dmg           = 3
def_fire_rate     = 200

wave_num          = 1
fortress_radius   = 60
eliminations      = 0
kills_needed      = 10

build_mode        = False
build_cursor      = [400, 400]
GLUT_BITMAP_HELVETICA_18 = GLUT_BITMAP_HELVETICA_18
foliage_count     = 0
currency          = 100

def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(color[0], color[1], color[2])
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 650)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(font, ord(character))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def render_objects():
    render_floor()
    render_fortress()
    render_foliage()
    for tx, ty, level in defenses:
        glPushMatrix()
        glTranslatef(tx, ty, 10)
        
        scale = 1.0 if level == 1 else 1.2 if level == 2 else 1.5
        glScalef(scale, scale, scale)
        
        color = (0.5, 0.5, 0.5) if level == 1 else (0.5, 0.7, 0.5) if level == 2 else (0.7, 0.5, 0.5)
        glColor3f(color[0], color[1], color[2])
        gluCylinder(gluNewQuadric(), 40, 45, 180, 20, 20)

        # Top Battlements
        glTranslatef(0, 0, 180)
        for i in range(8):
            angle = i * 45
            x = 50 * math.cos(math.radians(angle))
            y = 50 * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, y, 0)
            glRotatef(angle, 0, 0, 1)
            glColor3f(0.4, 0.4, 0.4)
            glScalef(1, 1, 1.5)
            glutSolidCube(15)
            glPopMatrix()

        # Flagpole
        glColor3f(0.6, 0.3, 0.1)
        gluCylinder(gluNewQuadric(), 1.5, 1.5, 40, 10, 10)

        # Flag
        glTranslatef(0, 0, 40)
        glColor3f(1, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(20, 8, 0)
        glVertex3f(0, 16, 0)
        glEnd()
        glPopMatrix()

    if not match_over:
        for t in hostiles:
            render_foe(*t)
        for s in projectiles:
            render_projectile(s[0], s[1], s[2])
        for es in foe_projectiles:
            render_foe_shot(es[0], es[1], es[2])
        for ts in def_projectiles:
            render_def_shot(ts[0], ts[1], ts[2])

def render_floor():
    # Render map floor
    glBegin(GL_QUADS)
    for i in range(-MAP_SIZE, MAP_SIZE + 1, 100):
        for j in range(-MAP_SIZE, MAP_SIZE + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(0, 0.2, 0)
            else:
                glColor3f(0, 0.3, 0)
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)
    glEnd()

    # Render conquered zone
    glBegin(GL_QUADS)
    for i in range(-ZONE, ZONE + 1, 100):
        for j in range(-ZONE, ZONE + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(0, 0.4, 0)
            else:
                glColor3f(0, 0.5, 0)
            glVertex3f(i, j, 2)
            glVertex3f(i + 100, j, 2)
            glVertex3f(i + 100, j + 100, 2)
            glVertex3f(i, j + 100, 2)
    glEnd()

    # Render fortress zone
    glBegin(GL_QUADS)
    for i in range(-FORTRESS_ZONE, FORTRESS_ZONE, 100):
        for j in range(-FORTRESS_ZONE, FORTRESS_ZONE, 100):
            if (i + j) % 200 == 0:
                glColor3f(0.8, 0.8, 0.8)
            else:
                glColor3f(1, 1, 1)
            glVertex3f(i, j, 9)
            glVertex3f(i + 100, j, 9)
            glVertex3f(i + 100, j + 100, 9)
            glVertex3f(i, j + 100, 9)
    glEnd()
    # Boundary

    glBegin(GL_QUADS)
    glColor3f(0, 0, 0)

    glVertex3f(-ZONE, -ZONE, 0)
    glVertex3f(-ZONE, ZONE + 100, 0)
    glVertex3f(-ZONE, ZONE + 100, 30)
    glVertex3f(-ZONE, -ZONE, 30)

    glVertex3f(ZONE + 100, -ZONE, 0)
    glVertex3f(ZONE + 100, ZONE + 100, 0)
    glVertex3f(ZONE + 100, ZONE + 100, 30)
    glVertex3f(ZONE + 100, -ZONE, 30)

    glVertex3f(-ZONE, ZONE + 100, 0)
    glVertex3f(ZONE + 100, ZONE + 100, 0)
    glVertex3f(ZONE + 100, ZONE + 100, 30)
    glVertex3f(-ZONE, ZONE + 100, 30)

    glVertex3f(-ZONE, -ZONE, 0)
    glVertex3f(ZONE + 100, -ZONE, 0)
    glVertex3f(ZONE + 100, -ZONE, 30)
    glVertex3f(-ZONE, -ZONE, 30)
    glEnd()
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)

    # Walls
    glVertex3f(-MAP_SIZE, -MAP_SIZE, 0)
    glVertex3f(-MAP_SIZE, MAP_SIZE + 100, 0)
    glVertex3f(-MAP_SIZE, MAP_SIZE + 100, 100)
    glVertex3f(-MAP_SIZE, -MAP_SIZE, 100)

    glVertex3f(MAP_SIZE + 100, -MAP_SIZE, 0)
    glVertex3f(MAP_SIZE + 100, MAP_SIZE + 100, 0)
    glVertex3f(MAP_SIZE + 100, MAP_SIZE + 100, 100)
    glVertex3f(MAP_SIZE + 100, -MAP_SIZE, 100)

    glVertex3f(-MAP_SIZE, MAP_SIZE + 100, 0)
    glVertex3f(MAP_SIZE + 100, MAP_SIZE + 100, 0)
    glVertex3f(MAP_SIZE + 100, MAP_SIZE + 100, 100)
    glVertex3f(-MAP_SIZE, MAP_SIZE + 100, 100)

    glVertex3f(-MAP_SIZE, -MAP_SIZE, 0)
    glVertex3f(MAP_SIZE + 100, -MAP_SIZE, 0)
    glVertex3f(MAP_SIZE + 100, -MAP_SIZE, 100)
    glVertex3f(-MAP_SIZE, -MAP_SIZE, 100)
    glEnd()

def render_foliage():
    rng = random.Random(42)
    foliage_count = 70
    for i in range(foliage_count):
        x = rng.randint(-MAP_SIZE + 200, MAP_SIZE - 200)
        y = rng.randint(-MAP_SIZE + 200, MAP_SIZE - 200)
        if math.sqrt(x**2 + y**2) >= 500:
            glPushMatrix()
            glTranslatef(x, y, 0)
            glColor3f(0.4*i/70, 0.2*i/70, 0.1)
            gluCylinder(gluNewQuadric(), 12, 12, 70, 10, 10)
            glTranslatef(0, 0, 70)
            glColor3f(0.0, 0.6*i/70, 0.0)
            gluSphere(gluNewQuadric(), 40, 15, 15)
            glPopMatrix()

def render_fortress():
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    for dx, dy in [(-60, -60), (60, -60), (-60, 60), (60, 60)]:
        glPushMatrix()
        glTranslatef(dx, dy, 0)
        glScalef(1, 1, 2)
        glutSolidCube(100)
        glPopMatrix()
    glPopMatrix()
    glColor3f(0.6, 0.6, 0.6)
    for dx, dy in [(-100, 0), (100, 0), (0, -100), (0, 100)]:
        glPushMatrix()
        glTranslatef(dx, dy, 50)
        glScalef(1.2, 1.2, 2.2)
        glutSolidCube(60)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(dx, dy, 120)
        for i in range(8):
            angle = i * 45
            x = 35 * math.cos(math.radians(angle))
            y = 35 * math.sin(math.radians(angle))
            glPushMatrix()
            glTranslatef(x, y, 0)
            glColor3f(0.5, 0.5, 0.5)
            glutSolidCube(12)
            glPopMatrix()
        glPopMatrix()
    glColor3f(1, 0, 0)  # Crimson flags
    for dx, dy in [(-100, 0), (100, 0), (0, -100), (0, 100)]:
        glPushMatrix()
        glTranslatef(dx, dy, 150)
        # Flag pole
        glColor3f(0.6, 0.3, 0.1)
        gluCylinder(gluNewQuadric(), 1.5, 1.5, 40, 10, 10)
        # Flag
        glTranslatef(0, 0, 40)
        glColor3f(1, 0, 0)
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(25, 10, 0)
        glVertex3f(0, 20, 0)
        glEnd()
        glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glColor3f(0.4, 0.4, 0.9)
    gluCylinder(gluNewQuadric(), 40, 50, 200, 20, 20)
    glTranslatef(0, 0, 200)
    for i in range(12):
        angle = i * 30
        x = 50 * math.cos(math.radians(angle))
        y = 50 * math.sin(math.radians(angle))
        glPushMatrix()
        glTranslatef(x, y, 0)
        glColor3f(0.5, 0.5, 0.6)
        glutSolidCube(12)
        glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,0,200)
    glRotatef(turret_rot, 0, 0, 1)
    # Legs
    glTranslatef(0, 0, 0)
    glColor3f(0.1, 0.1, 0.7)
    gluCylinder(gluNewQuadric(), 6, 12, 45, 10, 10)
    glTranslatef(30, 0, 0)
    glColor3f(0.1, 0.1, 0.7)
    gluCylinder(gluNewQuadric(), 6, 12, 45, 10, 10)
    # Body
    glTranslatef(-15, 0, 70)
    glColor3f(0.7, 0.7, 0)
    glutSolidCube(40)
    # Head
    glTranslatef(0, 0, 40)
    glColor3f(0.95, 0.85, 0.75)
    gluSphere(gluNewQuadric(), 20, 12, 12)
    # Arms
    glTranslatef(20, -60, -30)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.95, 0.85, 0.75)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    glRotatef(90, 1, 0, 0)
    glTranslatef(-45, 60, -40)
    glRotatef(0, 1, 0, 0)
    glColor3f(0.95, 0.85, 0.75)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    # Hat
    glColor3f(1, 1, 0)
    glTranslatef(25, 0, 87)
    glutSolidCone(12, 40, 16, 16)  # Base radius = 12, height = 40
    glTranslatef(-10, -15, -17)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 5, 12, 12)
    glTranslatef(20, 0, 0)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 5, 12, 12)
    glPopMatrix()

def spawn_defense():
    while True:
        x = random.randint(-ZONE + 100, ZONE - 100)
        y = random.randint(-ZONE + 100, ZONE - 100)
        if math.sqrt(x**2 + y**2) > 200:  # Avoid center
            return (x, y)

def render_foe(x, y, z, type="normal", health=1):
    glPushMatrix()
    glTranslatef(x, y, z + 35)
    if type == "boss":
        glScalef(2, 2, 2)
        glColor3f(1, 0, 1)
    else:
        if not wave_halt:
            glScalef(pulse_scale, pulse_scale, pulse_scale)
        glColor3f(0, 0, abs(pulse_scale))
    # Lower Body (Upside-down Cone)
    glPushMatrix()
    glTranslatef(0,0,35)
    glRotatef(180, 1, 0, 0)  # Rotate the cone upside down
    glutSolidCone(25, 70, 16, 16)  # Base radius = 35, height = 50
    glPopMatrix()
    # Head
    glTranslatef(0, 0, 50)
    glColor3f(0, 0, 0)  # Black color for the head
    gluSphere(gluNewQuadric(), 15, 12, 12)
    # Hat
    glPushMatrix()
    glColor3f(0.5, 0, 0)  # Red color for the hat
    glTranslatef(0, 0, 20)
    glutSolidCone(12, 40, 16, 16)  # Base radius = 12, height = 40
    glPopMatrix()
    glPopMatrix()

def render_projectile(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 0.5, 0)
    glutSolidCube(8)
    glPopMatrix()

def render_def_shot(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0, 0.7, 1)  # Azure color for defense shots
    glutSolidCone(4, 12, 8, 8)  # Cone shape for defense shots
    glPopMatrix()

def render_foe_shot(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 0, 0)  # Crimson color for hostile shots
    glutSolidSphere(5, 8, 8)  # Sphere for hostile shots
    glPopMatrix()

def fire_weapon():
    global projectiles
    if fps_mode:
        ang = math.radians(turret_rot + 45)
        x = hero_pos[0] + (turret_pos[0] + 5) * \
            math.sin(ang) - turret_pos[1] * math.cos(ang)
        y = hero_pos[1] - (turret_pos[0] + 5) * \
            math.cos(ang) - turret_pos[1] * math.sin(ang)
        z = hero_pos[2] + turret_pos[2]
        shot = [x, y, z, turret_rot]
    else:
        ang = math.radians(turret_rot - 90)
        off_x = turret_pos[0] * \
            math.cos(ang) - turret_pos[1] * math.sin(ang)
        off_y = turret_pos[0] * \
            math.sin(ang) + turret_pos[1] * math.cos(ang)
        x = hero_pos[0] + off_x
        y = hero_pos[1] + off_y
        z = hero_pos[2] + turret_pos[2]
        shot = [x, y, z, turret_rot]
    projectiles.append(shot)

def update_projectiles():
    global projectiles, failed_shots, hostiles, match_over
    if wave_halt:
        return
    to_remove = []
    for s in projectiles:
        ang = math.radians(s[3] - 90)
        s[0] += 2 * math.cos(ang)
        s[1] += 2 * math.sin(ang)
        if (s[0] > ZONE + 100 or s[0] < -ZONE or
                s[1] > ZONE + 100 or s[1] < -ZONE):
            to_remove.append(s)
            if not god_mode:
                failed_shots += 1
    for s in to_remove:
        if s in projectiles:
            projectiles.remove(s)
    if failed_shots >= shot_limit:
        match_over = True

def foe_fire(x, y, z):
    global foe_projectiles
    dx = hero_pos[0] - x
    dy = hero_pos[1] - y
    ang = math.atan2(dy, dx)
    ang += random.uniform(-0.1, 0.1)
    foe_projectiles.append([x, y, z + 70, ang])

def update_hostiles():
    global hostiles, hp, match_over, foe_spd, foe_shot_cd
    if wave_halt:
        return
    for t in hostiles:
        enemy_id = id(t)
        if enemy_id not in foe_shot_cd:
            foe_shot_cd[enemy_id] = random.randint(
                60, foe_fire_cd)
    for t in hostiles[:]:
        dx = hero_pos[0] - t[0]
        dy = hero_pos[1] - t[1]
        dist = math.sqrt(dx*dx + dy*dy)
        enemy_id = id(t)
        if enemy_id in foe_shot_cd:
            foe_shot_cd[enemy_id] -= 1
            if foe_shot_cd[enemy_id] <= 0 and not god_mode:
                foe_fire(t[0], t[1], t[2])
                foe_shot_cd[enemy_id] = foe_fire_cd + \
                    random.randint(-30, 30)
        if dist < 50:
            if not god_mode:
                hp -= 5
                if hp <= 0:
                    match_over = True
                    hostiles.clear()
                    projectiles.clear()
                    foe_projectiles.clear()
                    break
            if t in hostiles:
                hostiles.remove(t)
                if enemy_id in foe_shot_cd:
                    del foe_shot_cd[enemy_id]
            spawn_hostiles(1)
        else:
            ang = math.atan2(dy, dx)
            speed = foe_spd * 0.3 if t[3] == "boss" else foe_spd
            t[0] += speed * math.cos(ang)
            t[1] += speed * math.sin(ang)
    timer_keys = list(foe_shot_cd.keys())
    for enemy_id in timer_keys:
        if not any(id(t) == enemy_id for t in hostiles):
            del foe_shot_cd[enemy_id]
    if not hostiles:
        advance_wave()

def check_collisions():
    global projectiles, hostiles, points, eliminations, currency
    if wave_halt:
        return
    for s in projectiles[:]:
        s_x, s_y = s[0], s[1]
        for t in hostiles[:]:
            t_x, t_y = t[0], t[1]
            dx, dy = s_x - t_x, s_y - t_y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= 70:
                points += 1
                eliminations += 1
                currency += 10
                if s in projectiles:
                    projectiles.remove(s)
                t[4] -= 1
                if t[4] <= 0:
                    if t in hostiles:
                        hostiles.remove(t)
                    max_foes = (
                        wave_sizes[wave_num-1]
                        if wave_num <= len(wave_sizes)
                        else wave_sizes[-1] + 2 * (wave_num - len(wave_sizes))
                    )
                    if eliminations >= kills_needed:
                        advance_wave()
                    elif len(hostiles) < max_foes:
                        spawn_hostiles(1)
                break

def defense_fire(tower_idx, tx, ty, level=1):
    global def_projectiles, hostiles
    fire_rate = def_fire_rate * 0.7 if level >= 2 else def_fire_rate
    damage = def_dmg * 2 if level == 3 else def_dmg
    closest_foe = None
    min_dist = def_range
    for t in hostiles:
        dx = tx - t[0]
        dy = ty - t[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < min_dist:
            min_dist = dist
            closest_foe = t
    if closest_foe:
        ex, ey, ez, etype, ehealth = closest_foe
        dx = ex - tx
        dy = ey - ty
        ang = math.atan2(dy, dx)
        ang += random.uniform(-0.05, 0.05)
        def_projectiles.append([tx, ty, 160, ang, damage])
        return True
    return False

def update_defenses():
    global def_fire_cd, defenses
    if wave_halt:
        return
    for i, (tx, ty, level) in enumerate(defenses):
        fire_rate = def_fire_rate * 0.7 if level >= 2 else def_fire_rate
        if i in def_fire_cd:
            def_fire_cd[i] -= 1
            if def_fire_cd[i] <= 0:
                if defense_fire(i, tx, ty, level):
                    def_fire_cd[i] = fire_rate
                else:
                    def_fire_cd[i] = 60
        else:
            def_fire_cd[i] = random.randint(60, int(fire_rate))

def update_def_shots():
    global def_projectiles, hostiles, points, eliminations
    if wave_halt:
        return
    to_remove_shots = []
    to_remove_foes = []
    for shot in def_projectiles:
        shot[0] += 3 * math.cos(shot[3])
        shot[1] += 3 * math.sin(shot[3])
        if (shot[0] > ZONE + 100 or shot[0] < -ZONE or
                shot[1] > ZONE + 100 or shot[1] < -ZONE):
            to_remove_shots.append(shot)
            continue
        for t in hostiles:
            if t in to_remove_foes:
                continue
            dx = shot[0] - t[0]
            dy = shot[1] - t[1]
            dist = math.sqrt(dx*dx + dy*dy)
            damage = shot[4] if len(shot) > 4 else def_dmg
            if dist < 40:
                points += 1
                eliminations += 1
                to_remove_shots.append(shot)
                t[4] -= damage
                if t[4] <= 0:
                    to_remove_foes.append(t)
                break
    for shot in to_remove_shots:
        if shot in def_projectiles:
            def_projectiles.remove(shot)
    for t in to_remove_foes:
        if t in hostiles:
            hostiles.remove(t)
            if eliminations >= kills_needed:
                advance_wave()
            else:
                max_foes = (
                    wave_sizes[wave_num-1]
                    if wave_num <= len(wave_sizes)
                    else wave_sizes[-1] + 2 * (wave_num - len(wave_sizes))
                )
                if len(hostiles) < max_foes:
                    spawn_hostiles(1)

def animate_foes():
    global pulse_timer, pulse_scale
    pulse_timer += 0.01
    pulse_scale = 1.0 + 0.4 * math.cos(pulse_timer)

def get_foe_angles():
    angles = []
    for t in hostiles:
        dx, dy = hero_pos[0] - t[0], hero_pos[1] - t[1]
        ang = math.degrees(math.atan2(dy, dx)) - 90
        angles.append((ang + 360) % 360)
    return angles

def render_crosshair():
    if visor_on:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 800, 0, 650)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(400, 340)
        glVertex2f(400, 310)
        glVertex2f(380, 325)
        glVertex2f(400, 340)
        glVertex2f(420, 325)
        glVertex2f(400, 340)
        glEnd()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def spawn_hostiles(count=spawn_count):
    global hostiles, n
    max_foes = wave_sizes[wave_num - 1] if wave_num <= len(wave_sizes) else 15
    if len(hostiles) + count > max_foes:
        count = max(0, max_foes - len(hostiles))
    if wave_num < 4:
        n = wave_num
    for _ in range(count):
        x = random.uniform(-ZONE + 50, ZONE - 50)
        y = random.uniform(-ZONE + 50, ZONE - 50)
        z = random.uniform(0, 10)
        while abs(x) < 200:
            x = random.uniform(-ZONE + (100*n), ZONE - 100)
        while abs(y) < 200:
            y = random.uniform(-ZONE + (100*n), ZONE - 100)
        is_boss = (wave_num % 3 == 0) and (len(hostiles) == 0)
        if is_boss:
            hostiles.append([x, y, z, "boss", 10])
        else:
            hostiles.append([x, y, z, "normal", 1])

def update_foe_shots():
    global foe_projectiles, hp, match_over
    if wave_halt:
        return
    to_remove = []
    for shot in foe_projectiles:
        shot[0] += 1.5 * math.cos(shot[3])
        shot[1] += 1.5 * math.sin(shot[3])
        if (shot[0] > MAP_SIZE + 100 or shot[0] < -MAP_SIZE or shot[1] > MAP_SIZE + 100 or shot[1] < -MAP_SIZE):
            to_remove.append(shot)
            continue
        dx = hero_pos[0] - shot[0]
        dy = hero_pos[1] - shot[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < fortress_radius:
            if not god_mode:
                hp -= foe_dmg
                if hp <= 0:
                    match_over = True
                    hostiles.clear()
                    projectiles.clear()
                    foe_projectiles.clear()
            to_remove.append(shot)
    for shot in to_remove:
        if shot in foe_projectiles:
            foe_projectiles.remove(shot)

def advance_wave():
    global wave_num, fortress_radius, foe_spd, ZONE, wave_halt, reward_selected
    global hp, max_hp, points, failed_shots, kills_needed, eliminations, currency
    wave_num += 1
    eliminations = 0
    foe_spd += 0.25
    wave_halt = True
    kills_needed += 10
    hp = max_hp
    if wave_num < 5:
        fortress_radius += 20
        ZONE += 300
    if wave_num <= len(wave_sizes):
        spawn_count = wave_sizes[wave_num-1]
    else:
        spawn_count = wave_sizes[-1] + 2 * (wave_num - len(wave_sizes))

def restart_match():
    global match_over, fps_mode, god_mode, visor_on, failed_shots, ZONE, defenses, foe_spd, wave_num
    global hp, max_hp, points, hero_pos, turret_rot, fortress_radius
    global def_projectiles, def_fire_cd, wave_halt, reward_selected, kills_needed, eliminations, currency
    match_over, fps_mode = False, False
    god_mode, visor_on, wave_halt, reward_selected = False, False, False, False
    hero_pos = [0, 0, 0]
    defenses = []
    ZONE = 600
    max_hp = 100
    foe_spd = 0.025
    wave_num = 1
    eliminations = 0
    fortress_radius = 60
    kills_needed  = 10
    turret_rot, hp, max_hp, points, failed_shots, currency = 180, 100, 100, 0, 0, 100
    projectiles.clear()
    hostiles.clear()
    def_projectiles.clear()
    def_fire_cd.clear()
    spawn_hostiles()

def on_key_press(key, x, y):
    global god_mode, fps_mode, match_over, visor_on, turret_rot,cam_pos, cam_angle
    global hero_pos, hero_spd, hero_rot, hp, max_hp, points, failed_shots
    global wave_halt, reward_selected, defenses, def_fire_cd, build_mode, build_cursor, currency
    if wave_halt:
        if build_mode:
            if key == b's' and build_cursor[1] < ZONE - 50:
                build_cursor[1] += 50
            elif key == b'w' and build_cursor[1] > -ZONE + 50:
                build_cursor[1] -= 50
            elif key == b'd' and build_cursor[0] > -ZONE + 50:
                build_cursor[0] -= 50
            elif key == b'a' and build_cursor[0] < ZONE - 50:
                build_cursor[0] += 50
            elif key == b'\r':
                if (abs(build_cursor[0]) > FORTRESS_ZONE or
                        abs(build_cursor[1]) > FORTRESS_ZONE):
                    if len(defenses) < 5 and currency >= 50:
                        defenses.append(tuple(build_cursor) + (1,))
                        def_fire_cd[len(defenses)-1] = random.randint(60, def_fire_rate)
                        currency -= 50
                    build_mode = False
                    wave_halt = False
                    reward_selected = True
                    fps_mode = not fps_mode
                    visor_on = fps_mode
                    hero_rot = 2.5 if fps_mode else 5
                    spawn_hostiles(spawn_count)
                    
            return

        if key == b'1':
            spawn_hostiles(spawn_count)
            max_hp += 100
            hp = max_hp
            wave_halt = False
            reward_selected = True
            return
        elif key == b'2':
            if wave_num > 4:
                reward_selected = True
                return
            build_mode = True
            build_cursor = [400, 400]
            fps_mode = False
            visor_on = False
            hero_rot = 2.5 if fps_mode else 5
            cam_pos, cam_angle = (0, 600, 600), 0
            return
        return

    if match_over and key != b'r':
        return
    elif key == b'c':
        if god_mode:
            projectiles.clear()
            god_mode = False
        else:
            god_mode = True
    elif key == b'v':
        if fps_mode and god_mode:
            visor_on = not visor_on
    elif key == b'r' and match_over:
        restart_match()
    elif key == b'u':
        if defenses:
            min_dist = float('inf')
            nearest_idx = -1
            for i, (tx, ty, level) in enumerate(defenses):
                if level < 3:
                    dist = math.sqrt((tx - hero_pos[0])**2 + (ty - hero_pos[1])**2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_idx = i
            if nearest_idx >= 0 and currency >= 30:
                tx, ty, level = defenses[nearest_idx]
                defenses[nearest_idx] = (tx, ty, level + 1)
                currency -= 30
    if key == b'p':
        hp = 1000
    if not god_mode:
        turret_rot %= 360
        if key == b'd':
            turret_rot -= 5
        if key == b'a':
            turret_rot += 5

def on_special_key(key, x, y):
    global cam_angle, cam_dist, cam_height, cam_min_h, cam_max_h
    if not match_over:
        if key == GLUT_KEY_UP:
            if cam_height > cam_min_h:
                cam_height -= 20
        elif key == GLUT_KEY_DOWN:
            if cam_height < cam_max_h:
                cam_height += 20
        elif key == GLUT_KEY_LEFT:
            cam_angle -= 5
        elif key == GLUT_KEY_RIGHT:
            cam_angle += 5

def on_mouse(button, state, x, y):
    global fps_mode, hero_rot, visor_on, match_over
    if match_over:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not god_mode:
            fire_weapon()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fps_mode = not fps_mode
        visor_on = fps_mode
        hero_rot = 2.5 if fps_mode else 5

def configure_camera():
    global cam_pos, cam_angle, cam_dist, cam_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100, 1.25, 0.3, 2700)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if fps_mode:
        angle = math.radians(turret_rot)
        eye_x = hero_pos[0] + (turret_pos[0]*1.2 *math.sin(angle)) - (turret_pos[1]*0.6*math.cos(angle))
        eye_y = hero_pos[1] - (turret_pos[0]*1.2 *math.cos(angle)) - (turret_pos[1]*0.6*math.sin(angle))
        eye_z = hero_pos[2] + turret_pos[2] + 200
        cen_x = eye_x - math.sin(-angle) * 100
        cen_y = eye_y - math.cos(-angle) * 100
        cen_z = eye_z
        gluLookAt(eye_x, eye_y, eye_z + 50, cen_x, cen_y, cen_z - 30, 0, 0, 1)
    else:
        angle = math.radians(cam_angle)
        x = cam_dist * math.sin(angle)
        y = cam_dist * math.cos(angle)
        z = cam_height
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)
        
def game_tick():
    global points
    animate_foes()
    if wave_halt:
        hostiles.clear()
        glutPostRedisplay()
        return
    if not match_over:
        if god_mode and hostiles:
            t = hostiles[0]
            ang = math.degrees(math.atan2(t[1] - hero_pos[1], t[0] - hero_pos[0]))
            turret_rot = (ang + 360) % 360
            fire_weapon()
        update_hostiles()
        update_foe_shots()
        update_defenses()
        update_def_shots()
        update_projectiles()
        check_collisions()
    glutPostRedisplay()

def render_skybox():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 650)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_QUADS)
    glColor3f(0.63, 0.81, 0.98)
    glVertex2f(0, 650)
    glVertex2f(800, 650)
    glColor3f(0.07, 0.11, 0.21)
    glVertex2f(800, 0)
    glVertex2f(0, 0)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

def display_frame():
    global match_over, hp, max_hp, points, failed_shots, wave_halt, build_mode
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 800, 650)
    render_skybox()
    configure_camera()
    render_objects()
    if visor_on:
        render_crosshair()
    if wave_halt:
        if build_mode:
            glPushMatrix()
            glTranslatef(build_cursor[0], build_cursor[1], 10)
            glScalef(pulse_scale, pulse_scale, pulse_scale)
            glColor3f(0, 1, 1)
            glutSolidSphere(20, 16, 16)
            glPopMatrix()
            render_text(200, 400, "Use W, A, S, D to move the marker", color=(1, 1, 0))
            render_text(200, 350, "Press Enter to place the defense (Can't place on white tiles)", color=(0, 1, 0))
        else:
            if wave_num < 5:
                render_text(200, 400, f"Wave {wave_num-1} Completed! More zone conquered and health restored.", color=(1, 1, 0))
                render_text(200, 350, "Choose your reward:", color=(1, 0.7, 0.2))
                render_text(200, 300, "Press [1] to increase base fortress health by 100", color=(0, 1, 0))
                render_text(200, 250, "Press [2] to add an archer defense inside the zone", color=(0, 0.7, 1))
                render_text(200, 200, "A new wave of invaders are coming and they are faster!!!", color=(1, 0, 0))
            else:
                render_text(200, 400, f"Wave {wave_num-1} Completed! Max health increased by 100", color=(1, 1, 0))
                render_text(200, 300, "Press [1] to continue", color=(0, 1, 0))
                render_text(200, 250, "A new wave of invaders are coming and they are faster!!!", color=(1, 0, 0))
    elif not match_over:
        render_text(10, 650 - 25, f"Fortress Health: {hp}/{max_hp}", color=(0, 0, 0))
        render_text(10, 650 - 55, f"Player Score: {points}")
        render_text(10, 650 - 85, f"Shots Missed: {failed_shots}")
        render_text(10, 650 - 115, f"Currency: {currency}", color=(1, 0.8, 0))
        render_text(350, 625, f"Wave {wave_num}", color=(0, 0, 0))
        remaining = kills_needed - eliminations
        color = (1, 0, 0) if remaining > 5 else (1, 0.5, 0) if remaining > 2 else (0, 1, 0)
        render_text(580, 650 - 25, f"Foes to Eliminate: {remaining}", color=(0, 0, 0))
        render_text(580, 650 - 55, f"Total Foes: {len(hostiles)}")
    else:
        render_text(10, 650 - 25, f"Match Over! Your Score is {points}")
        render_text(10, 650 - 55, 'Press "R" to RESTART the Match')
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 650)
glutCreateWindow(b"Tower Defense")
spawn_hostiles()
glutDisplayFunc(display_frame)
glutIdleFunc(game_tick)
glutKeyboardFunc(on_key_press)
glutSpecialFunc(on_special_key)
glutMouseFunc(on_mouse)
glutMainLoop()