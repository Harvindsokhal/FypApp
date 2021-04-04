
function startScrape(){
    const fieled = document.querySelector('.custom-field input');
    const placeholder = document.querySelector('.custom-field .placeholder');
    const fieled1 = document.querySelector('.custom-field1 input');
    const placeholder1 = document.querySelector('.custom-field1 .placeholder1');
    const url = document.getElementById('url').value;
    const keyword = document.getElementById('keyword').value;
     
    const headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.wikipedia.org/',
        'Connection': 'keep-alive',
    }
    if (url == '' && keyword =='') {
        fieled.style.border = '2px solid red'
        placeholder.style.color = 'red'
        fieled1.style.border = '2px solid red'
        placeholder1.style.color = 'red'
    } else if (url.startsWith('https://exifmetadata.files.wordpress.com')) { 
        eel.make_soup(url, headers)
    } else if (url.startsWith('https://www.instagram.com')) {
        eel.InstagramScraper(url, keyword);
    } else if (url.startsWith('https://www.behance.net')) {
        eel.BehanceScraper(url, keyword);
    } else if (url.startsWith('https://www.pinterest.co.uk')) {
        eel.PinterestScraper(url, keyword);
    } else if (url.startsWith('http://flickr.com')) {
        eel.getToFlickr(url);
    }
}

eel.expose(setImageName);
function setImageName(data){
    document.getElementById('imageName').innerHTML = data;
}

eel.expose(setImageDate);
function setImageDate(data){
    document.getElementById('imageDate').innerHTML = data;
}

eel.expose(setImageTime);
function setImageTime(data){
    document.getElementById('imageTime').innerHTML = data;
}

eel.expose(setImageLocation);
function setImageLocation(data){
    document.getElementById('imageLocation').innerHTML = data;
}

function newPage(){
    location.replace("exifextract.html");
}

function getExif(){
    eel.selectImage()
}

eel.expose(successMessage);
function successMessage(){
    const ScrapeMessage = document.getElementById('status');
    ScrapeMessage.style.color = 'rgb(0, 255, 0)'
}

var rotate_factor = 0;

function rotateMe(e) {
    rotate_factor += 1;
    var rotate_angle = (180 * rotate_factor) % 360;
    $(e).rotate({angle:rotate_angle});
}