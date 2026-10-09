import unreal,json,math
from pathlib import Path
base='/Game/Characters/Mannequins/Animations/Manny/'
src=unreal.load_asset(base+'MM_Run_Fwd')
dst=unreal.load_asset(base+'MM_Run_Sprint')
ext=unreal.AnimPoseExtensions
W,L=unreal.AnimPoseSpaces.WORLD,unreal.AnimPoseSpaces.LOCAL
def p(pose,b): return ext.get_bone_pose(pose,b,W).translation.to_tuple()
def dist(a,b): return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
report={}
for kind in [unreal.AnimDataEvalType.RAW,unreal.AnimDataEvalType.COMPRESSED]:
    opt=unreal.AnimPoseEvaluationOptions(evaluation_type=kind)
    maxfoot,maxroot,maxdrop=0,0,0
    samples=[]
    for i in range(115):
        t=src.sequence_length*i/114
        a=ext.get_anim_pose_at_time(src,t,opt)
        b=ext.get_anim_pose_at_time(dst,t,opt)
        maxfoot=max(maxfoot,*[dist(p(a,f),p(b,f)) for f in ['foot_l','foot_r','ball_l','ball_r']])
        maxroot=max(maxroot,dist(p(a,'root'),p(b,'root')))
        maxdrop=max(maxdrop,abs(p(a,'pelvis')[2]-p(b,'pelvis')[2]-8))
        if i in [0,28,57,85,114]: samples.append({'t':t,'original_head':p(a,'head'),'sprint_head':p(b,'head')})
    assert maxdrop<0.1,(kind,maxdrop)
    assert maxfoot<0.5,(kind,maxfoot)
    assert maxroot<0.01,(kind,maxroot)
    report[str(kind)]={'max_foot_error_cm':maxfoot,'max_root_error_cm':maxroot,'max_pelvis_drop_error_cm':maxdrop,'samples':samples}
assert abs(dst.get_editor_property('rate_scale')-1.25)<0.001
registry=unreal.AssetRegistryHelpers.get_asset_registry()
registry.scan_paths_synchronous(['/Game'],True)
report['sprint_referencers']=[str(x) for x in registry.get_referencers(base+'MM_Run_Sprint',unreal.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True))]
dash=unreal.load_asset(base+'AM_Dash')
report['dash_blend_out_seconds']=dash.get_editor_property('blend_out').get_editor_property('blend_time')
Path(unreal.Paths.project_dir(),'Saved','sprint_verify.json').write_text(json.dumps(report,indent=2))
unreal.log('SPRINT_VERIFY_COMPLETE '+json.dumps(report))
