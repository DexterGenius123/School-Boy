extends CanvasLayer

@onready var player_hp_bar: ProgressBar = $TopLeft/HealthBar
@onready var player_hp_under: ProgressBar = $TopLeft/HealthBarUnder
@onready var score_label: Label = $TopLeft/ScoreLabel
@onready var lives_label: Label = $TopLeft/LivesLabel

@onready var enemy_panel: Control = $TopRight
@onready var enemy_name_label: Label = $TopRight/EnemyName
@onready var enemy_hp_bar: ProgressBar = $TopRight/EnemyHealthBar

@onready var combo_label: Label = $Center/ComboLabel
@onready var go_sign: TextureRect = $Center/GoSign
@onready var game_over_panel: Control = $Center/GameOverPanel
@onready var victory_panel: Control = $Center/VictoryPanel

var enemy_hide_timer: float = 0.0
var go_blink_timer: float = 0.0
var is_go_active: bool = false
var combo_timer: float = 0.0

func _ready():
	enemy_panel.visible = false
	combo_label.visible = false
	go_sign.visible = false
	game_over_panel.visible = false
	victory_panel.visible = false
	
	var player = get_tree().get_first_node_in_group("player")
	if player:
		update_player_hp(player.health, player.max_health)
		update_lives(player.lives)
		update_score(player.score)

func update_player_hp(current: int, max_hp: int):
	if not player_hp_bar or not player_hp_under:
		return
	player_hp_bar.max_value = max_hp
	player_hp_bar.value = current
	player_hp_under.max_value = max_hp
	var tween = create_tween()
	tween.tween_property(player_hp_under, "value", float(current), 0.35)

func update_score(score: int):
	if not score_label:
		return
	score_label.text = "SCORE %06d" % score

func update_lives(lives: int):
	if not lives_label:
		return
	lives_label.text = "x %d" % max(0, lives)

func show_enemy_health(enemy_name: String, current_hp: int, max_hp: int):
	enemy_panel.visible = true
	enemy_name_label.text = enemy_name.to_upper()
	enemy_hp_bar.max_value = max_hp
	enemy_hp_bar.value = current_hp
	enemy_hide_timer = 2.5

func show_combo(hits: int):
	if hits < 2:
		return
	combo_label.visible = true
	var comment = ""
	if hits == 2:
		comment = "NICE!"
	elif hits == 3:
		comment = "GREAT!"
	elif hits >= 4:
		comment = "EXCELLENT!!"
		
	combo_label.text = "%d HITS!\n%s" % [hits, comment]
	combo_label.scale = Vector2(1.2, 1.2)
	var tween = create_tween()
	tween.tween_property(combo_label, "scale", Vector2.ONE, 0.15)
	combo_timer = 1.2

func show_go_sign(active: bool):
	is_go_active = active
	go_sign.visible = active
	if active and SoundManager:
		SoundManager.play_sfx("go")

func show_game_over():
	game_over_panel.visible = true

func show_victory():
	victory_panel.visible = true
	if SoundManager:
		SoundManager.play_sfx("clear")

func _process(delta: float):
	# Enemy target bar auto-hide
	if enemy_hide_timer > 0:
		enemy_hide_timer -= delta
		if enemy_hide_timer <= 0:
			enemy_panel.visible = false

	# Combo timeout
	if combo_timer > 0:
		combo_timer -= delta
		if combo_timer <= 0:
			combo_label.visible = false

	# GO sign blinking
	if is_go_active:
		go_blink_timer += delta
		go_sign.visible = (int(go_blink_timer * 4.0) % 2 == 0)
