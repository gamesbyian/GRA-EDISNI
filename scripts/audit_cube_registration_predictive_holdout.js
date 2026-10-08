#!/usr/bin/env node
'use strict';
// Experiment 462: prediction, not visual resemblance.
// Exhaustively withhold nine-sticker frames. Also Monte Carlo-withhold
// entire 27-sticker primary cubes. All labels of each target are erased
// BEFORE candidate completion, and all candidate strings retain Q4 data.
// Only Node built-ins required.
const fs=require('node:fs'),path=require('node:path');
const csv=fs.readFileSync(path.resolve(__dirname,'../data/observations.csv'),'utf8').trim().split(/\r?\n/);
const obs=Array(109).fill(0),map={'/':1,'-':2,'.':3},L='ABCDEFGHI',layout='ABCDEFGHI';
for(const row of csv.slice(1)){
  const [,res,mark]=row.split(','),r=+res;
  if(obs[r]&&obs[r]!==map[mark])throw Error('contradiction at '+r);
  obs[r]=map[mark];
}
if(obs.filter(Boolean).length!==66)throw Error('Recalibrate on new physical data');
const cols=[[8,2,5],[0,3,6],[1,4,7]];
function patterns(f,training){
  const known=Array.from({length:9},(_,j)=>training[1+9*f+j]),out=[];
  for(const minority of [1,2])for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){
    const row=Array(9).fill(minority===1?2:1);
    row[cols[0][a]]=row[cols[1][b]]=row[cols[2][c]]=minority;
    if(known.every((s,j)=>!s||s===row[j]))out.push(row);
  }
  return out;
}
function tails(){
  const choices=[],selected=Array(9).fill(0);
  function rec(j){
    if(j===9){
      const tail=Array(27).fill(3);
      for(let k=0;k<9;k++)tail[9*selected[k]+k]=1;
      if(tail.every((v,i)=>!obs[82+i]||obs[82+i]===v))choices.push(tail);
      return;
    }
    for(let d=0;d<3;d++){selected[j]=d;rec(j+1);}
  }
  rec(0);return choices;
}
const tailChoices=tails();
if(tailChoices.length!==18)throw Error('Q4 candidate count changed');
function pairs(mode,primaryOnly=false){
  const result=[],coords=[];
  for(let r=1;r<=108;r++){const slot=layout.indexOf(L[(r-1)%9]);coords[r]=[
    Math.floor((r-1)/27),Math.floor(((r-1)%27)/9),slot%3,Math.floor(slot/3)
  ];}
  for(let a=1;a<=108;a++)for(let b=a+1;b<=108;b++){
    const A=coords[a],B=coords[b];if(A[0]===B[0])continue;
    if(primaryOnly&&(A[0]===3||B[0]===3))continue;
    const dz=Math.abs(A[1]-B[1]),dx=Math.abs(A[2]-B[2]),dy=Math.abs(A[3]-B[3]);
    const ok=mode==='same'?(dz===0&&dx===0&&dy===0):
      (dz===0&&dx===1&&dy===0);
    if(ok){result.push(a-1,b-1);}
  }
  return Int16Array.from(result);
}
const es=pairs('same'),ex=pairs('x'),ps=pairs('same',true),px=pairs('x',true);
function count(seq,e){let n=0;for(let i=0;i<e.length;i+=2)n+=seq[e[i]]===seq[e[i+1]];return n;}
function scores(seq){return [
  count(seq,es)/(es.length/2)-count(seq,ex)/(ex.length/2),
  count(seq,ps)/(ps.length/2)-count(seq,px)/(px.length/2)
];}
const strengths=[0,10,25,50],modes=['all_cubes','primary_only'];
function weightedAggregates(targets,candidateEmitter,prior){
  const accum=Array.from({length:2},()=>strengths.map(()=>({
    total:0,slash:Array(targets.length).fill(0),weightedSum2:0
  })));
  let countMasters=0;
  candidateEmitter(seq=>{
    countMasters++;
    const sc=scores(seq);
    for(let m=0;m<2;m++)for(let b=0;b<strengths.length;b++){
      const w=Math.exp(strengths[b]*(sc[m]-.25)),a=accum[m][b];
      a.total+=w;a.weightedSum2+=w*w;
      for(let j=0;j<targets.length;j++)a.slash[j]+=w*(seq[targets[j]-1]===1);
    }
  });
  return modes.flatMap((name,m)=>strengths.map((beta,b)=>{
    const a=accum[m][b],p=a.slash.map(x=>x/a.total);
    let correct=0,brier=0,logloss=0,baseCorrect=0,baseBrier=0;
    for(let j=0;j<targets.length;j++){
      const y=obs[targets[j]]===1?1:0,prob=p[j];
      correct+=Number((prob>=.5)===Boolean(y));
      baseCorrect+=Number((prior>=.5)===Boolean(y));
      brier+=(prob-y)**2;baseBrier+=(prior-y)**2;
      logloss-=y*Math.log(Math.max(prob,1e-12))+(1-y)*Math.log(Math.max(1-prob,1e-12));
    }
    return {mode:name,beta,master_samples:countMasters,targets:targets.length,
      correct,baseline_correct:baseCorrect,brier:brier/targets.length,
      logloss:logloss/targets.length,baseline_brier:baseBrier/targets.length,
      effective_samples:a.total*a.total/a.weightedSum2,probabilities:p};
  }));
}
function trainingData(hold){
  const train=obs.slice();for(const r of hold)train[r]=0;return train;
}
function targetPrior(train){
  let n=0,slash=0;
  for(let r=1;r<=81;r++)if(train[r]){n++;slash+=train[r]===1;}
  return slash/n;
}
function exactCandidates(training,callback){
  const options=Array.from({length:9},(_,f)=>patterns(f,training)),chosen=Array(9);
  if(options.some(x=>x.length===0))throw Error('Impossible heldout primary frame');
  function recurse(f){
    if(f===9){const primary=chosen.flat();
      for(const tail of tailChoices)callback(primary.concat(tail));
      return;}
    for(const row of options[f]){chosen[f]=row;recurse(f+1);}
  }
  recurse(0);
}
function randomSource(seed){
  let state=seed>>>0;
  return()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state/4294967296;};
}
function sampleCandidates(training,samples,random,callback){
  const options=Array.from({length:9},(_,f)=>patterns(f,training));
  for(let t=0;t<samples;t++){
    const seq=Array(108);
    for(let f=0;f<9;f++){
      const available=options[f],row=available[Math.floor(random()*available.length)];
      for(let j=0;j<9;j++)seq[9*f+j]=row[j];
    }
    const tail=tailChoices[Math.floor(random()*tailChoices.length)];
    for(let j=0;j<27;j++)seq[81+j]=tail[j];
    callback(seq);
  }
}
const foldRecords=[];
for(let f=0;f<9;f++){
  const targets=Array.from({length:9},(_,j)=>9*f+j+1).filter(r=>obs[r]);
  const train=trainingData(targets);
  const predictions=weightedAggregates(targets,cb=>exactCandidates(train,cb),targetPrior(train));
  foldRecords.push({frame:f,targets:targets.length,results:predictions});
}
function aggregate(records){
  return modes.flatMap(mode=>strengths.map(beta=>{
    const rows=records.map(r=>r.results.find(x=>x.mode===mode&&x.beta===beta));
    const n=rows.reduce((a,r)=>a+r.targets,0);
    return {mode,beta,targets:n,
      correct:rows.reduce((a,r)=>a+r.correct,0),
      baseline_correct:rows.reduce((a,r)=>a+r.baseline_correct,0),
      brier:rows.reduce((a,r)=>a+r.brier*r.targets,0)/n,
      baseline_brier:rows.reduce((a,r)=>a+r.baseline_brier*r.targets,0)/n,
      logloss:rows.reduce((a,r)=>a+r.logloss*r.targets,0)/n};
  }));
}
const frameSummary=aggregate(foldRecords);
const samples=process.argv.includes('--fast')?10000:250000;
const cubeRuns=[];
for(const seed of [20261008,951733]){
  const rng=randomSource(seed),records=[];
  for(let q=0;q<3;q++){
    const targets=Array.from({length:27},(_,i)=>1+27*q+i).filter(r=>obs[r]);
    const train=trainingData(targets),prior=targetPrior(train);
    const pred=weightedAggregates(targets,cb=>sampleCandidates(train,samples,rng,cb),prior);
    records.push({cube:q+1,targets:targets.length,results:pred});
  }
  cubeRuns.push({seed,samples_per_cube:samples,cubes:records,summary:aggregate(records)});
}
for(const stat of [frameSummary,cubeRuns[0].summary]){
  const chosen=stat.find(x=>x.mode==='all_cubes'&&x.beta===25);
  if(chosen.targets!==54)throw Error('bad heldout census');
}
const frame25=frameSummary.find(x=>x.mode==='all_cubes'&&x.beta===25);
if(frame25.correct!==40||frame25.baseline_correct!==32)throw Error('Expected whole-frame holdout changed');
console.log(JSON.stringify({
  operation:'alphabetical same-spot rate minus alphabetical ±1 horizontal-X rate',
  physical_count:66,whole_nine_sticker_frame_holdout:frameSummary,
  full_cube_holdout_monte_carlo:cubeRuns,
  warning:'Post-selected layout/contrast and beta cannot be treated as blind external validation. Half-correct variants may overfit known physical placement. The Q4-ablated model uses only primary pair scores.'
},null,2));
