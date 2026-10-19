extends Area2D
class_name Pickup

enum Type { CHICKEN, APPLE, GOLD }

@export var pickup_type: Type = Type.CHICKEN

@onready var sprite: Sprite2D = $Sprite2D
@onready var shadow: Sprite2D = $Shadow
@onready var label: Label = $Label

var z_pos: float = 20.0
var z_vel: float = 80.0
var z_gravity: float = 350.0
var bounce_count: int = 2

var tex_chicken = preload("res://assets/sprites/pickup_chicken.png")
var tex_apple = preload("res://assets/sprites/pickup_apple.png")
var tex_gold = preload("res://assets/sprites/pickup_gold.png")

var collected: bool = false

func _ready():
	y_sort_enabled = true
	update_appearance()
	body_entered.connect(_on_body_entered)

func setup(type: Type, drop_z: float = 25.0):
	pickup_type = type
	z_pos = drop_z
	z_vel = 80.0
	update_appearance()

func update_appearance():
	if not is_inside_tree() or not sprite:
		return
	match pickup_type:
		Type.CHICKEN:
			sprite.texture = tex_chicken
		Type.APPLE:
			sprite.texture = tex_apple
		Type.GOLD:
			sprite.texture = tex_gold

func _process(delta: float):
	if collected:
		label.position.y -= 30.0 * delta
		label.modulate.a -= 2.0 * delta
		if label.modulate.a <= 0:
			queue_free()
		return
		
	# Bouncing physics
	if z_pos > 0 or z_vel > 0:
		z_vel -= z_gravity * delta
		z_pos += z_vel * delta
		if z_pos <= 0:
			z_pos = 0
			if bounce_count > 0:
				bounce_count -= 1
				z_vel = -z_vel * 0.4
			else:
				z_vel = 0
	
	sprite.position.y = -z_pos

func _on_body_entered(body: Node2D):
	if collected:
		return
	if body.is_in_group("player"):
		collect(body)

func collect(player_node: Node2D):
	collected = true
	if SoundManager:
		SoundManager.play_sfx("pickup")
		
	var text = ""
	match pickup_type:
		Type.CHICKEN:
			player_node.heal(50)
			text = "+50 HP"
		Type.APPLE:
			player_node.heal(20)
			text = "+20 HP"
		Type.GOLD:
			if player_node.has_method("add_score"):
				player_node.add_score(1000)
			text = "+1000"
			
	sprite.visible = false
	shadow.visible = false
	label.text = text
	label.visible = true
	label.modulate = Color(1.0, 0.9, 0.2, 1.0)
