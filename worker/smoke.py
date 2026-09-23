import json, math, hashlib, pathlib

# Deterministic baseline: standard atmosphere + point-mass aerodynamic sanity case.
rho=1.225; v=50.0; S=16.2; CL=0.50; CD=0.035; mass=1100.0; g=9.80665
q=0.5*rho*v*v
lift=q*S*CL
drag=q*S*CD
weight=mass*g
ld=lift/drag
checks={"finite":all(math.isfinite(x) for x in [q,lift,drag,weight,ld]),"positive":min(q,lift,drag,weight,ld)>0,"ld_consistent":abs(ld-CL/CD)<1e-12}
result={"status":"PASS" if all(checks.values()) else "FAIL","model":"deterministic-aero-smoke-v1","inputs":{"rho_kg_m3":rho,"v_m_s":v,"S_m2":S,"CL":CL,"CD":CD,"mass_kg":mass},"outputs":{"q_pa":q,"lift_N":lift,"drag_N":drag,"weight_N":weight,"L_over_D":ld},"checks":checks,"epistemic":"SMOKE_TEST_ONLY_NOT_CALIBRATED_NOT_PHYSICAL_VALIDATION"}
pathlib.Path("artifacts").mkdir(exist_ok=True)
raw=json.dumps(result,sort_keys=True,indent=2).encode(); result["payload_sha256"]=hashlib.sha256(raw).hexdigest()
pathlib.Path("artifacts/smoke-result.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(0 if result["status"]=="PASS" else 1)
