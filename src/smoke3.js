const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:390,height:844}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+process.cwd()+'/prototype/v60-prototype.html');
  await p.click('[data-tab=beans]');
  for(const r of ['roots','jebla','east48']){await p.click('[data-set=libR][data-val='+r+']');console.log(r,await p.locator('[data-use]').count());}
  await p.screenshot({path:'shot_lib.png',fullPage:false});
  await p.click('[data-tab=me]');await p.click('[data-set=lang][data-val=ar]');await p.click('[data-tab=beans]');await p.screenshot({path:'shot_lib_ar.png'});
  await p.click('[data-use=e9]');console.log('brew bean:',(await p.locator('main').innerText()).slice(0,200).replace(/\n/g,' | '));
  await p.click('[data-tab=beans]');await p.click('[data-lib=e4]').catch(e=>console.log('no lib btn'));
  console.log('errors:',JSON.stringify(errs));await b.close();
})();
