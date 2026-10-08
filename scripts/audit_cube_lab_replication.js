#!/usr/bin/env node
/**
 * Experiment 459: reproduce the community Cube Registration Lab's pair
 * definitions and exact cube x A-I null on both the original 65-residue
 * snapshot and the current 66-residue observation ledger.
 *
 * Uses Node built-ins only. No source HTML, embedded fonts, or
 * third-party redistribution. Call: node scripts/audit_cube_lab_replication.js
 */
const fs = require("node:fs");
const path = require("node:path");
const csv = fs.readFileSync(path.join(__dirname, "../data/observations.csv"), "utf8").trim().split(/\r?\n/);
const marks = { "/": "G", "-": "R", ".": "Y" };
const known = Array(109).fill("?");
for (let i = 1; i < csv.length; i++) {
  const [serial, r, mark] = csv[i].split(",");
  if (!Number.isInteger(+r) || !marks[mark]) throw Error("Invalid observation");
  if (known[+r] !== "?" && known[+r] !== marks[mark]) throw Error("Contradictory residue " + r);
  known[+r] = marks[mark];
}
const original = known.slice(); original[103] = "?";
const symbols = "GRY";
const layouts = ["IABCDEFGH", "ABCDEFGHI"];
const modes = ["exact", "x", "y", "z", "flat"];
function pairs(sequence, layout, mode) {
  const cells = [];
  for (let n = 1; n <= 108; n++) if (sequence[n] !== "?") cells.push(n);
  function coord(n) {
    const slot = layout.indexOf("ABCDEFGHI"[(n - 1) % 9]);
    return {cube: Math.floor((n - 1) / 27),
      depth: Math.floor(((n - 1) % 27) / 9),
      x: slot % 3, y: Math.floor(slot / 3), letter: (n - 1) % 9};
  }
  const output = [];
  for (let a = 0; a < cells.length; a++) for (let b = a + 1; b < cells.length; b++) {
    const i = cells[a], j = cells[b], x = coord(i), y = coord(j);
    if (x.cube === y.cube) continue;
    const dz = Math.abs(x.depth - y.depth),
      dx = Math.abs(x.x - y.x), dy = Math.abs(x.y - y.y);
    const yes = mode === "flat" ? x.letter === y.letter && dz !== 0 :
      mode === "exact" ? dz === 0 && dx === 0 && dy === 0 :
      mode === "x" ? dz === 0 && dx === 1 && dy === 0 :
      mode === "y" ? dz === 0 && dx === 0 && dy === 1 :
      dz === 1 && dx === 0 && dy === 0;
    if (yes) output.push([i,j]);
  }
  return output;
}
function score(state, edges) {
  let count = 0;
  for (const [a,b] of edges) if (state[a] === state[b]) count++;
  return count;
}
function options(values) {
  const out = [], seen = new Set();
  function walk(prefix, rest) {
    if (rest.length === 0) {
      const key = prefix.join("");
      if (!seen.has(key)) {seen.add(key);out.push(prefix);}
      return;
    }
    for (let i=0;i<rest.length;i++)
      walk([...prefix,rest[i]],[...rest.slice(0,i),...rest.slice(i+1)]);
  }
  walk([],values);
  return out;
}
function audit(input, name) {
  const observed = input.filter((mark, idx) => idx && mark !== "?").length;
  const sets = layouts.flatMap(layout => {
    const edges = Object.fromEntries(modes.map(m => [m,pairs(input,layout,m)]));
    const actual = Object.fromEntries(modes.map(m => [m,score(input,edges[m])]));
    return [{layout,edges,actual}];
  });
  const groups = [];
  for (let q=0;q<4;q++) for (let j=0;j<9;j++) {
    const sites=[0,1,2].map(d=>1+q*27+d*9+j).filter(r=>input[r]!=="?");
    const vals=sites.map(r=>input[r]);
    if (new Set(vals).size>1) groups.push({sites,choices:options(vals)});
  }
  const total=groups.reduce((a,b)=>a*b.choices.length,1);
  if (total !== 331776) throw Error("Observation census changed: "+total);
  const work=input.slice();
  const measures=sets.flatMap(s=>modes.slice(1).map(mode=>{
    const n0=s.edges.exact.length, n1=s.edges[mode].length;
    return {layout:s.layout,mode,n0,n1,
      observed:s.actual.exact/n0-s.actual[mode]/n1,
      sum:0,sumsq:0,tail:0,distribution:new Float64Array(total)};
  }));
  let iteration=0;
  function enumerate(k) {
    if (k===groups.length) {
      for(const m of measures){
        const s=sets.find(s=>s.layout===m.layout);
        const val=score(work,s.edges.exact)/m.n0-score(work,s.edges[m.mode])/m.n1;
        m.sum+=val;m.sumsq+=val*val;
        if(val+1e-12>=m.observed)m.tail++;
        m.distribution[iteration]=val;
      }
      iteration++;
      return;
    }
    for(const candidate of groups[k].choices){
      groups[k].sites.forEach((site,i)=>work[site]=candidate[i]);
      enumerate(k+1);
    }
  }
  enumerate(0);
  for(const m of measures){
    m.mean=m.sum/total;
    m.sd=Math.sqrt(m.sumsq/total-m.mean*m.mean);
    m.z=(m.observed-m.mean)/m.sd;
  }
  const observedMax=Math.max(...measures.filter(m=>m.mode!=="flat").map(m=>m.z));
  let familyExceed=0;
  for(let i=0;i<total;i++)
    if(measures.filter(m=>m.mode!=="flat").some(m=>(m.distribution[i]-m.mean)/m.sd+1e-12>=observedMax))
      familyExceed++;
  const result={
    snapshot:name, observed, total,
    pair_counts:sets.map(s=>({layout:s.layout,
      observations:Object.fromEntries(modes.map(m=>[m,{match:s.actual[m],pairs:s.edges[m].length}]))})),
    comparisons:measures.map(m=>({layout:m.layout,mode:m.mode,
      observed_delta:m.observed,null_mean_delta:m.mean,standardized_excess:m.z,
      exact_upper_tail:m.tail/total})),
    exploratory_max_Z_across_both_layouts_and_xyz:{
      observed:observedMax,upper_tail:familyExceed/total}
  };
  return result;
}
const older=audit(original,"lab65");
const current=audit(known,"repo66");
for(const snapshot of [older,current]){
  const physical=snapshot.pair_counts[0].observations;
  if(snapshot.snapshot==="lab65" && JSON.stringify(Object.values(physical).map(x=>[x.match,x.pairs])) !==
    JSON.stringify([[33,63],[21,68],[31,74],[28,81],[43,114]]))
    throw Error("Failed published physical-layout replication");
  if(snapshot.snapshot==="repo66" && JSON.stringify(Object.values(physical).map(x=>[x.match,x.pairs])) !==
    JSON.stringify([[33,64],[21,72],[31,77],[28,83],[43,118]]))
    throw Error("Failed updated corpus replication");
}
console.log(JSON.stringify({original:older,current},null,2));
