shader_type canvas_item;

void fragment() {
    vec4 tex_color = texture(TEXTURE, UV);
    // Если пиксель ярко-розовый (magenta), делаем его прозрачным
    if (tex_color.r > 0.8 && tex_color.g < 0.2 && tex_color.b > 0.8) {
        discard;
    }
    COLOR = tex_color;
}