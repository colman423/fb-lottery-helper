# encoding=UTF-8
from flask import Flask, render_template, request, Response
from scraper import Scraper
from lottery import lottery
import json

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 1
    return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrapy/<source>', methods=['POST'])
def scrapy(source):
    if source=="group":
        req = request.get_json()
        if 'comment_options' in req:
            comment_options = {
                'TAGS': int(req['comment_options']['tag']),
                'TEXT': req['comment_options']['text']
            }
        else:
            comment_options = {
                'TAGS': 0,
                'TEXT': ""
            }            
        try:
            legal_list = Scraper(req['post_link'], comment_options, req['need_like']).run()
        except Exception as e:
            print("YA", e, "YA")
            return str(e), 400
        legal_list = [ { 'name': item[0], 'url': item[1], 'comment': item[2] } for item in legal_list ]
        # print(legal_list)
        # legal_list = [{"name":"王品云","url":"/profile.php?id=100001701070269","comment":"星巴克抽起來！ 陳毓珊 呂佳穎"},{"name":"林心瑜","url":"/rhoda980224","comment":"星巴克抽起來！ 吳奕柔 蘇子淳"},{"name":"陳品潔","url":"/profile.php?id=100004430224605","comment":"星巴克抽起來!陳信甫 Cht Yang"},{"name":"徐藝庭","url":"/xu.t.ting.7","comment":"星巴克抽起來! 林余柔 葉楹茹"},{"name":"Crystal Ooi","url":"/jin0812","comment":"星巴克抽起來！ Tina Huang Athena Wong"},{"name":"Yvan Cai","url":"/yvan.cai.9","comment":"星巴克抽起來! 楊彩柔謝育真喝咖啡打報告"},{"name":"Zyin Choy","url":"/Zyinchoy","comment":"星巴克抽起來！ Ng Angie Lim Saw Yu"},{"name":"何瑄芳","url":"/profile.php?id=100001720903109","comment":"蔡喬羽 蔡瑞紘 劉書妤 簡敬堂 李思儀 李銘翰 星巴克抽起來！幫幫我室友Chung Fiona的期末🙏🙏🙏"},{"name":"史純睿","url":"/ray.shih.54","comment":"星巴克抽起來! 王易達林琮軒"},{"name":"Weeyi Lim","url":"/weeyi.lim.1","comment":"Yimin Hsieh 邱明欣星巴克抽起來！"},{"name":"洪振旂","url":"/alexpetertom","comment":"星巴克抽起來! Jojo Chen 賴映竹"},{"name":"張博涵","url":"/profile.php?id=100004785340097","comment":"星巴克抽起來！Bryan Wang 葉孟昀"},{"name":"陳欣妤","url":"/profile.php?id=100003493913557","comment":"星巴克抽起來！黃欣儀闕千蘋"},{"name":"許庭瑄","url":"/profile.php?id=100007970101021","comment":"星巴克抽起來！ 曹瑩琇 楊博傑"},{"name":"陳怡安","url":"/profile.php?id=100005487766723","comment":"星巴克抽起來！蘇梅子 陳姿吟"},{"name":"楊喬茵","url":"/profile.php?id=100000361832779","comment":"星巴克抽起來! 葉明瑜孫靖媛"},{"name":"Lala Chi","url":"/profile.php?id=100004356125645","comment":"星巴克抽起來！陳信杰 林韋岑"},{"name":"劉冠履","url":"/profile.php?id=100009986258453","comment":"星巴克抽起來! 葉明瑜 孫靖媛"},{"name":"高士昌","url":"/scott.kao.73","comment":"星巴克抽起來！愷宸張蘇晏加"},{"name":"Hoi Ping Goh","url":"/hoiping.goh","comment":"星巴克抽起來！How Jia JianBeeKee Soon"},{"name":"吳貞慧","url":"/profile.php?id=100002109118707","comment":"星巴克抽起來！沈宛臻古孟君"},{"name":"林余柔","url":"/yuzo8866","comment":"星巴克抽起來！ 徐藝庭 傅有萱"},{"name":"許佩琪","url":"/profile.php?id=100002511869301","comment":"星巴克抽起來！楊雅筑Rita Yang"},{"name":"愷宸張","url":"/profile.php?id=100003804896982","comment":"星巴克抽起來！ 蘇晏加 Kulas Isin"},{"name":"林芯妘","url":"/profile.php?id=100003728904355","comment":"星巴克抽起來!潘羿辰 謝沅沅"},{"name":"張珮慈","url":"/yoolite","comment":"星巴克抽起來！ 彭湘晴 葉洧彤"},{"name":"謝宜憫","url":"/profile.php?id=100004056912711","comment":"星巴克抽起來！ 邱明欣 Chi Cheng"},{"name":"呂菱","url":"/arielluuu","comment":"星巴克抽起來！ 黃心瑜 余沁容"},{"name":"Angel Hsu","url":"/angel.hsu.3591","comment":"星巴克抽起來！ 林亞嬛 Sherlyn Tania"},{"name":"KaHei Chui","url":"/kahei.chui.5","comment":"星巴克抽起來! 黃俊瑋Wong Hoi Ian"},{"name":"何怡萱","url":"/chy880718","comment":"星巴克抽起來！范馨之洪嘉君"},{"name":"周祈鈞","url":"/profile.php?id=100009568613443","comment":"星巴克抽起來！葉馨謝弦"},{"name":"張皓鈞","url":"/profile.php?id=100000703535228","comment":"星巴克抽起來！尹可親徐樹紅"},{"name":"謝巧琳","url":"/profile.php?id=100000494577498","comment":"星巴克抽起來！ Cheah Bei Yi黃雪瑜"},{"name":"商婕瑜","url":"/jamie.shang.7","comment":"星巴克抽起來！魏語欣 徐慕薇"},{"name":"林孟璇","url":"/sherry.lin.896","comment":"星巴克抽起來！ 鄧雅云 邱華奕"},{"name":"王雅琳","url":"/profile.php?id=100003541445645","comment":"鄭佑瑩周葦星巴克抽起來！"},{"name":"陳秀玲","url":"/profile.php?id=100009155445602","comment":"星巴克抽起來！朱子涵 陳竫涵"},{"name":"顧采薇","url":"/profile.php?id=100003126297107","comment":"星巴克抽起來! Tan Jia Shin Daisy Ho"},{"name":"Shiyuan Sy","url":"/shiyuan.sy","comment":"星巴克抽起來! Annabelle Choo 黃雪瑜"},{"name":"周韋伶","url":"/weiling.zhou2","comment":"星巴克抽起來！Chou Yuhsun Tina Huang"},{"name":"羅亞帆","url":"/profile.php?id=100001466886832","comment":"星巴克抽起來！ Jack Lee 張以臻"},{"name":"黃妍婷","url":"/profile.php?id=100004162204699","comment":"星巴克抽起來！陳琪 Athena Wong"},{"name":"李宜璉","url":"/profile.php?id=100002701763522","comment":"星巴克抽起來！李雨璇 蔡之寧"},{"name":"蔡喜善","url":"/profile.php?id=100002436548346","comment":"星巴克抽起來! 王品云 王意涵"},{"name":"丁希彤","url":"/claireting714","comment":"星巴克抽起來趙芳瑀羅倩如"},{"name":"蘇蘇","url":"/profile.php?id=100000350261939","comment":"星巴克抽起來！陳孟緯郭令瑜"},{"name":"周采瑄","url":"/profile.php?id=100002612675055","comment":"星巴克抽起來！全書亞Hamber Chang"},{"name":"思穎","url":"/zhong.ying.9","comment":"吉他社星巴克抽起來！拯救期末大作戰哈哈哈鄭雅云蕭伊涵林莉雯林承懌邱致柔朱光愷Cindy Lin劉玉孝Alex Yin洪振傑丁顯翔徐子瑤還有好多人喔歡迎大家來抽獎！！"},{"name":"劉玉孝","url":"/profile.php?id=100004019411436","comment":"洪振傑 林承懌感謝我ㄅ\n星巴克抽起來"},{"name":"劉玉孝","url":"/profile.php?id=100004019411436","comment":"洪振傑 林承懌感謝我ㄅ\n星巴克抽起來"},{"name":"葉洧彤","url":"/ye.zi.980","comment":"胡馨尹吳昱弘星巴克抽起來！"},{"name":"邱致柔","url":"/amy.chiu.125","comment":"朱易宣張文姿填問卷救室友思穎星巴克抽起來！"},{"name":"邱致柔","url":"/amy.chiu.125","comment":"朱易宣張文姿填問卷救室友思穎星巴克抽起來！"},{"name":"楊恭豪","url":"/sun.how.71","comment":"星巴克抽起來！ 彭文亭 （WenTing Peng） 吳柏穎"},{"name":"Hui Yee","url":"/Huiyee1998","comment":"星巴克抽起來！Zyin ChoyRuo Thung"},{"name":"Stacie Hsiao","url":"/stacie.hsiao","comment":"紀妤岫施泯嘉星巴克抽起來！"},{"name":"楊晏婷","url":"/pa.zou.73","comment":"黃顗蓁 Sara Wu 星巴克抽起來"},{"name":"陳彥慈","url":"/profile.php?id=100000586324433","comment":"星巴克抽起來！劉北辰馬允中"},{"name":"林宜萱","url":"/sandylin.lin.92","comment":"星巴克抽起來！黃大瑋 謝孟慈"},{"name":"劉品婕","url":"/profile.php?id=100001432904325","comment":"星巴克抽起來! 江佩芸何硯涵"},{"name":"詹珮渝","url":"/carol011629","comment":"星巴克抽起來！ 李承樺 Tsung Chen"},{"name":"吳智穎","url":"/aaronlove1211","comment":"星巴克抽起來！張雅涵 張馨文"},{"name":"陳伯霏","url":"/profile.php?id=100001309787880","comment":"星巴克抽起來！ Godest Wang 黃品瑄"},{"name":"黃品瑄","url":"/cheynehuang","comment":"星巴克抽起來! 游皓鈞林勉"},{"name":"蕭子勤","url":"/profile.php?id=100000359172345","comment":"星巴克抽起來！ 宋弘軒張郁怜"},{"name":"陳品婕","url":"/jessicayoya","comment":"星巴克抽起來！Jacky Huang李梓翔"},{"name":"王偉力","url":"/godest.wang","comment":"星巴克抽起來！ 于其弘 周俐廷"},{"name":"Shu Lian","url":"/shu.lian.5","comment":"Hong DaTan Jia Shin 星巴克抽起來！"},{"name":"李昀","url":"/profile.php?id=100003402272483","comment":"星巴克抽起來！ 陳昕 張珈漩"},{"name":"張芳瑄","url":"/1997jennie","comment":"星巴克抽起來！ 許東溢 鮑威宇"},{"name":"黃語萱","url":"/profile.php?id=100002916605910","comment":"黃浩瑀 陳宜涵 星巴克抽起來!"},{"name":"范瑜庭","url":"/tina1226tina","comment":"陳奐君 吳念蓁 星巴克抽起來！"},{"name":"吳念蓁","url":"/profile.php?id=100000594528788","comment":"古欣璇張榛芸星巴克抽起來！"},{"name":"高慧君","url":"/profile.php?id=100013876578152","comment":"陳昱臻 王懿柔 星巴克抽起來！"},{"name":"Glory Liang","url":"/glory.liang.9","comment":"星巴克抽起來！許綺珊 黃郁茹"},{"name":"邱明欣","url":"/profile.php?id=100003615537778","comment":"星巴克抽起來!Yimin HsiehChi Cheng"},{"name":"林欣儒","url":"/profile.php?id=100003302436199","comment":"星巴克抽起來！郭嘉茵 陳韋君"},{"name":"吳恩庭","url":"/enting.wu1","comment":"星巴克抽起來！ 顏于傑吳恩庭"},{"name":"蘇毓涵","url":"/katie.sue.940","comment":"陳奕君徐若庭星巴克抽起來！"},{"name":"李昱萱","url":"/profile.php?id=100002037107245","comment":"星巴克抽起來！ 魏家琳 關雅文 （Maggie Guan）"},{"name":"羅歆瑜","url":"/pluviophilerusty","comment":"星巴克抽起來！ 張博涵 （Teresa Chang）王桂芳"},{"name":"王桂芳","url":"/profile.php?id=100002846095042","comment":"星巴克抽起來！張博涵 羅歆瑜"}]
        if 'csv_options' in req:
            print(req['csv_options'])
        return Response(json.dumps(legal_list),  mimetype='application/json')
    else:
        return "fk"

@app.route('/lottery', methods=['POST'])
def get_lottery():
    req = request.get_json()
    try:
        winner = lottery(req['prize'], req['legal_list'])
        return Response(json.dumps(winner),  mimetype='application/json')
    except KeyError:
        return "請先爬取中獎名單！", 400

if __name__ == "__main__":
    app.config['ENV'] = "development"
    app.config['DEBUG'] = True
    app.run(port=3000)