#!/usr/bin/env node
'use strict';
// Experiments 470–471: exact full-completion registration controls and
// mask/census-preserving structural null. No third-party HTML/fonts copied.
const fs=require('node:fs'),path=require('node:path');
const csv=fs.readFileSync(path.resolve(__dirname,'../data/observations.csv'),'utf8').trim().split(/\r?\n/);
const marks=Array(109).fill(0),V={'/':1,'-':2,'.':3},LET='ABCDEFGHI',cols=[[8,2,5],[0,3,6],[1,4,7]];
for(const line of csv.slice(1)){
  let [serial,res,sym]=line.split(',');res=+res;
  if(marks[res]&&marks[res]!==V[sym])throw Error('Conflicting residue '+res);
  marks[res]=V[sym];
}
if(marks.filter(Boolean).length!==66)throw Error('Corpus changed; recalibrate expected counts');
const seed=20261008;
function randGen(x){return()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x/4294967296;};}
const layouts=['IABCDEFGH','ABCDEFGHI'];
function frameChoices(f,condition){
  const out=[],start=1+9*f,known=Array.from({length:9},(_,j)=>marks[start+j]);
  const k=known.filter(x=>x===1).length;
  for(let minority of [1,2])for(let a=0;a<9;a++)for(let b=a+1;b<9;b++)for(let c=b+1;c<9;c++){
    const s=Array(9).fill(minority===1?2:1);s[a]=s[b]=s[c]=minority;
    if(condition.startsWith('exact')&&known.some((v,j)=>v&&v!==s[j]))continue;
    if(condition.startsWith('census')&&known.filter((v,j)=>v&&s[j]===1).length!==k)continue;
    if(condition.endsWith('column')&&!cols.every(col=>{
      const ns=col.filter(j=>s[j]===1).length;return ns===1||ns===2;
    }))continue;
    out.push(s);
  }
  return out;
}
function tails(condition){
  const result=[],selector=Array(9).fill(0),q4slash=marks.slice(82).filter(x=>x===1).length;
  function rec(j){
    if(j===9){
      const tail=Array(27).fill(3);
      for(let c=0;c<9;c++)tail[9*selector[c]+c]=1;
      if(condition==='exact'&&tail.some((v,i)=>marks[82+i]&&marks[82+i]!==v))return;
      if(condition==='census'&&tail.filter((v,i)=>marks[82+i]&&v===1).length!==q4slash)return;
      result.push(tail);return;
    }
    for(let d=0;d<3;d++){selector[j]=d;rec(j+1);}
  }
  rec(0);return result;
}
function edges(layout,mode,masked=false){
  const out=[],coords=[];
  for(let n=1;n<=108;n++){
    const s=layout.indexOf(LET[(n-1)%9]);
    coords[n]=[Math.floor((n-1)/27),Math.floor(((n-1)%27)/9),s%3,Math.floor(s/3),(n-1)%9];
  }
  for(let a=1;a<=108;a++)for(let b=a+1;b<=108;b++){
    if(masked&&(!marks[a]||!marks[b]))continue;
    const A=coords[a],B=coords[b];if(A[0]===B[0])continue;
    const dz=Math.abs(A[1]-B[1]),dx=Math.abs(A[2]-B[2]),dy=Math.abs(A[3]-B[3]);
    const yes=mode==='same'?dz===0&&dx===0&&dy===0:
      mode==='x'?dz===0&&dx===1&&dy===0:
      mode==='y'?dz===0&&dx===0&&dy===1:
      mode==='z'?dz===1&&dx===0&&dy===0:A[4]===B[4]&&dz!==0;
    if(yes)out.push([a-1,b-1]);
  }
  return out;
}
function flatten(pairs){const out=new Int16Array(pairs.length*2);let i=0;for(const [a,b] of pairs){out[i++]=a;out[i++]=b;}return out;}
function tally(seq,e){let count=0;for(let i=0;i<e.length;i+=2)count+=seq[e[i]]===seq[e[i+1]];return count;}
function cross(body,tail,e){let count=0;for(let i=0;i<e.length;i+=2)count+=body[e[i]]===tail[e[i+1]];return count;}
function completionAudit(){
  const out={},last=tails('exact'),keys=layouts.flatMap(lay=>['x','y','z','flat'].map(mode=>lay+'/'+mode));
  const edgeSet={};
  for(const key of new Set(['IABCDEFGH/same',...keys])){
    const [layout,mode]=key.split('/'),e=edges(layout,mode);
    const body=[],tail=[];
    for(const [a,b] of e){if(b<81)body.push(a,b);else tail.push(a,b-81);}
    edgeSet[key]={n:e.length,body:Int16Array.from(body),tail:Int16Array.from(tail)};
  }
  for(const strict of [false,true]){
    const frames=Array.from({length:9},(_,f)=>frameChoices(f,strict?'exact_column':'exact'));
    const stats={count:0,preferred:{},mean:{}},selected=Array(9);
    for(const key of keys){stats.preferred[key]=0;stats.mean[key]=0;}
    function recurse(f){
      if(f===9){
        const body=selected.flat(),pre={};
        for(const [key,e] of Object.entries(edgeSet))pre[key]=tally(body,e.body);
        for(const tail of last){
          stats.count++;
          const s=edgeSet['IABCDEFGH/same'];
          const same=(pre['IABCDEFGH/same']+cross(body,tail,s.tail))/s.n;
          for(const key of keys){
            const e=edgeSet[key],d=same-(pre[key]+cross(body,tail,e.tail))/e.n;
            stats.mean[key]+=d;stats.preferred[key]+=(d>1e-12);
          }
        }
        return;
      }
      for(const frow of frames[f]){selected[f]=frow;recurse(f+1);}
    }
    recurse(0);
    for(const key of keys)stats.mean[key]/=stats.count;
    out[strict?'strict_column':'broad_3of9']=stats;
  }
  return out;
}
function structuralNull(N){
  const results={},keys=layouts.flatMap(l=>['x','y','z'].map(m=>l+'/'+m));
  const all=layouts.flatMap(l=>['same','x','y','z','flat'].map(m=>l+'/'+m));
  const pairs=Object.fromEntries(all.map(key=>{
    const [layout,mode]=key.split('/');return [key,flatten(edges(layout,mode,true))];
  }));
  const actualSymbols=Array.from({length:108},(_,i)=>marks[i+1]);
  const actual=Object.fromEntries(all.map(k=>[k,tally(actualSymbols,pairs[k])/(pairs[k].length/2)]));
  for(const strict of [false,true]){
    const random=randGen(seed+(strict?1927:0));
    const opts=Array.from({length:9},(_,f)=>frameChoices(f,strict?'census_column':'census'));
    const q4=tails('census'),seq=new Array(108);
    const distributions=Object.fromEntries(keys.map(k=>[k,new Float64Array(N)]));
    const sums=Object.fromEntries(all.map(k=>[k,0]));
    for(let i=0;i<N;i++){
      for(let f=0;f<9;f++){const row=opts[f][Math.floor(random()*opts[f].length)];for(let j=0;j<9;j++)seq[9*f+j]=row[j];}
      const tail=q4[Math.floor(random()*q4.length)];for(let j=0;j<27;j++)seq[81+j]=tail[j];
      const rates={};
      for(const k of all){rates[k]=tally(seq,pairs[k])/(pairs[k].length/2);sums[k]+=rates[k];}
      for(const k of keys){const l=k.split('/')[0];distributions[k][i]=rates[l+'/same']-rates[k];}
    }
    const stats={};
    for(const k of keys){
      const l=k.split('/')[0],observed=actual[l+'/same']-actual[k];
      let total=0,varSum=0,high=0;
      for(const v of distributions[k])total+=v;
      const mean=total/N;
      for(const v of distributions[k]){varSum+=(v-mean)**2;high+=(v>=observed-1e-12);}
      const sd=Math.sqrt(varSum/N);
      stats[k]={observed_contrast:observed,mean_null_contrast:mean,
        upper_tail:high/N,z:(observed-mean)/sd,sd};
    }
    const observedMax=Math.max(...keys.map(k=>stats[k].z));let familyHigh=0;
    for(let i=0;i<N;i++){
      let best=-Infinity;
      for(const k of keys)best=Math.max(best,(distributions[k][i]-stats[k].mean_null_contrast)/stats[k].sd);
      familyHigh+=(best>=observedMax-1e-12);
    }
    results[strict?'one_minority_per_column':'three_of_nine']={
      samples:N,frame_options:opts.map(x=>x.length),q4_choices:q4.length,actual,
      null_means:Object.fromEntries(all.map(k=>[k,sums[k]/N])),
      contrasts:stats,six_comparison_max_Z:{observed:observedMax,upper_tail:familyHigh/N}
    };
  }
  return results;
}
const N=process.argv.includes('--fast')?5000:250000;
const completions=completionAudit(),nulls=structuralNull(N);
if(completions.broad_3of9.count!==233280||completions.strict_column.count!==324)throw Error('wrong family');
if(completions.broad_3of9.preferred['ABCDEFGHI/x']!==233136)throw Error('wrong broad alphabetical X');
if(completions.strict_column.preferred['ABCDEFGHI/x']!==324)throw Error('wrong strict alphabetical X');
if(nulls.one_minority_per_column.q4_choices!==6120)throw Error('wrong null Q4 choices');
console.log(JSON.stringify({completion_families:completions,structural_null:nulls},null,2));
