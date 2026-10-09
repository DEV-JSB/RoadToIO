import unreal, json
from pathlib import Path

out = {}
base = '/Game/Characters/Mannequins/Animations/Manny/'
for name in ['MM_Run_Fwd', 'MM_Run_Sprint', 'AS_Dash', 'AM_Dash', 'BS_MM_WalkRun']:
    a = unreal.load_asset(base + name)
    d = {'class': a.get_class().get_name()}
    for prop in ['rate_scale', 'sequence_length', 'skeleton', 'sample_data', 'blend_out', 'blend_in']:
        try: d[prop] = str(a.get_editor_property(prop))
        except Exception: pass
    if isinstance(a, unreal.AnimSequence):
        d['methods'] = [x for x in dir(a) if 'data' in x or 'controller' in x]
        d['poses'] = {}
        for t in [0.0, a.sequence_length * 0.25, a.sequence_length * 0.5, a.sequence_length * 0.75, a.sequence_length]:
            pose = unreal.AnimPoseExtensions.get_anim_pose_at_time(a, t, unreal.AnimPoseEvaluationOptions())
            d['poses'][str(t)] = {}
            for bone in ['root','pelvis','spine_01','spine_02','spine_03','spine_04','spine_05','neck_01','head','thigh_l','calf_l','foot_l','thigh_r','calf_r','foot_r','upperarm_l','upperarm_r']:
                tr = unreal.AnimPoseExtensions.get_bone_pose(pose, bone, unreal.AnimPoseSpaces.WORLD)
                d['poses'][str(t)][bone] = {'p': tr.translation.to_tuple(), 'q': tr.rotation.to_tuple()}
    out[name] = d
Path(unreal.Paths.project_dir(), 'Saved', 'sprint_inspect.json').write_text(json.dumps(out, indent=2))
unreal.log('SPRINT_INSPECT_COMPLETE')
