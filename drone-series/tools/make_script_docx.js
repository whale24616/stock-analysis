// Build bilingual (EN | KO) script .docx files from drone-series/scripts/epNN.json
// Usage: node make_script_docx.js <outDir> [ep numbers...]   (no numbers = all + combined)
const fs=require('fs'), path=require('path');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,HeadingLevel,AlignmentType,BorderStyle,Footer,PageNumber,TableLayoutType,VerticalAlign,TableOfContents,PageBreak}=require('docx');
const SRC=path.join(__dirname,'..','scripts');
const OUT=process.argv[2]||'.'; const only=process.argv.slice(3).map(Number);
const FONT={ascii:'Calibri',hAnsi:'Calibri',eastAsia:'Malgun Gothic',cs:'Calibri'};
const TW=9638, CW=[4819,4819];
const border={style:BorderStyle.SINGLE,size:4,color:'D0D7DE'};
const borders={top:border,bottom:border,left:border,right:border};
const PART=n=>n<=5?'PART 1 · OFFENSE (공격)':'PART 2 · DEFENCE (방어)';
function runs(t,size){
  const out=[]; const parts=t.split(/(\*\*\[FACT-CHECK[^\]]*\]\*\*|\[FACT-CHECK[^\]]*\]|\*\*[^*]+\*\*|\*[^*]+\*)/);
  for(const p of parts){ if(!p) continue;
    if(p.includes('[FACT-CHECK')) out.push(new TextRun({text:' '+p.replace(/\*/g,''),font:FONT,size:size-4,color:'B45309',italics:true}));
    else if(p.startsWith('**')) out.push(new TextRun({text:p.slice(2,-2),font:FONT,size,bold:true}));
    else if(p.startsWith('*')&&p.endsWith('*')&&p.length>2) out.push(new TextRun({text:p.slice(1,-1),font:FONT,size,italics:true}));
    else out.push(new TextRun({text:p,font:FONT,size}));
  } return out;
}
const P=(t,size=21)=>new Paragraph({spacing:{after:120,line:300},children:runs(t,size)});
function cell(t,w,head=false){
  return new TableCell({width:{size:w,type:WidthType.DXA},borders,verticalAlign:VerticalAlign.TOP,margins:{top:100,bottom:100,left:140,right:140},
    shading:head?{type:ShadingType.CLEAR,fill:'0B1215',color:'auto'}:undefined,
    children:[head?new Paragraph({children:[new TextRun({text:t,font:FONT,size:20,bold:true,color:'FFFFFF'})]}):new Paragraph({spacing:{line:300},children:runs(t,20)})]});
}
const words=d=>d.sections.reduce((a,s)=>a+s.paras_en.reduce((b,p)=>b+p.replace(/\*\*\[FACT-CHECK[^\]]*\]\*\*/g,'').split(/\s+/).filter(Boolean).length,0),0);
const fc=d=>d.sections.reduce((a,s)=>a+s.paras_en.reduce((b,p)=>b+(p.match(/\[FACT-CHECK/g)||[]).length,0),0);
function episodeBlocks(d,{combined}){
  const n=String(d.ep).padStart(2,'0'); const c=[];
  c.push(new Paragraph({pageBreakBefore:combined,spacing:{after:60},children:[new TextRun({text:'DRONE WAR DECODED · '+PART(d.ep),font:FONT,size:20,bold:true,color:'3FA9A3'})]}));
  c.push(new Paragraph({heading:combined?HeadingLevel.HEADING_1:HeadingLevel.TITLE,spacing:{after:100},children:[new TextRun({text:`EP${n} — ${d.title_en}`,font:FONT,size:combined?40:48,bold:true})]}));
  c.push(new Paragraph({spacing:{after:200},children:[new TextRun({text:`${d.title_ko} · ${d.subtitle_ko}`,font:FONT,size:24,color:'555555'})]}));
  const w=words(d), mins=(w/140);
  const info=[['예상 러닝타임',`약 ${Math.floor(mins)}분 ${Math.round((mins%1)*60)}초 (분당 140단어 기준, 영어 ${w}단어)`],['확인 필요 항목',`[FACT-CHECK] ${fc(d)}개`],['원문 언어','영어 (내레이션 원본) · 오른쪽 한국어 번역']];
  c.push(new Table({width:{size:TW,type:WidthType.DXA},columnWidths:[2400,7238],rows:info.map(([a,b])=>new TableRow({children:[
    new TableCell({width:{size:2400,type:WidthType.DXA},borders,shading:{type:ShadingType.CLEAR,fill:'EEF4F5',color:'auto'},margins:{top:80,bottom:80,left:140,right:140},children:[new Paragraph({children:[new TextRun({text:a,font:FONT,size:20,bold:true})]})]}),
    new TableCell({width:{size:7238,type:WidthType.DXA},borders,margins:{top:80,bottom:80,left:140,right:140},children:[new Paragraph({children:[new TextRun({text:b,font:FONT,size:20})]})]})]}))}));
  d.sections.forEach((s,i)=>{
    if(s.paras_en.length!==s.paras_ko.length) throw new Error(`EP${n} section ${i} paragraph mismatch`);
    c.push(new Paragraph({heading:combined?HeadingLevel.HEADING_2:HeadingLevel.HEADING_1,spacing:{before:360,after:60},keepNext:true,children:[new TextRun({text:s.title_en,font:FONT,size:combined?26:28,bold:true,color:'0B1215'})]}));
    c.push(new Paragraph({spacing:{after:140},keepNext:true,children:[new TextRun({text:s.title_ko,font:FONT,size:22,color:'3FA9A3'})]}));
    c.push(new Table({width:{size:TW,type:WidthType.DXA},columnWidths:CW,layout:TableLayoutType.FIXED,rows:[
      new TableRow({tableHeader:true,children:[cell('ENGLISH (narration)',CW[0],true),cell('한국어 번역',CW[1],true)]}),
      ...s.paras_en.map((p,j)=>new TableRow({cantSplit:true,children:[cell(p,CW[0]),cell(s.paras_ko[j],CW[1])]}))]}));
  });
  return c;
}
const legend=()=>[
  new Paragraph({spacing:{before:240,after:80},children:[new TextRun({text:'읽는 법',font:FONT,size:22,bold:true})]}),
  P('왼쪽은 녹음용 영어 원문, 오른쪽은 한국어 번역입니다. 굵은 글씨는 화면 그래픽과 연결되는 핵심 용어입니다.'),
  P('[FACT-CHECK] 주황색 표시는 업로드 전에 최신 공개자료(RUSI, ISW, CSIS, Oryx, Reuters 등)로 반드시 확인해야 할 수치·사건입니다.')];
function doc(children,label){
  return new Document({styles:{default:{document:{run:{font:FONT,size:21}}}},features:{updateFields:true},
    sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1134,bottom:1134,left:1134,right:1134}}},
      footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:`Drone War Decoded · ${label} · `,font:FONT,size:16,color:'888888'}),new TextRun({children:[PageNumber.CURRENT],font:FONT,size:16,color:'888888'})]})]})},
      children}]});
}
const files=fs.readdirSync(SRC).filter(f=>/^ep\d\d\.json$/.test(f)).sort();
const eps=files.map(f=>JSON.parse(fs.readFileSync(path.join(SRC,f))));
(async()=>{
  fs.mkdirSync(OUT,{recursive:true});
  for(const d of eps){ if(only.length&&!only.includes(d.ep)) continue;
    const n=String(d.ep).padStart(2,'0'); const name=`EP${n}_${d.title_en.replace(/[^A-Za-z0-9]+/g,'-').replace(/-$/,'')}_Script_EN-KO.docx`;
    fs.writeFileSync(path.join(OUT,name),await Packer.toBuffer(doc([...episodeBlocks(d,{combined:false}),...legend()],`EP${n} script (EN/KO)`)));
    console.log(name,words(d),'words');
  }
  if(!only.length){
    const c=[];
    c.push(new Paragraph({spacing:{before:2400,after:120},children:[new TextRun({text:'DRONE WAR DECODED',font:FONT,size:64,bold:true})]}));
    c.push(new Paragraph({spacing:{after:200},children:[new TextRun({text:'How Ukraine Rewrote Modern Warfare',font:FONT,size:32,color:'3FA9A3'})]}));
    c.push(new Paragraph({spacing:{after:600},children:[new TextRun({text:'전체 대본 EP01–EP10 · 영어 원문 + 한국어 번역',font:FONT,size:28,color:'555555'})]}));
    const rows=eps.map(d=>[`EP${String(d.ep).padStart(2,'0')}`,d.title_en,d.title_ko,d.ep<=5?'공격':'방어',String(words(d))]);
    const cw=[900,3300,3038,900,1500];
    const hc=(t,w)=>new TableCell({width:{size:w,type:WidthType.DXA},borders,shading:{type:ShadingType.CLEAR,fill:'0B1215',color:'auto'},margins:{top:80,bottom:80,left:120,right:120},children:[new Paragraph({children:[new TextRun({text:t,font:FONT,size:19,bold:true,color:'FFFFFF'})]})]});
    const bc=(t,w)=>new TableCell({width:{size:w,type:WidthType.DXA},borders,margins:{top:80,bottom:80,left:120,right:120},children:[new Paragraph({children:[new TextRun({text:t,font:FONT,size:19})]})]});
    c.push(new Table({width:{size:TW,type:WidthType.DXA},columnWidths:cw,rows:[new TableRow({tableHeader:true,children:['편','English title','한국어 제목','구분','영어 단어'].map((t,i)=>hc(t,cw[i]))}),...rows.map(r=>new TableRow({children:r.map((t,i)=>bc(t,cw[i]))}))]}));
    c.push(...legend());
    c.push(new Paragraph({children:[new PageBreak()]}));
    c.push(new Paragraph({spacing:{after:120},children:[new TextRun({text:'목차 (Table of Contents)',font:FONT,size:28,bold:true})]}));
    c.push(new TableOfContents('Contents',{hyperlink:true,headingStyleRange:'1-1'}));
    c.push(new Paragraph({spacing:{before:120},children:[new TextRun({text:'※ 목차가 비어 보이면 Word에서 목차를 클릭 → “필드 업데이트”를 누르세요.',font:FONT,size:18,color:'888888'})]}));
    for(const d of eps) c.push(...episodeBlocks(d,{combined:true}));
    const name='Drone-War-Decoded_EP01-EP10_All-Scripts_EN-KO.docx';
    fs.writeFileSync(path.join(OUT,name),await Packer.toBuffer(doc(c,'All scripts EP01–EP10 (EN/KO)')));
    console.log(name);
  }
})();
