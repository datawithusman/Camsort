from __future__ import annotations
import base64, json, os, random, time, uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
import requests
from sqlalchemy import create_engine, text

JsonObject = dict[str, Any]

def db_url():
    u=os.getenv("DATABASE_URL")
    if not u: raise RuntimeError("DATABASE_URL is required")
    return u.replace("postgresql://","postgresql+psycopg://",1) if u.startswith("postgresql://") else u
engine=create_engine(db_url(), pool_pre_ping=True)
def nid(p): return f"{p}-{uuid.uuid4()}"
def camel(s):
    a=s.split('_'); return a[0]+''.join(x[:1].upper()+x[1:] for x in a[1:])
def val(v):
    if isinstance(v, Decimal): return float(v)
    if isinstance(v, datetime): return v.isoformat().replace('+00:00','Z')
    return v
def rd(row): return None if row is None else {camel(k):val(v) for k,v in dict(row._mapping).items()}
def one(sql, p=None, commit=False):
    with engine.connect() as c:
        r=c.execute(text(sql), p or {}).first()
        if commit: c.commit()
        return rd(r)
def many(sql, p=None):
    with engine.connect() as c: return [rd(r) for r in c.execute(text(sql), p or {}).fetchall()]
def execsql(sql,p=None):
    with engine.connect() as c: c.execute(text(sql), p or {}); c.commit()
def rest(): return os.getenv('REST_API_BASE_URL','http://rest-api:8080').rstrip('/')
def cambase(): return os.getenv('CAMERA_SYSTEM_BASE_URL','http://camera-system-mocker-rest-api:8080').rstrip('/')
def jget(url):
    r=requests.get(url,timeout=60); r.raise_for_status(); return r.json() if r.content else {}
def bget(url):
    r=requests.get(url,timeout=60); r.raise_for_status(); return r.content, r.headers.get('content-type','image/jpeg')
def img_url(p):
    if p.startswith('http'): return p
    if p.startswith('/camera-system/'): p=p[len('/camera-system'):]
    return cambase()+p

def model(payload):
    if os.getenv('GEMINI_MODE','fake').lower()!='real': raise RuntimeError('fake')
    url=os.getenv('GEMINI_API_URL'); key=os.getenv('GEMINI_API_KEY')
    if not url or not key: raise RuntimeError('GEMINI_API_URL and GEMINI_API_KEY required')
    r=requests.post(url,headers={'Content-Type':'application/json','Authorization':f'Bearer {key}'},json=payload,timeout=float(os.getenv('GEMINI_API_TIMEOUT_SECONDS','90'))); r.raise_for_status()
    data=r.json(); return data.get('result', data) if isinstance(data,dict) else data

def first_pass(cam_id,prompt,b64,mime):
    if os.getenv('GEMINI_MODE','fake').lower()!='real':
        s=abs(hash((cam_id,prompt)))%101
        return {'camId':cam_id,'include':s>=30,'firstPassPromptScore':s,'operatorPriorityScore':min(100,max(0,s+random.randint(-12,12))),'operatorAction':'Review this camera.' if s>=30 else 'No immediate action.','reason':'Fake first-pass result.'}
    res=model({'requestType':'firstPassEvaluateCamera','camId':cam_id,'operatorPrompt':prompt,'cameraSnapshot':{'mimeType':mime,'base64':b64},'returnShape':{'camId':'string','include':'boolean','firstPassPromptScore':'number 0-100','operatorPriorityScore':'number 0-100','operatorAction':'string','reason':'string'}})
    return res if isinstance(res,dict) else {}

def second_pass(prompt, rows):
    if os.getenv('GEMINI_MODE','fake').lower()!='real':
        out=[]
        for rank,r in enumerate(sorted(rows,key=lambda x:(x.get('firstPassPromptScore') or 0,x.get('operatorPriorityScore') or 0),reverse=True),1):
            out.append({'camId':r['cameraId'],'firstPassResultId':r['id'],'include':r.get('include',True),'globalRank':rank,'promptScore':r.get('firstPassPromptScore') or 0,'operatorPriorityScore':r.get('operatorPriorityScore') or 0,'operatorAction':r.get('operatorAction') or 'Review this camera.','reason':r.get('reason') or 'Ranked by fake second pass.'})
        return out
    res=model({'requestType':'secondPassRankCameraResults','operatorPrompt':prompt,'firstPassResults':rows,'returnShape':[{'camId':'string','firstPassResultId':'string','include':'boolean','globalRank':'integer','promptScore':'number 0-100','operatorPriorityScore':'number 0-100','operatorAction':'string','reason':'string'}]})
    if isinstance(res,dict) and isinstance(res.get('results'),list): return res['results']
    return res if isinstance(res,list) else []

def settings(): return one('SELECT * FROM gemini_caller_settings WHERE id=true') or {}
def next_op():
    op=one("SELECT * FROM operations WHERE status='queued' AND trigger='manual' ORDER BY created_at ASC LIMIT 1")
    if op: return op
    op=one("SELECT * FROM operations WHERE status='queued' AND trigger='scheduled' ORDER BY created_at ASC LIMIT 1")
    if op: return op
    s=settings()
    if s.get('enabled') and s.get('continuousScanEnabled') and (not s.get('nextContinuousScanAt') or str(s.get('nextContinuousScanAt')) <= datetime.now(timezone.utc).isoformat().replace('+00:00','Z')):
        for b in many('SELECT * FROM prompt_bindings WHERE enabled=true ORDER BY created_at'):
            g=one('SELECT * FROM camera_groups WHERE id=:id',{'id':b['cameraGroupId']}) or {}; cams=g.get('cameraIds') or []
            one("INSERT INTO operations (id,prompt_id,camera_group_id,prompt_binding_id,trigger,status,total_cameras,estimated_gemini_calls) VALUES (:id,:pid,:gid,:bid,'scheduled','queued',:n,:calls) RETURNING *", {'id':nid('operation'),'pid':b['promptId'],'gid':b['cameraGroupId'],'bid':b['id'],'n':len(cams),'calls':len(cams)+1}, True)
        execsql("UPDATE gemini_caller_settings SET last_continuous_scan_at=now(), next_continuous_scan_at=now()+make_interval(secs=>continuous_scan_interval_seconds), updated_at=now() WHERE id=true")
        return one("SELECT * FROM operations WHERE status='queued' AND trigger='scheduled' ORDER BY created_at ASC LIMIT 1")
    return None

def process(op):
    opid=op['id']; pr=one('SELECT * FROM saved_prompts WHERE id=:id',{'id':op['promptId']}); gr=one('SELECT * FROM camera_groups WHERE id=:id',{'id':op['cameraGroupId']})
    if not pr or not gr: execsql("UPDATE operations SET status='failed', error_message='Missing prompt or group', completed_at=now() WHERE id=:id",{'id':opid}); return
    cams=gr.get('cameraIds') or []; execsql("UPDATE operations SET status='running', first_pass_status='running', started_at=COALESCE(started_at,now()), total_cameras=:n WHERE id=:id",{'id':opid,'n':len(cams)})
    delay=int(settings().get('geminiCallDelayMs') or 2000); rows=[]; calls=0
    for i,cam_id in enumerate(cams,1):
        try:
            snap=jget(f"{rest()}/camera-system/cameras/{cam_id}/snapshot"); fr=snap.get('frameRef') or {}; frame=snap.get('frame') or {}
            data,mime=bget(img_url(frame.get('url') or fr.get('frameUrl'))); res=first_pass(cam_id,pr['promptText'],base64.b64encode(data).decode(),mime); calls+=1
            row=one("INSERT INTO operation_first_pass_results (id,operation_id,camera_id,camera_group_id,prompt_id,frame_ref_id,frame_url,include,first_pass_prompt_score,operator_priority_score,operator_action,reason,raw_model_json) VALUES (:id,:op,:cam,:gid,:pid,:fr,:url,:inc,:score,:prio,:act,:reason,CAST(:raw AS jsonb)) RETURNING *", {'id':nid('first-pass'),'op':opid,'cam':cam_id,'gid':op['cameraGroupId'],'pid':op['promptId'],'fr':fr['id'],'url':fr.get('frameUrl') or frame.get('url'),'inc':res.get('include',True),'score':res.get('firstPassPromptScore',res.get('promptScore',0)),'prio':res.get('operatorPriorityScore',0),'act':res.get('operatorAction') or 'Review this camera.','reason':res.get('reason') or '', 'raw':json.dumps(res)}, True)
            rows.append(row)
            one("INSERT INTO latest_first_pass_results (prompt_id,camera_group_id,camera_id,operation_id,first_pass_result_id,frame_ref_id,frame_url,include,first_pass_prompt_score,operator_priority_score,operator_action,reason) VALUES (:pid,:gid,:cam,:op,:rid,:fr,:url,:inc,:score,:prio,:act,:reason) ON CONFLICT (prompt_id,camera_group_id,camera_id) DO UPDATE SET operation_id=EXCLUDED.operation_id, first_pass_result_id=EXCLUDED.first_pass_result_id, frame_ref_id=EXCLUDED.frame_ref_id, frame_url=EXCLUDED.frame_url, include=EXCLUDED.include, first_pass_prompt_score=EXCLUDED.first_pass_prompt_score, operator_priority_score=EXCLUDED.operator_priority_score, operator_action=EXCLUDED.operator_action, reason=EXCLUDED.reason, updated_at=now() RETURNING prompt_id", {'pid':op['promptId'],'gid':op['cameraGroupId'],'cam':cam_id,'op':opid,'rid':row['id'],'fr':row['frameRefId'],'url':row['frameUrl'],'inc':row['include'],'score':row['firstPassPromptScore'],'prio':row['operatorPriorityScore'],'act':row['operatorAction'],'reason':row['reason']}, True)
        except Exception as e: print('first pass error', cam_id, e, flush=True)
        execsql("UPDATE operations SET processed_cameras=:p, first_pass_result_count=:c, actual_gemini_calls=:calls WHERE id=:id", {'p':i,'c':len(rows),'calls':calls,'id':opid})
        if delay: time.sleep(delay/1000)
    if not rows:
        execsql("UPDATE operations SET status='failed', first_pass_status='failed', second_pass_status='skipped', error_message='No first-pass results were created. Check GeminiCaller logs for camera snapshot/image fetch errors.', actual_gemini_calls=:calls, completed_at=now() WHERE id=:id", {'id':opid, 'calls':calls})
        return
    execsql("UPDATE operations SET first_pass_status='completed', second_pass_status='running' WHERE id=:id", {'id':opid})
    ranked=second_pass(pr['promptText'], rows); calls+=1; count=0; matched=0
    for item in ranked:
        fp=next((r for r in rows if r['id']==item.get('firstPassResultId') or r['cameraId']==item.get('camId')),None)
        if not fp: continue
        inc=bool(item.get('include',True)); matched += 1 if inc else 0
        row=one("INSERT INTO operation_second_pass_results (id,operation_id,camera_id,camera_group_id,prompt_id,first_pass_result_id,frame_ref_id,frame_url,include,global_rank,prompt_score,operator_priority_score,operator_action,reason,raw_model_json) VALUES (:id,:op,:cam,:gid,:pid,:fpid,:fr,:url,:inc,:rank,:score,:prio,:act,:reason,CAST(:raw AS jsonb)) RETURNING *", {'id':nid('second-pass'),'op':opid,'cam':fp['cameraId'],'gid':op['cameraGroupId'],'pid':op['promptId'],'fpid':fp['id'],'fr':fp['frameRefId'],'url':fp['frameUrl'],'inc':inc,'rank':item.get('globalRank'),'score':item.get('promptScore',fp['firstPassPromptScore']),'prio':item.get('operatorPriorityScore',fp['operatorPriorityScore']),'act':item.get('operatorAction',fp['operatorAction']),'reason':item.get('reason',fp['reason']),'raw':json.dumps(item)}, True); count+=1
        one("INSERT INTO latest_second_pass_results (prompt_id,camera_group_id,camera_id,operation_id,second_pass_result_id,first_pass_result_id,frame_ref_id,frame_url,include,global_rank,prompt_score,operator_priority_score,operator_action,reason) VALUES (:pid,:gid,:cam,:op,:rid,:fpid,:fr,:url,:inc,:rank,:score,:prio,:act,:reason) ON CONFLICT (prompt_id,camera_group_id,camera_id) DO UPDATE SET operation_id=EXCLUDED.operation_id, second_pass_result_id=EXCLUDED.second_pass_result_id, first_pass_result_id=EXCLUDED.first_pass_result_id, frame_ref_id=EXCLUDED.frame_ref_id, frame_url=EXCLUDED.frame_url, include=EXCLUDED.include, global_rank=EXCLUDED.global_rank, prompt_score=EXCLUDED.prompt_score, operator_priority_score=EXCLUDED.operator_priority_score, operator_action=EXCLUDED.operator_action, reason=EXCLUDED.reason, updated_at=now() RETURNING prompt_id", {'pid':op['promptId'],'gid':op['cameraGroupId'],'cam':row['cameraId'],'op':opid,'rid':row['id'],'fpid':row['firstPassResultId'],'fr':row['frameRefId'],'url':row['frameUrl'],'inc':row['include'],'rank':row['globalRank'],'score':row['promptScore'],'prio':row['operatorPriorityScore'],'act':row['operatorAction'],'reason':row['reason']}, True)
        if inc: one("INSERT INTO operator_queue_items (id,second_pass_result_id,operation_id,camera_id,camera_group_id,prompt_id,frame_ref_id,frame_url,prompt_score,operator_priority_score,operator_action,reason,status) VALUES (:id,:rid,:op,:cam,:gid,:pid,:fr,:url,:score,:prio,:act,:reason,'queued') ON CONFLICT (second_pass_result_id) DO UPDATE SET prompt_score=EXCLUDED.prompt_score, operator_priority_score=EXCLUDED.operator_priority_score, operator_action=EXCLUDED.operator_action, reason=EXCLUDED.reason, updated_at=now() RETURNING id", {'id':nid('queue'),'rid':row['id'],'op':opid,'cam':row['cameraId'],'gid':row['cameraGroupId'],'pid':row['promptId'],'fr':row['frameRefId'],'url':row['frameUrl'],'score':row['promptScore'],'prio':row['operatorPriorityScore'],'act':row['operatorAction'],'reason':row['reason']}, True)
    execsql("UPDATE operations SET status='completed', second_pass_status='completed', second_pass_result_count=:c, matched_cameras=:m, actual_gemini_calls=:calls, completed_at=now() WHERE id=:id", {'c':count,'m':matched,'calls':calls,'id':opid})
    if op.get('promptBindingId'): execsql("UPDATE prompt_bindings SET last_run_at=now(), updated_at=now() WHERE id=:id", {'id':op['promptBindingId']})

def main():
    print('GeminiCaller two-pass worker starting', flush=True); poll=float(os.getenv('WORKER_POLL_INTERVAL_SECONDS','5'))
    while True:
        try:
            op=next_op(); process(op) if op else time.sleep(poll)
        except Exception as e:
            print('worker error', e, flush=True); time.sleep(poll)
if __name__=='__main__': main()
