extends Node2D

@onready var sprite: Sprite2D = $Sprite2D
@onready var label: Label = $Label

var current_frame: int = 0
var frame_timer: float = 0.0
var frame_duration: float = 0.04
var total_frames: int = 4

func _ready():
	z_index = 100 # Always on top of characters
	if label:
		label.position.y = -10
		label.modulate = Color(1.0, 1.0, 0.2, 1.0)

func setup(damage_amount: int = 0, is_heavy: bool = false):
	if label:
		if damage_amount > 0:
			label.text = str(damage_amount)
			if is_heavy:
				label.text += "!"
				label.modulate = Color(1.0, 0.3, 0.2, 1.0)
		else:
			label.text = ""

func _process(delta: float):
	frame_timer += delta
	if label and label.text != "":
		label.position.y -= 30.0 * delta
		label.modulate.a -= 2.0 * delta
		
	if frame_timer >= frame_duration:
		frame_timer -= frame_duration
		current_frame += 1
		if current_frame >= total_frames:
			queue_free()
		else:
			if sprite:
				sprite.frame = current_frame
