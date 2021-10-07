const puppeteer = require("puppeteer");
const fs = require('fs');

const preparePageForTests = async (page) => {
  // Pass the User-Agent Test.
  const userAgent =
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0";
  await page.setUserAgent(userAgent);
};

(async () => {
const browser = await puppeteer.launch({
	headless: true,
	executablePath: '/usr/bin/chromium-browser',
	args: ['--no-sandbox', '--disable-setuid-sandbox']
});
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
    return Array.from(document.querySelectorAll("a.ag-cell-content-link")).map((x) => x.title).filter(x => x != "");
  });

  let boat_names = result.map((x) => x.slice(18))

  let epoch = Date.now();

  let data = {"timestamp": epoch, "boats": boat_names}

  const filename = "dundee_port_data.json";

  const file = fs.readFileSync(filename, 'utf8')
  let file_json = JSON.parse(file);
  file_json.push(data);
  fs.writeFileSync(filename, JSON.stringify(file_json, null, 2), "utf-8");

  await browser.close();
})();
