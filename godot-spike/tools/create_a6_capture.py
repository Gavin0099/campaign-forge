"""Reuse the proven A5 observer; no gameplay/manifest change."""
from prepare_a6_frames import *
src=(REPO/'godot-spike/tools/capture_a5.gd').read_text(encoding='utf-8-sig')
src=src.replace('A5','A6').replace('a5','a6').replace('baseline-a4','baseline-a5')
src=src.replace('var scene\n','var scene\nvar render_trace: Array = []\n')
src=src.replace('scene.hitstop_started.connect(on_hold)','scene.hitstop_started.connect(on_hold)\n\tRenderingServer.frame_post_draw.connect(record_render_frame)')
src=src.replace('func finish() -> void:', '''func record_render_frame() -> void:
	if not movie or complete or not is_instance_valid(scene): return
	var player = scene.players.thoma
	render_trace.append({"process_frame":Engine.get_process_frames(),"phase":scene.phase,
		"index":player.frame_index,"path":player.sequence.frames[player.frame_index].path,
		"hold":scene.hold_active,"body_transform":[player.body.get_global_transform_with_canvas().x.x,
		player.body.get_global_transform_with_canvas().y.y,player.body.get_global_transform_with_canvas().origin.x,
		player.body.get_global_transform_with_canvas().origin.y]})

func finish() -> void:''')
src=src.replace('file.close()\n\tcomplete = true','''file.close()
	if movie:
		var trace_file := FileAccess.open(PREFIX+"render-trace.json",FileAccess.WRITE)
		trace_file.store_string(JSON.stringify(render_trace,"\\t"))
		trace_file.close()
	complete = true''')
(REPO/'godot-spike/tools/capture_a6.gd').write_text(src,encoding='utf-8',newline='\n')
print('A6_CAPTURE observer generated from A5; added post-draw pose trace only')
