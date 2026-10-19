extends Node2D
class_name StageManager

@export var camera: GameCamera
@export var player: Player
@export var y_sort_world: Node2D

var enemy_scene = preload("res://scenes/Enemy.tscn")
var barrel_scene = preload("res://scenes/Barrel.tscn")

var hud: CanvasLayer = null

var current_wave: int = 0
var alive_enemies: Array[Enemy] = []
var stage_finished: bool = false

# Waves definitions
# Trigger X, Lock Camera X, Spawns: Array of [Enemy.Type, spawn_offset_x, spawn_y]
var waves = [
	{
		"trigger_x": 180.0,
		"lock_x": 240.0,
		"spawns": [
			[Enemy.Type.BRAWLER, 400.0, 160.0],
			[Enemy.Type.BRAWLER, 440.0, 220.0]
		],
		"barrels": [
			[290.0, 180.0]
		]
	},
	{
		"trigger_x": 600.0,
		"lock_x": 680.0,
		"spawns": [
			[Enemy.Type.BRAWLER, 820.0, 150.0],
			[Enemy.Type.SPEEDY, 860.0, 200.0],
			[Enemy.Type.BRAWLER, 880.0, 230.0]
		],
		"barrels": [
			[740.0, 210.0]
		]
	},
	{
		"trigger_x": 1100.0,
		"lock_x": 1200.0,
		"spawns": [
			[Enemy.Type.SPEEDY, 1380.0, 140.0],
			[Enemy.Type.BRAWLER, 1400.0, 180.0],
			[Enemy.Type.SPEEDY, 1420.0, 210.0],
			[Enemy.Type.BRAWLER, 1440.0, 240.0]
		],
		"barrels": [
			[1260.0, 170.0],
			[1290.0, 220.0]
		]
	}
]

func _ready():
	hud = get_tree().get_first_node_in_group("hud")

func _process(_delta: float):
	# Restart key
	if Input.is_key_pressed(KEY_R):
		get_tree().reload_current_scene()
		return

	if stage_finished or not player or not is_instance_valid(player):
		return

	# Check wave triggers
	if current_wave < waves.size():
		var w = waves[current_wave]
		if player.global_position.x >= w["trigger_x"] and alive_enemies.is_empty():
			start_wave(current_wave)
	else:
		# Check stage clear trigger (player reaches end of street)
		if player.global_position.x >= 1550.0:
			stage_finished = true
			if hud:
				hud.show_victory()

func start_wave(wave_idx: int):
	var w = waves[wave_idx]
	if camera:
		camera.lock_at(w["lock_x"])
	if hud:
		hud.show_go_sign(false)

	# Spawn Barrels
	if w.has("barrels"):
		for b_data in w["barrels"]:
			var b = barrel_scene.instantiate()
			b.global_position = Vector2(b_data[0], b_data[1])
			y_sort_world.add_child(b)

	# Spawn Enemies
	for sp in w["spawns"]:
		var en = enemy_scene.instantiate()
		en.global_position = Vector2(sp[1], sp[2])
		en.enemy_died.connect(_on_enemy_died)
		y_sort_world.add_child(en)
		en.setup_type(sp[0])
		alive_enemies.append(en)

func _on_enemy_died(enemy_node: Enemy):
	if alive_enemies.has(enemy_node):
		alive_enemies.erase(enemy_node)

	if alive_enemies.is_empty():
		wave_cleared()

func wave_cleared():
	current_wave += 1
	if camera:
		camera.unlock()
	if hud:
		hud.show_go_sign(true)
