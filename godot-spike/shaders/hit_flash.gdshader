shader_type canvas_item;
uniform float flash : hint_range(0.0, 1.0) = 0.0;
uniform float flash_mix : hint_range(0.0, 1.0) = 0.65;
uniform vec4 flash_color : source_color = vec4(1.0);
void fragment() {
	// Fragment COLOR already includes the texture and vertex modulation.
	vec4 source = COLOR;
	COLOR = vec4(mix(source.rgb, flash_color.rgb, flash * flash_mix), source.a);
}
