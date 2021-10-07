const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const url = "https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&current_port_in|begins|DUNDEE|current_port_in=735";
  const url2 = "https://linuxize.com/post/how-to-install-node-js-on-raspberry-pi/"
  await page.goto(url);
  await page.waitForNavigation({
    waitUntil: 'networkidle0',
  });

  const result = await page.evaluate(() => {
    let a = document.querySelectorAll(".ag-cell-content-link");
    const names = [...a];

    return names
  })

  console.log(result);

  console.log("closing");

  await browser.close();
})();
