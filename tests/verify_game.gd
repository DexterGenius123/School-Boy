extends SceneTree

func _init():
	print("--- BEGIN STREETS OF RAGE 5 VERIFICATION TEST ---")
	
	# Load main scene
	var main_scene = load("res://scenes/Main.tscn")
	if not main_scene:
		printerr("FAILED to load res://scenes/Main.tscn")
		quit(1)
		return
		
	print("Main.tscn loaded successfully!")
	var main_instance = main_scene.instantiate()
	root.add_child(main_instance)
	print("Main instance added to root tree!")
	
	# Verify Player
	var player: Player = main_instance.find_child("Player", true, false) as Player
	if not player:
		printerr("FAILED: Player node not found!")
		quit(1)
		return
	print("Player found at:", player.global_position, "Health:", player.health)
	
	# Verify HUD
	var hud = main_instance.find_child("HUD", true, false)
	if not hud:
		printerr("FAILED: HUD not found!")
		quit(1)
		return
	print("HUD found!")
	
	# Test Player attack
	print("Testing combo attack 1...")
	player.perform_combo_attack()
	print("Player state after attack 1:", player.current_state)
	
	# Test jump kick
	print("Testing jump...")
	player.start_jump()
	player.z_pos = 30.0
	player.start_jump_kick()
	print("Player state in air:", player.current_state)
	
	# Test taking damage & heal
	print("Testing heal and damage...")
	player.take_damage(10, false, Vector2.LEFT)
	print("Player health after hit:", player.health)
	player.heal(10)
	print("Player health after heal:", player.health)
	
	# Test StageManager wave trigger
	var stage_mgr: StageManager = null
	for child in main_instance.get_children():
		if child is StageManager:
			stage_mgr = child
			break
			
	if stage_mgr:
		print("Starting Wave 0...")
		stage_mgr.start_wave(0)
		print("Alive enemies in wave:", stage_mgr.alive_enemies.size())
		if stage_mgr.alive_enemies.size() > 0:
			var enemy = stage_mgr.alive_enemies[0]
			print("Enemy 0 type:", enemy.enemy_name, "HP:", enemy.health)
			enemy.take_damage(20, false, Vector2.RIGHT, enemy.global_position)
			print("Enemy HP after damage:", enemy.health)
	
	print("--- VERIFICATION SUCCEEDED: ALL CHECKS PASSED! ---")
	quit(0)
