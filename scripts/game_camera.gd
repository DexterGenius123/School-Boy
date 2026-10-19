extends Camera2D
class_name GameCamera

@export var follow_target: Node2D = null
@export var min_x: float = 240.0
@export var max_x: float = 1700.0

var is_locked: bool = false
var locked_x: float = 240.0

var shake_amount: float = 0.0
var shake_decay: float = 14.0

func _ready():
	position.x = min_x
	position.y = 135.0 # Center of 270 viewport

func _process(delta: float):
	# Screen shake
	if shake_amount > 0:
		shake_amount = max(0.0, shake_amount - shake_decay * delta)
		offset = Vector2(randf_range(-shake_amount, shake_amount), randf_range(-shake_amount, shake_amount))
	else:
		offset = Vector2.ZERO

	if is_locked:
		position.x = locked_x
		return

	if follow_target and is_instance_valid(follow_target):
		# Camera only scrolls forward (right), never back
		var target_x = max(position.x, follow_target.global_position.x)
		target_x = clamp(target_x, min_x, max_x)
		position.x = lerp(position.x, target_x, 10.0 * delta)

func lock_at(x_pos: float):
	is_locked = true
	locked_x = x_pos

func unlock():
	is_locked = false

func shake(intensity: float):
	shake_amount = max(shake_amount, intensity)
