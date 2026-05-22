'use client';
import { useEffect, useState } from 'react';

type P={x:number,y:number}; type C={top_left:P;top_right:P;bottom_right:P;bottom_left:P};
const order:(keyof C)[]=['top_left','top_right','bottom_right','bottom_left'];

export default function Page(){
  const [items,setItems]=useState<any[]>([]); const [idx,setIdx]=useState(0); const [corners,setCorners]=useState<C|null>(null);
  useEffect(()=>{fetch('http://localhost:8000/api/images').then(r=>r.json()).then(d=>setItems(d.items||[]));},[]);
  const cur=items[idx];
  useEffect(()=>{if(!cur)return; fetch(`http://localhost:8000/api/predict/${cur.image_id}`,{method:'POST'}).then(r=>r.json()).then(d=>setCorners(d.corners));},[cur?.image_id]);
  const save=()=>cur&&corners&&fetch(`http://localhost:8000/api/annotations/${cur.image_id}`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({corners_px:corners,status:'corrected'})});
  return <main style={{padding:20,fontFamily:'sans-serif'}}>
    <h1>Nutrition Corner Tool (MVP)</h1>
    <button onClick={()=>setIdx(Math.max(0,idx-1))}>B</button><button onClick={()=>setIdx(Math.min(items.length-1,idx+1))}>N</button><button onClick={save}>S</button>
    <p>{cur?.filename||'Keine Bilder'}</p>
    <div style={{position:'relative',width:800,height:600,border:'1px solid #ccc'}}>
      {corners&&order.map(k=><div key={k} title={k} onMouseDown={(e)=>{const move=(ev:MouseEvent)=>setCorners(s=>s?{...s,[k]:{x:Math.max(0,Math.min(800,ev.offsetX)),y:Math.max(0,Math.min(600,ev.offsetY))}}:s); window.onmousemove=move; window.onmouseup=()=>{window.onmousemove=null;};}}
      style={{position:'absolute',left:corners[k].x-6,top:corners[k].y-6,width:12,height:12,borderRadius:8,background:'red',cursor:'move'}}/>) }
    </div>
  </main>
}
