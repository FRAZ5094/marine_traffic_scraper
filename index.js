const puppeteer = require("puppeteer");

const preparePageForTests = async (page) => {
  // Pass the User-Agent Test.
  const userAgent =
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0";
  await page.setUserAgent(userAgent);
};

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const url =
    "https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position,notes&current_port_in|begins|DUNDEE|current_port_in=735";
  const url2 = "https://learnwebcode.github.io/practice-requests/";
  await page.goto(url);

  await page.waitForNavigation({
    waitUntil: "networkidle2",
  });

  //await page.screenshot({ path: "screnshot.png" });

  const result = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("div.ag-react-container")).map(
      (x) => x.textContent
    );
  });

  console.log(JSON.stringify(result));

  //console.log("closing");

  await browser.close();
})();
