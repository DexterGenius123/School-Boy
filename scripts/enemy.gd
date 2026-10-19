extends CharacterBody2D
class_name Enemy

enum Type { BRAWLER, SPEEDY }
enum State {
	IDLE,
	APPROACH,
	ATTACK,
	HURT,
	KNOCKDOWN,
	DEAD
}

@export var enemy_type: Type = Type.BRAWLER
@export var max_health: int = 50

var enemy_name: String = "GALSIA"
var health: int = 50
var current_state: State = State.IDLE

var speed_x: float = 75.0
var speed_y: float = 55.0
var attack_damage: int = 10
var attack_range_x: float = 34.0
var attack_depth_y: float = 12.0

var facing_dir: int = -1
var state_timer: float = 0.0
var attack_cooldown: float = 0.0
var invincible_timer: float = 0.0

# Z height physics
var z_pos: float = 0.0
var z_vel: float = 0.0
var gravity: float = 800.0

# Visuals
var anim_timer: float = 0.0
var flash_timer: float = 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var shadow: Sprite2D = $Shadow
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var tex_brawler = preload("res://assets/sprites/enemy_brawler.png")
var tex_speedy = preload("res://assets/sprites/enemy_speedy.png")
var hit_effect_scene = preload("res://scenes/HitEffect.tscn")
var pickup_scene = preload("res://scenes/Pickup.tscn")

var player_target: Player = null
var hud: CanvasLayer = null

signal enemy_died(enemy_node)

func _ready():
	add_to_group("enemies")
	y_sort_enabled = true
	setup_type(enemy_type)
	hud = get_tree().get_first_node_in_group("hud")

func setup_type(type: Type):
	enemy_type = type
	if not is_inside_tree() or not sprite:
		return
		
	match type:
		Type.BRAWLER:
			enemy_name = "GALSIA"
			max_health = 50
			health = max_health
			speed_x = 75.0
			speed_y = 55.0
			attack_damage = 10
			sprite.texture = tex_brawler
		Type.SPEEDY:
			enemy_name = "SIGNAL"
			max_health = 40
			health = max_health
			speed_x = 105.0
			speed_y = 75.0
			attack_damage = 14
			sprite.texture = tex_speedy

func is_dead() -> bool:
	return current_state == State.DEAD or health <= 0

func _process(delta: float):
	if flash_timer > 0:
		flash_timer -= delta
		if flash_timer <= 0:
			sprite.modulate = Color.WHITE

	if invincible_timer > 0:
		invincible_timer -= delta
		sprite.visible = (int(invincible_timer * 16.0) % 2 == 0)
	else:
		sprite.visible = true

	if attack_cooldown > 0:
		attack_cooldown -= delta

	update_ai(delta)
	update_physics(delta)
	update_animation(delta)

func update_ai(delta: float):
	if current_state in [State.HURT, State.KNOCKDOWN, State.DEAD]:
		return

	if not player_target or not is_instance_valid(player_target):
		player_target = get_tree().get_first_node_in_group("player")
		if not player_target:
			current_state = State.IDLE
			velocity = Vector2.ZERO
			return

	var diff = player_target.global_position - global_position
	var dist_x = abs(diff.x)
	var dist_y = abs(diff.y)

	# Face player
	facing_dir = 1 if diff.x > 0 else -1

	if current_state == State.ATTACK:
		state_timer -= delta
		if state_timer <= 0.18 and state_timer > 0.08:
			# Strike moment
			execute_attack()
		elif state_timer <= 0:
			current_state = State.IDLE
			attack_cooldown = randf_range(0.6, 1.2)
		return

	# In attack range?
	if dist_x <= attack_range_x and dist_y <= attack_depth_y:
		velocity = Vector2.ZERO
		if attack_cooldown <= 0:
			start_attack()
		else:
			current_state = State.IDLE
		return

	# AI Movement: Align Y depth first, then close in on X
	current_state = State.APPROACH
	var move_dir = Vector2.ZERO

	if dist_y > attack_depth_y * 0.7:
		move_dir.y = sign(diff.y)

	# Only approach on X if close to alignment or far away
	if dist_x > attack_range_x * 0.8:
		move_dir.x = sign(diff.x)
	elif dist_x < attack_range_x * 0.4:
		# Too close, back off slightly
		move_dir.x = -sign(diff.x)

	velocity = Vector2(move_dir.x * speed_x, move_dir.y * speed_y)

func start_attack():
	current_state = State.ATTACK
	state_timer = 0.35 # 0.17s windup, 0.10s strike, 0.08s recover
	velocity = Vector2.ZERO
	if SoundManager:
		SoundManager.play_sfx("whoosh")

func execute_attack():
	if not player_target or not is_instance_valid(player_target):
		return
	var diff = player_target.global_position - global_position
	var in_reach = (diff.x * facing_dir) > 0 and abs(diff.x) <= attack_range_x + 5.0 and abs(diff.y) <= attack_depth_y + 4.0
	if in_reach:
		var knock_dir = Vector2(facing_dir, 0.0)
		player_target.take_damage(attack_damage, false, knock_dir)

func take_damage(amount: int, is_heavy: bool, knock_dir: Vector2, hit_pos: Vector2):
	if is_dead():
		return

	health -= amount
	flash_timer = 0.08
	if sprite:
		sprite.modulate = Color(2.5, 2.5, 2.5, 1.0)

	if hud:
		hud.show_enemy_health(enemy_name, health, max_health)

	var fx = hit_effect_scene.instantiate()
	fx.global_position = global_position + Vector2(0, -26 - z_pos)
	fx.setup(amount, is_heavy)
	get_parent().add_child(fx)

	if health <= 0:
		die(knock_dir)
		return

	if is_heavy or z_pos > 5.0:
		current_state = State.KNOCKDOWN
		state_timer = 0.8
		z_vel = 180.0
		velocity = knock_dir * 130.0
		invincible_timer = 1.3
		if SoundManager:
			SoundManager.play_sfx("knockdown")
	else:
		current_state = State.HURT
		state_timer = 0.22
		velocity = knock_dir * 45.0
		if SoundManager:
			SoundManager.play_sfx("punch")

func die(knock_dir: Vector2):
	current_state = State.DEAD
	state_timer = 1.2
	velocity = knock_dir * 140.0
	z_vel = 160.0
	collision_shape.set_deferred("disabled", true)
	if SoundManager:
		SoundManager.play_sfx("knockdown")
		
	# Chance to drop Apple or Gold
	if randf() < 0.35:
		call_deferred("spawn_loot")

	enemy_died.emit(self)

	var tween = create_tween()
	tween.tween_interval(0.8)
	tween.tween_property(self, "modulate:a", 0.0, 0.5)
	tween.tween_callback(queue_free)

func spawn_loot():
	var p = pickup_scene.instantiate()
	p.global_position = global_position
	var type = Pickup.Type.APPLE if randf() < 0.5 else Pickup.Type.GOLD
	p.setup(type, 20.0)
	get_parent().add_child(p)

func update_physics(delta: float):
	# Z height physics
	if z_pos > 0 or z_vel > 0:
		z_vel -= gravity * delta
		z_pos += z_vel * delta
		if z_pos <= 0:
			z_pos = 0
			z_vel = 0

	if current_state == State.KNOCKDOWN:
		velocity = velocity.move_toward(Vector2.ZERO, 300.0 * delta)
	elif current_state == State.HURT:
		velocity = velocity.move_toward(Vector2.ZERO, 350.0 * delta)
	elif current_state == State.DEAD:
		velocity = velocity.move_toward(Vector2.ZERO, 250.0 * delta)

	move_and_slide()

	# State timer transitions
	if current_state == State.HURT:
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
			var f = int(anim_timer * 6.0) % 4
			sprite.frame = f
		State.APPROACH:
			var f = 4 + (int(anim_timer * 8.0) % 6)
			sprite.frame = f
		State.ATTACK:
			if state_timer > 0.18:
				sprite.frame = 10 # Windup
			else:
				sprite.frame = 11 # Strike punch
		State.HURT:
			sprite.frame = 24 if state_timer > 0.11 else 25
		State.KNOCKDOWN:
			if z_pos > 10.0:
				sprite.frame = 26
			elif state_timer > 0.35:
				sprite.frame = 27
			else:
				sprite.frame = 28
		State.DEAD:
			sprite.frame = 29
