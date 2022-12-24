# https://github.com/mybdye 🌟


import os, requests, urllib, pydub, base64, ssl, random
from seleniumbase import SB
from func_timeout import func_set_timeout, FunctionTimedOut
from urllib.parse import quote
import pyscreenshot as ImageGrab

@func_set_timeout(30)
def urlOpen(url):
    try:
        print('- url open:', url)
        sb.open(url)
        print('- func url open finish')
    except FunctionTimedOut as e:
        print('- 👀 url open:', e)
   

def checkbox():
    print('- click checkbox')
    checkbox = 'span#recaptcha-anchor'
    try:
        sb.wait_for_element(checkbox)
        sb.click(checkbox)
        sb.sleep(4)
    except FunctionTimedOut as e:
        print('- 👀 checkbox:', e)
    
    
def recaptcha():
    global body
    print('- recaptcha')
    try:
        #sb.open(urlLogin)
        urlOpen(urlLogin)
        sb.assert_text('Login', 'h2', timeout=20)
        print('- access')
    except Exception as e:
        print('- 👀 sb.open() issue: %s \nwhen open: %s' % (e,sb.get_current_url()))
        #sb.driver.close()
        return False
    #   reCAPTCHA
    sb.switch_to_frame('[src*="/recaptcha/api2/anchor?"]')
    print('- switch to frame checkbox')
    checkbox()
    try:
        #   预防弹了广告
        sb.switch_to_window(0)
        sb.switch_to_frame('[src*="/recaptcha/api2/anchor?"]')
    except Exception as e:
        print('- 👀 switch issue:', e)
    status = checkbox_status()
    tryReCAPTCHA = 1
    while status != 'true':
        sb.switch_to_default_content()  # Exit all iframes
        sb.sleep(1)
        sb.switch_to_frame('[src*="/recaptcha/api2/bframe?"]')
        print('- switch to frame image/audio')
        sb.click("button#recaptcha-audio-button")
        try:
            sb.assert_element('[href*="/recaptcha/api2/payload/audio.mp3?"]', timeout=20)
            print('- normal')
            src = sb.find_elements('[href*="/recaptcha/api2/payload/audio.mp3?"]'
                                   )[0].get_attribute("href")
            print('- audio src:', src)
            # download audio file
            urllib.request.urlretrieve(src, os.getcwd() + audioMP3)
            mp3_to_wav()
            text = speech_to_text()
            if text == '':
                screenshot()
                break
            sb.switch_to_window(0)
            sb.assert_text('Login', 'h2', timeout=20)
            sb.switch_to_default_content()  # Exit all iframes
            sb.sleep(1)
            sb.switch_to_frame('[src*="/recaptcha/api2/bframe?"]')
            sb.type('#audio-response', text)
            sb.click('button#recaptcha-verify-button')
            sb.sleep(4)
            sb.switch_to_default_content()  # Exit all iframes
            sb.switch_to_frame('[src*="/recaptcha/api2/anchor?"]')
            sb.sleep(1)
            status = checkbox_status()

        except Exception as e:
            print('- 💣 Exception:', e)
            body = e
            sb.switch_to_default_content()  # Exit all iframes
            sb.sleep(1)
            sb.switch_to_frame('[src*="/recaptcha/api2/bframe?"]')
            msgBlock = '[class*="rc-doscaptcha-body-text"]'
            if sb.assert_element(msgBlock, timeout=20):
                body = sb.get_text(msgBlock)
                print('- 💣 maybe block by google\n', body)
                body = '[%s***]\n💣 %s' % (username[:3], body)
                break
            elif tryReCAPTCHA > 3:
                break
            else:
                tryReCAPTCHA += 1
    if status == 'true':
        print('- reCAPTCHA solved!')
        return True


def login():
    print('- login')
    sb.switch_to_default_content()  # Exit all iframes
    sb.sleep(1)
    sb.type('#text', username)
    sb.type('#password', password)
    sb.click('button:contains("Submit")')
    sb.sleep(20)
    sb.assert_exact_text('ACTIVE', '[class*="badge badge-success"]', timeout=20)
    print('- login success')
    return True


def checkbox_status():
    print('- checkbox_status')
    statuslist = sb.find_elements('#recaptcha-anchor')
    # print('- statuslist:', statuslist)
    status = statuslist[0].get_attribute('aria-checked')
    print('- status:', status)
    return status


def mp3_to_wav():
    print('- mp3_to_wav')
    pydub.AudioSegment.from_mp3(
        os.getcwd() + audioMP3).export(
        os.getcwd() + audioWAV, format="wav")
    print('- mp3_to_wav done')


def speech_to_text():
    print('- speech_to_text')
    sb.open_new_window()
    text = ''
    trySpeech = 1
    while trySpeech <= 3:
        print('- trySpeech *', trySpeech)
        sb.open(urlSpeech)
        sb.assert_text('Speech to text', 'h1', timeout=10)
        sb.choose_file('input[type="file"]', os.getcwd() + audioWAV)
        sb.sleep(12)
        response = sb.get_text('[id*="speechout"]')
        print('- response:', response)
        try:
            text = response.split('-' * 80)[1].split('\n')[1].replace('. ', '.')
            print('- text:', text)
            if ' ' in text:
                break
        except Exception as e:
            print('- 💥 speech2text:', e)
        trySpeech += 1
    return text


def renew():
    global statuRenew
    print('- renew')
    #sb.open(urlRenew)
    urlOpen(urlRenew)
    sb.sleep(2)
    #screenshot()
    #sb.switch_to_window(0)
    sb.assert_text('Renew VPS', 'h2', timeout=10)
    print('- access')
    #
    print('- fill web_address')
    web_address = '#web_address'
    sb.wait_for_element(web_address, timeout=20)
    sb.type(web_address, urlBase)
    print('- fill web_address done')
    #   captcha
    number1 = int(sb.find_elements('img[src]')[0].get_attribute('src').split('-')[1][0])
    number2 = int(sb.find_elements('img[src]')[1].get_attribute('src').split('-')[1][0])
    method = sb.get_text('[class*="col-sm-3"]').split('=')[0]

    if method == '+':
        captcharesult = number1 + number2
    elif method == '-':
        # 应该没有 但还是写了
        captcharesult = number1 - number2
    elif method == 'X' or method == 'x':
        captcharesult = number1 * number2
    elif method == '/':
        # 应该没有 但还是写了
        captcharesult = number1 / number2

    captcharesult = int(captcharesult)
    print('- captcharesult: %d %s %d = %d' % (number1, method, number2, captcharesult))
    #
    sb.sleep(random.randint(1,3))
    print('- fill captcha')
    sb.type('#captcha', captcharesult)
    #
    sb.sleep(random.randint(1,3))
    print('- check agreement')
    sb.click('[name*="agreement"]')
    #
    sb.sleep(random.randint(1,3))
    print('- click Renew VPS')
    sb.click('button:contains("Renew VPS")')
    sb.sleep(8)
    statuRenew = renew_check()


def renew_check():
    global body, countRenew
    print('- renew_check')
    sb.assert_element('div#response', timeout=20)
    print('- access')
    body = sb.get_text('div#response')
    i = 1
    while body == 'Loading.....':
        if i > 3:
            break
        print('- waiting for response... *', i)
        sb.sleep(2)
        body = sb.get_text('div#response')
        i += 1
    print('- response [After %d run(s)]: %s' % (countRenew, body))
    if 'renew' in body:
        body = '[%s***][After %d run(s)]\n🎉 %s' % (username[:3], countRenew, body)
        return True
    else:
        body = '[%s***][After %d run(s)]\n💣 %s' % (username[:3], countRenew, body)



def screenshot():
    global body
    print('- screenshot')
    # grab fullscreen
    im = ImageGrab.grab()
    # save image file
    im.save("fullscreen.png")
    
    #sb.save_screenshot(imgFile, folder=os.getcwd())
    print('- screenshot done')
    sb.open_new_window()
    print('- screenshot upload')
    sb.open('http://imgur.com/upload')
    # sb.choose_file('input[type="file"]', os.getcwd() + '/' + imgFile)
    sb.choose_file('input[type="file"]', "fullscreen.png")
    sb.sleep(6)
    imgUrl = sb.get_current_url()
    i = 1
    while not '/a/' in imgUrl:
        if i > 3:
            break
        print('- waiting for url... *', i)
        sb.sleep(2)
        imgUrl = sb.get_current_url()
        i += 1
    print('- 📷 img url:', imgUrl)
    body = imgUrl
    print('- screenshot upload done')

    return imgUrl


def url_decode(s):
    return str(base64.b64decode(s + '=' * (4 - len(s) % 4))).split('\'')[1]


def push(body):
    print('- body: %s \n- waiting for push result' % body)
    
    # tg push
    if tgBotToken == '' or tgUserID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        tgbody = urlBase + '\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + tgBotToken + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': tgUserID, 'text': tgbody}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))
            
    # bark push
    if barkToken == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + barkToken
        barktitle = quote(urlBase, safe='')
        barkbody = quote(body, safe='')
        rq_bark = requests.get(url=f'{barkurl}/{barktitle}/{barkbody}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))
    
    print('- push finish!')


##
try:
    urlBase = os.environ['URL_BASE']
except:
    # 本地调试用， please type here the website address without any 'https://' or '/'
    urlBase = ''
try:
    username = os.environ['USERNAME']
except:
    # 本地调试用
    username = ''
try:
    password = os.environ['PASSWORD']
except:
    # 本地调试用
    password = ''
try:
    barkToken = os.environ['BARK_TOKEN']
except:
    # 本地调试用
    barkToken = ''
try:
    tgBotToken = os.environ['TG_BOT_TOKEN']
except:
    # 本地调试用
    tgBotToken = ''
try:
    tgUserID = os.environ['TG_USER_ID']
except:
    # 本地调试用
    tgUserID = ''
##
body = ''
statuRenew = False
countRenew = 1
audioMP3 = '/' + urlBase + '.mp3'
audioWAV = '/' + urlBase + '.wav'
# imgFile = urlBase + '.png'
##
urlLogin = 'https://' + urlBase + '/login'
urlRenew = 'https://' + urlBase + '/vps-renew'
urlSpeech = url_decode(
    'aHR0cHM6Ly9henVyZS5taWNyb3NvZnQuY29tL2VuLXVzL3Byb2R1Y3RzL2NvZ25pdGl2ZS1zZXJ2aWNlcy9zcGVlY2gtdG8tdGV4dC8jZmVhdHVyZXM==')
# 关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

with SB(uc=True, pls="none", sjw=True) as sb:  # By default, browser="chrome" if not set.
    print('- 🚀 loading...')
    if urlBase != '' and username != '' and password != '':
        try:
            if recaptcha():
                if login():
                    while not statuRenew:
                        if countRenew > 15:
                            break
                        renew()
                        countRenew += 1
        except Exception as e:
            print('- 💥', e)
            try:
                screenshot()
            finally:
                push(str(e))
        push(body)
    else:
        print('- please check urlBase/username/password')

# END
