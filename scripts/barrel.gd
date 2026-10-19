extends StaticBody2D
class_name Barrel

@export var health: int = 2
@export var contains_pickup: bool = true

@onready var sprite: Sprite2D = $Sprite2D
@onready var shadow: Sprite2D = $Shadow
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var pickup_scene = preload("res://scenes/Pickup.tscn")
var hit_effect_scene = preload("res://scenes/HitEffect.tscn")

var is_destroyed: bool = false
var flash_timer: float = 0.0

func _ready():
	add_to_group("hittable")
	y_sort_enabled = true

func _process(delta: float):
	if flash_timer > 0:
		flash_timer -= delta
		if flash_timer <= 0:
			sprite.modulate = Color.WHITE

func take_damage(amount: int, is_heavy: bool = false, hit_pos: Vector2 = Vector2.ZERO):
	if is_destroyed:
		return
		
	health -= 1
	flash_timer = 0.1
	sprite.modulate = Color(2.0, 2.0, 2.0, 1.0)
	
	if SoundManager:
		SoundManager.play_sfx("punch" if health > 0 else "heavy_hit")
		
	var fx = hit_effect_scene.instantiate()
	fx.global_position = global_position + Vector2(0, -16)
	fx.setup(amount, is_heavy)
	get_parent().add_child(fx)
	
	if health <= 0 or is_heavy:
		destroy()

func destroy():
	if is_destroyed:
		return
	is_destroyed = true
	collision_shape.set_deferred("disabled", true)
	sprite.frame = 1 # Broken barrel frame
	
	if contains_pickup:
		spawn_pickup()
		
	# Fade out
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 0.0, 0.8)
	tween.tween_callback(queue_free)

func spawn_pickup():
	var p = pickup_scene.instantiate()
	p.global_position = global_position
	# Choose type: 40% Chicken, 30% Apple, 30% Gold
	var r = randf()
	var type = Pickup.Type.CHICKEN
	if r < 0.35:
		type = Pickup.Type.CHICKEN
	elif r < 0.65:
		type = Pickup.Type.APPLE
	else:
		type = Pickup.Type.GOLD
		
	p.setup(type, 20.0)
	get_parent().call_deferred("add_child", p)
