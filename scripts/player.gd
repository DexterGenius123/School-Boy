extends CharacterBody2D
class_name Player

enum State {
	IDLE,
	WALK,
	JUMP,
	ATTACK1,
	ATTACK2,
	FINISHER,
	JUMP_KICK,
	SPECIAL,
	HURT,
	KNOCKDOWN,
	DEAD
}

@export var speed_x: float = 130.0
@export var speed_y: float = 90.0
@export var max_health: int = 100
@export var lives: int = 2

var health: int = 100
var score: int = 0
var current_state: State = State.IDLE

# Jump / Vertical height simulation
var z_pos: float = 0.0
var z_vel: float = 0.0
var gravity: float = 800.0
var jump_force: float = 270.0

# Combat & Combo
var combo_step: int = 0
var combo_timer: float = 0.0
var state_timer: float = 0.0
var facing_dir: int = 1 # 1 = right, -1 = left
var invincible_timer: float = 0.0
var hit_stop_timer: float = 0.0
var attack_has_hit: bool = false

# Animation frame timers
var anim_timer: float = 0.0
var anim_frame: int = 0

@onready var sprite: Sprite2D = $Sprite2D
@onready var shadow: Sprite2D = $Shadow
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var hit_effect_scene = preload("res://scenes/HitEffect.tscn")
var hud: CanvasLayer

# Boundaries for street playfield
var min_y: float = 120.0
var max_y: float = 255.0
var min_x: float = 20.0
var max_x: float = 1900.0

func _ready():
	add_to_group("player")
	health = max_health
	y_sort_enabled = true
	hud = get_tree().get_first_node_in_group("hud")
	if hud:
		hud.update_player_hp(health, max_health)
		hud.update_lives(lives)
		hud.update_score(score)

func _process(delta: float):
	if hit_stop_timer > 0:
		hit_stop_timer -= delta
		return

	if invincible_timer > 0:
		invincible_timer -= delta
		sprite.visible = (int(invincible_timer * 16.0) % 2 == 0)
	else:
		sprite.visible = true

	# Combo reset timer
	if combo_timer > 0:
		combo_timer -= delta
		if combo_timer <= 0:
			combo_step = 0

	handle_input(delta)
	update_physics(delta)
	update_animation(delta)

func handle_input(_delta: float):
	if current_state in [State.HURT, State.KNOCKDOWN, State.DEAD]:
		return

	# Special attack
	if Input.is_action_just_pressed("special") or Input.is_key_pressed(KEY_L) or Input.is_key_pressed(KEY_C):
		if current_state in [State.IDLE, State.WALK, State.ATTACK1, State.ATTACK2] and health > 5:
			perform_special()
			return

	# Jump
	if Input.is_action_just_pressed("jump") or Input.is_key_pressed(KEY_K) or Input.is_key_pressed(KEY_X) or Input.is_key_pressed(KEY_SPACE):
		if current_state in [State.IDLE, State.WALK]:
			start_jump()
			return

	# Attack
	if Input.is_action_just_pressed("attack") or Input.is_key_pressed(KEY_J) or Input.is_key_pressed(KEY_Z) or Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		if current_state == State.JUMP:
			start_jump_kick()
			return
		elif current_state in [State.IDLE, State.WALK]:
			perform_combo_attack()
			return
		elif current_state in [State.ATTACK1, State.ATTACK2] and state_timer > 0.08:
			# Combo buffer
			perform_combo_attack()
			return

func start_jump():
	current_state = State.JUMP
	z_vel = jump_force
	if SoundManager:
		SoundManager.play_sfx("jump")

func start_jump_kick():
	current_state = State.JUMP_KICK
	attack_has_hit = false
	if SoundManager:
		SoundManager.play_sfx("whoosh")
	check_attack_hit(22, true, 38.0, 18.0)

func perform_combo_attack():
	attack_has_hit = false
	velocity = Vector2.ZERO
	
	if combo_step == 0:
		current_state = State.ATTACK1
		state_timer = 0.20
		combo_step = 1
		combo_timer = 0.45
		if SoundManager:
			SoundManager.play_sfx("whoosh")
		check_attack_hit(12, false, 34.0, 14.0)
	elif combo_step == 1:
		current_state = State.ATTACK2
		state_timer = 0.22
		combo_step = 2
		combo_timer = 0.45
		if SoundManager:
			SoundManager.play_sfx("whoosh")
		check_attack_hit(16, false, 36.0, 14.0)
	elif combo_step == 2:
		current_state = State.FINISHER
		state_timer = 0.32
		combo_step = 0
		combo_timer = 0.0
		if SoundManager:
			SoundManager.play_sfx("whoosh")
		check_attack_hit(28, true, 42.0, 16.0)

func perform_special():
	current_state = State.SPECIAL
	state_timer = 0.40
	attack_has_hit = false
	invincible_timer = 0.45
	velocity = Vector2.ZERO
	take_damage_internal(5, false) # Costs 5 HP
	if SoundManager:
		SoundManager.play_sfx("special")
	# 360 hit around player
	check_area_hit(32, true, 55.0, 24.0)

func check_attack_hit(damage: int, is_heavy: bool, reach_x: float, depth_y: float):
	if not is_inside_tree():
		return
	var targets_hit = 0
	
	# Enemies
	var enemies = get_tree().get_nodes_in_group("enemies")
	for e in enemies:
		if not is_instance_valid(e) or e.is_dead():
			continue
		var diff = e.global_position - global_position
		# Check horizontal reach according to facing direction
		var in_front = (diff.x * facing_dir) > -5.0 and abs(diff.x) <= reach_x
		var in_depth = abs(diff.y) <= depth_y
		
		if in_front and in_depth:
			var hit_dir = Vector2(facing_dir, 0.0)
			e.take_damage(damage, is_heavy, hit_dir, global_position)
			targets_hit += 1
			add_combo_hit()
			
	# Hittable objects (barrels, etc.)
	var barrels = get_tree().get_nodes_in_group("hittable")
	for b in barrels:
		if not is_instance_valid(b) or not b.has_method("take_damage"):
			continue
		var diff = b.global_position - global_position
		var in_front = (diff.x * facing_dir) > -5.0 and abs(diff.x) <= reach_x
		var in_depth = abs(diff.y) <= depth_y
		if in_front and in_depth:
			b.take_damage(damage, is_heavy, global_position)
			targets_hit += 1

	if targets_hit > 0:
		attack_has_hit = true
		hit_stop_timer = 0.05
		shake_camera(3.0 if is_heavy else 1.5)

func check_area_hit(damage: int, is_heavy: bool, radius_x: float, radius_y: float):
	if not is_inside_tree():
		return
	var enemies = get_tree().get_nodes_in_group("enemies")
	var hit_count = 0
	for e in enemies:
		if not is_instance_valid(e) or e.is_dead():
			continue
		var diff = e.global_position - global_position
		if abs(diff.x) <= radius_x and abs(diff.y) <= radius_y:
			var knock_dir = Vector2(sign(diff.x) if diff.x != 0 else facing_dir, 0.0)
			e.take_damage(damage, is_heavy, knock_dir, global_position)
			hit_count += 1
			add_combo_hit()

	if hit_count > 0:
		hit_stop_timer = 0.06
		shake_camera(4.0)

func add_combo_hit():
	if hud:
		var current_combo = 3 if combo_step == 0 else combo_step
		hud.show_combo(current_combo)
	add_score(150)

func add_score(amount: int):
	score += amount
	if hud:
		hud.update_score(score)

func heal(amount: int):
	health = min(max_health, health + amount)
	if hud:
		hud.update_player_hp(health, max_health)

func take_damage(amount: int, is_heavy: bool = false, knock_dir: Vector2 = Vector2.ZERO):
	if invincible_timer > 0 or current_state == State.DEAD:
		return
	take_damage_internal(amount, is_heavy, knock_dir)

func take_damage_internal(amount: int, is_heavy: bool = false, knock_dir: Vector2 = Vector2.ZERO):
	health -= amount
	if hud:
		hud.update_player_hp(health, max_health)

	var fx = hit_effect_scene.instantiate()
	fx.global_position = global_position + Vector2(0, -25 - z_pos)
	fx.setup(amount, is_heavy)
	get_parent().add_child(fx)

	if health <= 0:
		die()
		return

	if is_heavy or z_pos > 5.0:
		current_state = State.KNOCKDOWN
		state_timer = 1.0
		z_vel = 180.0
		velocity = knock_dir * 120.0
		invincible_timer = 1.6
		if SoundManager:
			SoundManager.play_sfx("knockdown")
	else:
		current_state = State.HURT
		state_timer = 0.25
		velocity = knock_dir * 40.0
		invincible_timer = 0.4
		if SoundManager:
			SoundManager.play_sfx("hurt")

func die():
	current_state = State.DEAD
	state_timer = 2.0
	velocity = Vector2(-facing_dir * 60.0, 0.0)
	z_vel = 140.0
	lives -= 1
	if hud:
		hud.update_lives(lives)
	if SoundManager:
		SoundManager.play_sfx("knockdown")

	if lives < 0:
		if hud:
			hud.show_game_over()
	else:
		# Respawn after 2 seconds
		var tween = create_tween()
		tween.tween_interval(1.8)
		tween.tween_callback(respawn)

func respawn():
	health = max_health
	current_state = State.IDLE
	z_pos = 100.0 # Drop from top
	z_vel = 0.0
	invincible_timer = 2.0
	if hud:
		hud.update_player_hp(health, max_health)

func update_physics(delta: float):
	# Z height physics (Jumping / falling)
	if z_pos > 0 or z_vel > 0:
		z_vel -= gravity * delta
		z_pos += z_vel * delta
		if z_pos <= 0:
			z_pos = 0
			z_vel = 0
			if current_state in [State.JUMP, State.JUMP_KICK]:
				current_state = State.IDLE

	# Ground movement
	if current_state in [State.IDLE, State.WALK, State.JUMP]:
		var input_vec = Vector2.ZERO
		if Input.is_action_pressed("move_left") or Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
			input_vec.x -= 1
		if Input.is_action_pressed("move_right") or Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
			input_vec.x += 1
		if Input.is_action_pressed("move_up") or Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
			input_vec.y -= 1
		if Input.is_action_pressed("move_down") or Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
			input_vec.y += 1

		if input_vec.x != 0:
			facing_dir = 1 if input_vec.x > 0 else -1

		if current_state != State.JUMP:
			if input_vec != Vector2.ZERO:
				current_state = State.WALK
				velocity = Vector2(input_vec.x * speed_x, input_vec.y * speed_y)
			else:
				current_state = State.IDLE
				velocity = Vector2.ZERO
		else:
			# Air steering
			velocity.x = input_vec.x * (speed_x * 0.9)
			velocity.y = input_vec.y * (speed_y * 0.9)
	elif current_state == State.KNOCKDOWN:
		velocity = velocity.move_toward(Vector2.ZERO, 300.0 * delta)
	elif current_state == State.HURT:
		velocity = velocity.move_toward(Vector2.ZERO, 400.0 * delta)
	else:
		velocity = Vector2.ZERO

	move_and_slide()

	# Clamp to walkable street area
	global_position.y = clamp(global_position.y, min_y, max_y)
	global_position.x = clamp(global_position.x, min_x, max_x)

	# State timers
	if current_state in [State.ATTACK1, State.ATTACK2, State.FINISHER, State.SPECIAL, State.HURT]:
		state_timer -= delta
		if state_timer <= 0:
			current_state = State.IDLE
	elif current_state == State.KNOCKDOWN:
		state_timer -= delta
		if state_timer <= 0 and z_pos == 0:
			current_state = State.IDLE

func update_animation(delta: float):
	if not sprite:
		return
	sprite.flip_h = (facing_dir == -1)
	sprite.position.y = -z_pos

	anim_timer += delta

	match current_state:
		State.IDLE:
			var frame_idx = int(anim_timer * 6.0) % 4
			sprite.frame = frame_idx # Row 0: 0..3
		State.WALK:
			var frame_idx = 4 + (int(anim_timer * 9.0) % 6)
			if frame_idx >= 8:
				sprite.frame = frame_idx # Row 1: 8, 9
			else:
				sprite.frame = frame_idx # Row 0: 4, 5, 6, 7
		State.JUMP:
			sprite.frame = 17
		State.JUMP_KICK:
			sprite.frame = 18 if (z_pos > 20) else 19
		State.ATTACK1:
			sprite.frame = 10 if state_timer > 0.1 else 11
		State.ATTACK2:
			sprite.frame = 12 if state_timer > 0.11 else 13
		State.FINISHER:
			if state_timer > 0.20:
				sprite.frame = 14
			elif state_timer > 0.08:
				sprite.frame = 15
			else:
				sprite.frame = 16
		State.SPECIAL:
			var spin_step = int((0.40 - state_timer) * 10.0) % 4
			sprite.frame = 20 + spin_step
		State.HURT:
			sprite.frame = 24 if state_timer > 0.12 else 25
		State.KNOCKDOWN:
			if z_pos > 10.0:
				sprite.frame = 26
			elif state_timer > 0.4:
				sprite.frame = 27
			else:
				sprite.frame = 28
		State.DEAD:
			sprite.frame = 29

func shake_camera(intensity: float):
	var cam = get_viewport().get_camera_2d()
	if cam and cam.has_method("shake"):
		cam.shake(intensity)
