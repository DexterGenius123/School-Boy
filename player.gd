extends CharacterBody2D

# Скорость движения
export var speed = 200
# Сила прыжка
export var jump_force = -400
# Максимальное здоровье
export var max_health = 100
# Текущее здоровье
var health = 100

# Анимации
onready var animation_player = $AnimationPlayer

func _ready():
    # Устанавливаем начальное здоровье
    health = max_health

func _process(delta):
    # Обработка движения
    var velocity = Vector2.ZERO
    if Input.is_action_pressed("ui_right"):
        velocity.x += 1
    if Input.is_action_pressed("ui_left"):
        velocity.x -= 1
    if Input.is_action_just_pressed("ui_jump"):
        if is_on_floor():
            velocity.y = jump_force

    # Умножаем скорость на delta для фиксированной скорости
    velocity.x *= speed * delta

    # Перемещаем игрока
    velocity = move_and_slide(velocity)

    # Обработка атаки
    if Input.is_action_just_pressed("ui_attack"):
        attack()

    # Обновляем анимацию
    update_animation(velocity)

func attack():
    # Логика атаки
    print("Attack!")
    animation_player.play("attack")

func take_damage(amount):
    health -= amount
    if health <= 0:
        die()

func die():
    print("Player died!")
    animation_player.play("die")
    # Добавьте логику для завершения игры или перезапуска уровня

func update_animation(velocity):
    if velocity.x != 0:
        animation_player.play("run")
    elif is_on_floor():
        animation_player.play("idle")
    else:
        animation_player.play("jump")
