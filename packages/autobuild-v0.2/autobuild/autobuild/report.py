def target_markdown(target):
    lines=[f"# Target: {target['id']}","",f"**Objective:** {target['objective']}","",f"**Strategic scarcity:** {target.get('strategic_parent',{}).get('durable_scarcity')}","","## Minimum moat path",""]
    for row in target.get("metadata",{}).get("underengineer",{}).get("scored",[]):
        mark="BUILD" if row["selected"] else "DEFER"; lines.append(f"- **{mark}** `{row['id']}` — score {row['score']}; {', '.join(row['reasons'])}")
    lines += ["","## Requirements",""]
    for r in target.get("requirements",[]):lines.append(f"- `{r['id']}` [{r['criticality']}] {r['statement']}")
    reuse=target.get("reuse",{}); lines += ["","## Reuse","",f"- status: {reuse.get('status')}",f"- existing capability coverage: {reuse.get('coverage')}",f"- missing: {len(reuse.get('missing_requirement_ids',[]))}"]
    return "\n".join(lines)
