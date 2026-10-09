"""UE 5.4 commandlet: sculpt the existing sprint with foot-preserving two-bone IK.

Always sample MM_Run_Fwd, so rerunning never accumulates the pose edits.
"""
import unreal, math, json, shutil
from pathlib import Path

BASE = '/Game/Characters/Mannequins/Animations/Manny/'
PROJECT = Path(unreal.Paths.project_dir())
EXT = unreal.AnimPoseExtensions
WORLD, LOCAL = unreal.AnimPoseSpaces.WORLD, unreal.AnimPoseSpaces.LOCAL

def add(a,b): return tuple(x+y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def mul(a,s): return tuple(x*s for x in a)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(dot(a,a))
def unit(a): return mul(a, 1.0/max(norm(a), 1e-10))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def qmul(a,b):
    v=add(add(mul(b[:3],a[3]),mul(a[:3],b[3])),cross(a[:3],b[:3]))
    return (*v, a[3]*b[3]-dot(a[:3],b[:3]))
def between(a,b):
    a,b=unit(a),unit(b)
    q=(*cross(a,b),1+dot(a,b))
    assert norm(q)>1e-6, 'Unexpected opposite IK vectors'
    return unit(q)
def pitch(deg):
    r=math.radians(deg)/2
    return (math.sin(r),0,0,math.cos(r))
def axis_angle(axis,deg):
    r=math.radians(deg)/2
    return (*mul(unit(axis),math.sin(r)),math.cos(r))
def get(p,b,space=WORLD): return EXT.get_bone_pose(p,b,space)
def pos(p,b): return get(p,b).translation.to_tuple()
def rotate(p,b,q):
    tr=get(p,b)
    tr.rotation=unreal.Quat(*qmul(q,tr.rotation.to_tuple()))
    return EXT.set_bone_pose(p,tr,b,WORLD)

src=unreal.load_asset(BASE+'MM_Run_Fwd')
dst=unreal.load_asset(BASE+'MM_Run_Sprint')
assert src and dst and src.get_editor_property('skeleton') == dst.get_editor_property('skeleton')
backup=PROJECT/'Saved'/'SprintBackup'/'MM_Run_Sprint.uasset'
backup.parent.mkdir(parents=True,exist_ok=True)
if not backup.exists():
    shutil.copy2(PROJECT/'Content/Characters/Mannequins/Animations/Manny/MM_Run_Sprint.uasset',backup)
previous=backup.with_name('MM_Run_Sprint_pose_v1.uasset')
if not previous.exists():
    shutil.copy2(PROJECT/'Content/Characters/Mannequins/Animations/Manny/MM_Run_Sprint.uasset',previous)

model=src.data_model_interface
n=model.get_number_of_keys()
frames=n-1
changed=['pelvis','spine_01','neck_01','thigh_l','calf_l','foot_l','thigh_r','calf_r','foot_r',
         'upperarm_l','lowerarm_l','upperarm_r','lowerarm_r']
keys={b:[] for b in changed}
report={'frames':frames,'rate_scale':1.25,'pelvis_drop_cm':8.0,'pelvis_forward_cm':2.0,
        'pelvis_forward_lean_deg':28.0,'spine_counter_rotation_deg':4.0,'head_counter_rotation_deg':8.0,
        'upperarm_swing_multiplier':1.45,'elbow_flexion_range_deg':[65,110],
        'max_foot_position_error_cm':0.0,'max_bone_length_error_cm':0.0,'samples':[]}
draw_bones=['root','pelvis','spine_01','spine_02','spine_03','spine_04','spine_05','neck_01','head',
            'clavicle_l','upperarm_l','lowerarm_l','hand_l','clavicle_r','upperarm_r','lowerarm_r','hand_r',
            'thigh_l','calf_l','foot_l','ball_l','thigh_r','calf_r','foot_r','ball_r']
options=unreal.AnimPoseEvaluationOptions()
arm_angles={s:[] for s in ['l','r']}
for i in range(frames):
    p=EXT.get_anim_pose_at_time(src,src.sequence_length*i/frames,options)
    for s in arm_angles:
        v=sub(pos(p,'lowerarm_'+s),pos(p,'upperarm_'+s))
        arm_angles[s].append(math.degrees(math.atan2(v[1],-v[2])))
arm_mean={s:sum(a)/len(a) for s,a in arm_angles.items()}
for i in range(n):
    t=src.sequence_length*i/frames
    pose=EXT.get_anim_pose_at_time(src,t,options)
    original={b:pos(pose,b) for b in draw_bones}
    legs={s:{b:get(pose,b+'_'+s) for b in ['thigh','calf','foot']} for s in ['l','r']}
    pelvis=get(pose,'pelvis')
    pelvis.translation=unreal.Vector(*add(pelvis.translation.to_tuple(),(0,2,-8)))
    pose=EXT.set_bone_pose(pose,pelvis,'pelvis',WORLD)
    pose=rotate(pose,'pelvis',pitch(-28))
    pose=rotate(pose,'spine_01',pitch(4))
    pose=rotate(pose,'neck_01',pitch(8))
    assert abs(pos(pose,'pelvis')[2]-original['pelvis'][2]+8)<0.001
    for s in ['l','r']:
        upper,lower,hand=['%s_%s'%(b,s) for b in ['upperarm','lowerarm','hand']]
        # Add phase-preserving shoulder swing, rather than a constant arm offset.
        extra=0.45*(arm_angles[s][i%frames]-arm_mean[s])
        pose=rotate(pose,upper,pitch(extra))
        humerus=unit(sub(pos(pose,lower),pos(pose,upper)))
        forearm=unit(sub(pos(pose,hand),pos(pose,lower)))
        flex=math.degrees(math.acos(max(-1,min(1,dot(humerus,forearm)))))
        target=max(65,min(110,flex+15))
        pose=rotate(pose,lower,axis_angle(cross(humerus,forearm),target-flex))
    for s in ['l','r']:
        thigh,calf,foot=['%s_%s'%(b,s) for b in ['thigh','calf','foot']]
        old=legs[s]
        hip0,knee0,ankle0=[old[b].translation.to_tuple() for b in ['thigh','calf','foot']]
        hip=pos(pose,thigh)
        l1,l2=norm(sub(knee0,hip0)),norm(sub(ankle0,knee0))
        delta=sub(ankle0,hip)
        distance=norm(delta)
        assert abs(l1-l2)+0.001 < distance < l1+l2-0.001, 'Unreachable preserved foot target'
        axis=unit(delta)
        # Preserve the original knee bend plane while solving the lowered hip.
        bend=unit(sub(sub(knee0,hip0),mul(axis,dot(sub(knee0,hip0),axis))))
        along=(l1*l1-l2*l2+distance*distance)/(2*distance)
        height=math.sqrt(max(0,l1*l1-along*along))
        knee=add(add(hip,mul(axis,along)),mul(bend,height))
        pose=rotate(pose,thigh,between(sub(pos(pose,calf),hip),sub(knee,hip)))
        pose=rotate(pose,calf,between(sub(pos(pose,foot),pos(pose,calf)),sub(ankle0,pos(pose,calf))))
        tr=get(pose,foot)
        tr.rotation=old['foot'].rotation
        pose=EXT.set_bone_pose(pose,tr,foot,WORLD)
        report['max_foot_position_error_cm']=max(report['max_foot_position_error_cm'],norm(sub(pos(pose,foot),ankle0)))
        for a,b,length in [(thigh,calf,l1),(calf,foot,l2)]:
            report['max_bone_length_error_cm']=max(report['max_bone_length_error_cm'],abs(norm(sub(pos(pose,a),pos(pose,b)))-length))
    for b in changed: keys[b].append(get(pose,b,LOCAL))
    report['samples'].append({'time':t,'before':original,'after':{b:pos(pose,b) for b in draw_bones}})

assert report['max_foot_position_error_cm'] < 0.01, report
assert report['max_bone_length_error_cm'] < 0.01, report
# Close the pose loop exactly on modified local tracks; retain the original root motion.
for b in changed: keys[b][-1]=keys[b][0]
controller=dst.controller
if controller is None:
    controller=unreal.AnimSequencerController()
    controller.set_model(dst.data_model_interface)
controller.open_bracket('Author low dash-follow sprint',False)
try:
    for b,track in keys.items():
        assert controller.set_bone_track_keys(b,[k.translation for k in track],[k.rotation for k in track],[k.scale3d for k in track],False), b
finally:
    controller.close_bracket(False)
dst.set_editor_property('rate_scale',1.25)
assert unreal.EditorAssetLibrary.save_loaded_asset(dst,False)
bs=unreal.load_asset(BASE+'BS_MM_WalkRun')
report['blendspace_samples']=[{'animation':str(s.get_editor_property('animation').get_path_name()),
                            'value':str(s.get_editor_property('sample_value'))} for s in bs.get_editor_property('sample_data')]
Path(PROJECT/'Saved'/'sprint_build_report.json').write_text(json.dumps(report,indent=2))
unreal.log('SPRINT_BUILD_COMPLETE '+json.dumps({k:v for k,v in report.items() if k!='samples'}))
