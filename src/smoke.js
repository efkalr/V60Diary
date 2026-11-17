const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(async()=>chromium.launch());
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+process.cwd()+'/prototype/v60-prototype.html');
  await p.click('[data-act=pick]');await p.screenshot({path:'shot_picker.png'});await p.click('[data-roastery=jebla]');await p.click('[data-pickb=j12]');await p.screenshot({path:'shot_jebla.png'});await p.click('[data-act=pick]');await p.click('[data-roastery=east48]');await p.screenshot({path:'shot_east.png'});await p.click('[data-pickb=e16]');await p.screenshot({path:'shot_my.png'});
  await p.click('[data-act=start]');await p.waitForTimeout(600);await p.click('[data-act=finish]');
  await p.click('[data-tag=sour]');await p.click('[data-act=fix]');await p.click('[data-act=apply]');await p.click('[data-act=saveTaste]');
  for(const t of ['beans','me','log','brew'])await p.click('[data-tab='+t+']');
  await p.click('[data-tab=me]');await p.selectOption('#gSel','esp');await p.screenshot({path:'shot.png'});
  console.log('errors:',JSON.stringify(errs));await b.close();
})();
