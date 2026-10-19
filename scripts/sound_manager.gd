class_name SoundManager
extends Node

static var instance = null

var sounds = {}
var sfx_players: Array[AudioStreamPlayer] = []
var max_players = 8
var bgm_player: AudioStreamPlayer

func _enter_tree():
	instance = self

func _ready():
	instance = self
	process_mode = Node.PROCESS_MODE_ALWAYS
	
	var sound_files = {
		"punch": "res://assets/sounds/punch.wav",
		"heavy_hit": "res://assets/sounds/heavy_hit.wav",
		"whoosh": "res://assets/sounds/whoosh.wav",
		"jump": "res://assets/sounds/jump.wav",
		"hurt": "res://assets/sounds/hurt.wav",
		"knockdown": "res://assets/sounds/knockdown.wav",
		"special": "res://assets/sounds/special.wav",
		"pickup": "res://assets/sounds/pickup.wav",
		"go": "res://assets/sounds/go.wav",
		"clear": "res://assets/sounds/clear.wav"
	}
	
	for s_name in sound_files:
		var path = sound_files[s_name]
		if ResourceLoader.exists(path):
			sounds[s_name] = load(path)
	
	# Create SFX player pool
	for i in range(max_players):
		var p = AudioStreamPlayer.new()
		add_child(p)
		sfx_players.append(p)
		
	# BGM player
	bgm_player = AudioStreamPlayer.new()
	add_child(bgm_player)
	var bgm_path = "res://assets/sounds/bgm.wav"
	if ResourceLoader.exists(bgm_path):
		var bgm_stream = load(bgm_path)
		bgm_player.stream = bgm_stream
		bgm_player.volume_db = -6.0
		bgm_player.finished.connect(_on_bgm_finished)
		bgm_player.play()

func _on_bgm_finished():
	if bgm_player:
		bgm_player.play()

static func get_singleton():
	if not instance:
		var tree = Engine.get_main_loop() as SceneTree
		if tree and tree.root:
			var found = tree.root.get_node_or_null("SoundManager")
			if found:
				instance = found
			else:
				var sm = SoundManager.new()
				sm.name = "SoundManager"
				tree.root.add_child.call_deferred(sm)
				instance = sm
	return instance

static func play_sfx(s_name: String, pitch_scale: float = 1.0, volume_db: float = 0.0):
	var inst = get_singleton()
	if inst:
		inst._do_play_sfx(s_name, pitch_scale, volume_db)

func _do_play_sfx(s_name: String, pitch_scale: float = 1.0, volume_db: float = 0.0):
	if not sounds.has(s_name) or sounds[s_name] == null:
		return
	
	for p in sfx_players:
		if not p.playing:
			p.stream = sounds[s_name]
			p.pitch_scale = pitch_scale + randf_range(-0.05, 0.05)
			p.volume_db = volume_db
			p.play()
			return
			
	if not sfx_players.is_empty():
		var fallback = sfx_players[0]
		fallback.stream = sounds[s_name]
		fallback.pitch_scale = pitch_scale
		fallback.volume_db = volume_db
		fallback.play()
