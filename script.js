const input=document.getElementById("urlInput");
const btn=document.getElementById("scanBtn");
const result=document.getElementById("result");
const status=document.getElementById("status");
const score=document.getElementById("score");
const meter=document.getElementById("meterFill");
const reasons=document.getElementById("reasons");

function useExample(url){input.value=url; scan();}

async function scan(){
  const url=input.value.trim();
  if(!url){input.focus();return;}
  btn.disabled=true; btn.textContent="SCANNING...";
  try{
    const res=await fetch("/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url})});
    const data=await res.json();
    result.classList.remove("hidden");
    status.textContent=data.status;
    score.textContent=data.score;
    meter.style.width=data.score+"%";
    reasons.innerHTML=data.reasons.map(r=>`<li>${r}</li>`).join("");
    result.scrollIntoView({behavior:"smooth",block:"center"});
  }catch(e){alert("Could not scan. Make sure the Flask server is running.");}
  finally{btn.disabled=false;btn.textContent="SCAN LINK";}
}
btn.addEventListener("click",scan);
input.addEventListener("keydown",e=>{if(e.key==="Enter")scan();});
