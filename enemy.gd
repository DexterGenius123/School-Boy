extends CharacterBody2D

# Скорость движения
export var speed = 100
# Максимальное здоровье
export var max_health = 50
# Текущее здоровье
var health = 50

# Анимации
onready var animation_player = $AnimationPlayer

func _ready():
    # Устанавливаем начальное здоровье
    health = max_health

func _process(delta):
    # Обработка движения
    var velocity = Vector2.ZERO
    if position.x < get_global_mouse_position().x:
        velocity.x += 1
    else:
        velocity.x -= 1

    # Умножаем скорость на delta для фиксированной скорости
    velocity.x *= speed * delta

    # Перемещаем врага
    velocity = move_and_slide(velocity)

    # Обновляем анимацию
    update_animation(velocity)

func take_damage(amount):
    health -= amount
    if health <= 0:
        die()

func die():
    print("Enemy died!")
    animation_player.play("die")
    queue_free()

func update_animation(velocity):
    if velocity.x != 0:
        animation_player.play("run")
    else:
        animation_player.play("idle")
