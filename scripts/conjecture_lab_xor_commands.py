#!/usr/bin/env python3
"""CL-VLEN-09: nine class states updated by three shared XOR-mask commands.

State j+1 = State j XOR 9-bit Mask[tail_select_j], cyclic A..I..A.
Eliminate all unknown body bits and command masks exactly over GF(2).
Physical observations are never imputed. Exploratory only.
"""
import argparse,csv,itertools,json,math,random,statistics
from pathlib import Path

def read(path):
 s=['?']*108;seen={};n=0
 if path.suffix=='.csv':
  with path.open(newline='') as f:
   for r in csv.DictReader(f):
    i=int(r['residue'])-1;c=r['symbol'];n+=1
    assert i not in seen or seen[i]==c
    seen[i]=c;s[i]=c
 else:
  for tok in path.read_text().split():
   i=int(tok[:-1])-1;c=tok[-1];n+=1
   assert i not in seen or seen[i]==c
   seen[i]=c;s[i]=c
 assert (n,len(seen))==(84,66)
 return s

def options(s):
 opts=[]
 for j in range(9):
  tail=[s[81+j+9*k] for k in range(3)]
  opts.append([k for k in range(3) if tail[k] in ('/','?') and all(c in ('.','?') for n,c in enumerate(tail) if n!=k)])
 return opts

def rank(rows):
 """Augmented binary 12-variable Gaussian elimination: return rank, inconsistent."""
 basis=[0]*12;rr=0
 for v in rows:
  a=v
  while a:
   leading=(a & ((1<<12)-1)).bit_length()-1
   if leading<0:return rr,True
   if basis[leading]:a^=basis[leading]
   else:
    basis[leading]=a;rr+=1;break
 return rr,False

def equations(commands,rail,s):
 eqs=[]
 for j,k in enumerate(commands):
  eqs.append((1<<j)^(1<<((j+1)%9))^(1<<(9+k)))
 for j in range(9):
  c=s[j+9*rail]
  if c!='?':eqs.append((1<<j) | (int(c=='/')<<12))
 return eqs

def group(s,commands):
 loglike=0;candidate_exponent=0;rank0s=[];conflicts=[]
 for rail in range(9):
  eqs=equations(commands,rail,s)
  base,contr=rank(eqs[:9]); assert not contr
  total,contr=rank(eqs)
  rank0s.append(base)
  if contr:conflicts.append(rail)
  else:
   loglike-=total-base
   candidate_exponent+=12-total
 return {'log2_conditional_likelihood':loglike if not conflicts else None,
         'number_of_full_solutions_pow2':candidate_exponent if not conflicts else None,
         'incompatible_rails':conflicts,'baseline_rank':rank0s[0]}

def evaluate(s):
 opt=options(s);completions=list(itertools.product(*opt)) if all(opt) else []
 rows=[]
 for commands in completions:
  r=group(s,commands)
  rows.append((commands,r))
 ok=[(cmd,r) for cmd,r in rows if r['log2_conditional_likelihood'] is not None]
 best=max((r['log2_conditional_likelihood'] for cmd,r in ok),default=None)
 return {'selector_completions':len(completions),'compatible_codebooks':len(ok),
         'best_log2_likelihood':best,'best_log2_bf_vs_iid':(best+sum(c!='?' for c in s[:81])) if best is not None else None,
         'max_satisfied_rails':max((9-len(r['incompatible_rails']) for c,r in rows),default=0),
         'witnesses':[{'commands':list(c),'results':r} for c,r in ok[:15]],
         'failed_models':[{'commands':list(c),'conflicts':r['incompatible_rails']} for c,r in rows[:6]]}

def shuffle(s,rng,mode):
 x=s[:]
 if mode=='frame':gr=[list(range(i*9,(i+1)*9)) for i in range(9)]
 elif mode=='class':gr=[[j+9*k for k in range(9)] for j in range(9)]
 elif mode=='zone':gr=[list(range(81))]
 else:raise ValueError(mode)
 for g in gr:
  ind=[i for i in g if x[i]!='?'];vl=[x[i] for i in ind];rng.shuffle(vl)
  for i,v in zip(ind,vl):x[i]=v
 return x

def two_step_involution_obstruction(s):
 """Exact physical witness conditional on one-slash-per-class selectors.

 H command position 2 and I command position 2 force one shared operation
 twice along H -> I -> A. An involution implies A and H are identical.
 """
 opts=options(s)
 h,i=opts[7],opts[8]
 a_ob=s[9]  # residue 10: class A, second body row
 h_ob=s[16] # residue 17: class H, second body row
 return {'class_H_command_positions':h,'class_I_command_positions':i,
         'body_residue_10_A':a_ob,'body_residue_17_H':h_ob,
         'involution_incompatible':h==i==[2] and (a_ob,h_ob)==('-','/'),
         'proof':'H->I->A executes identical command 2 twice. Any command O with O^2=identity forces A==H at all body positions; raw residues 10 (-) and 17 (/) disagree.'}

def test():
 assert rank([1,2,4])==(3,False)
 assert rank([1,1|(1<<12)])==(1,True)
 assert rank([1|1<<12,2,3])==(2,True)
 x=['?']*108
 # For exact one-hot commands all opcode0, identity masks=0 can support all-zero input.
 for i in range(9):x[81+i]='/' ;x[90+i]='.';x[99+i]='.'
 for i in range(81):x[i]='-'
 r=evaluate(x);assert r['compatible_codebooks']==1 and r['selector_completions']==1
 x[9]='/' # class A and B have different bit0 but opcode same across all; one transition can flip and next undo?
 assert evaluate(x)['compatible_codebooks']==0
 return 'GF(2) elimination, structural cycle and forced-bit synthetic fixtures passed'

def run(s,n=250):
 obs=evaluate(s);rng=random.Random(20261013)
 controls={}
 for mode in ('frame','class','zone'):
  res=[evaluate(shuffle(s,rng,mode)) for _ in range(n)]
  controls[mode]={'replicates':n,'compatible_ge':sum(x['compatible_codebooks']>=obs['compatible_codebooks'] for x in res),
                  'any_compatible':sum(x['compatible_codebooks']>0 for x in res),
                  'best_bf_ge':sum(x['best_log2_bf_vs_iid'] is not None and x['best_log2_bf_vs_iid']>=obs['best_log2_bf_vs_iid'] for x in res) if obs['best_log2_bf_vs_iid'] is not None else None,
                  'median_compatible':statistics.median(x['compatible_codebooks'] for x in res),
                  'max_rail_ge':sum(x['max_satisfied_rails']>=obs['max_satisfied_rails'] for x in res)}
 return {'experiment':'CL-VLEN-09','scope':'stateful 9-bit class-to-class XOR masks selected by three slash/dot control positions, cyclic 9 register program',
         'source':'data/observations.csv; 84 records/66 unique H108 residues','status':'DISCOVER/DEVELOP only','observed':obs,'matched_null':controls,'two_step_obstruction':two_step_involution_obstruction(s),'invariants':test()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--observations',type=Path,default=Path('data/observations.csv'));p.add_argument('--nulls',type=int,default=250);p.add_argument('--test',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
 if a.test:print(test());return
 d=run(read(a.observations),a.nulls)
 s=json.dumps(d,indent=2,sort_keys=True)
 if a.output:a.output.write_text(s+'\n')
 print(json.dumps({'observed':d['observed'],'matched_null':d['matched_null']},indent=2))
if __name__=='__main__':main()