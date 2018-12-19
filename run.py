# encoding=UTF-8
from flask import Flask, render_template, request, Response
from scraper import Scraper
import lottery
import csv_filter
import json
from config import google_api

app = Flask(__name__)

@app.after_request
def add_header(response):   # disabled cached when debugging
    response.cache_control.max_age = 1
    return response

@app.route('/')
def index():    # get html page
    return render_template('index.html', google_key=google_api.key)

@app.route('/scrapy', methods=['POST'])
def scrapy():     # post scrapy setting to backend
    req = request.get_json()       # get setting
    print(req)
    if 'comment_options' in req:    # if need comment
        comment_options = {         
            'TAGS': int(req['comment_options']['tag']),
            'TEXT': req['comment_options']['text']
        }
    else:                       # if dont need comment, set an empty comment_options
        comment_options = {
            'TAGS': 0,
            'TEXT': ""
        }            
    try:
        legal_list = Scraper(req['post_link'], comment_options, req['need_like']).run()
    except Exception as e:
        print("except:", e, "QQWTF")
        return str(e), 400
    # print(legal_list)
    # legal_list = [('Claire Wang', '/xiao.xu.315', '簡叡張玄Lee KevinBryan Hsaio財管怪人們快來填'), ('Claire Wang', '/xiao.xu.315', '陳品妤Hannah Hsu♥️'), ('Chung Fiona', '/chung.fiona.90', 'Hoi Ping GohHui YeeYi Qi Goh'), ('Chung Fiona', '/chung.fiona.90','何瑄芳快利用你廣大的人脈哈哈哈'), ('Claire Wang', '/xiao.xu.315', 'Chloe Lin莊筑茵許珈維林心瑜王筠婷幫忙填個ㄅ🙏'), ('Yvan Cai', '/yvan.cai.9', '生理性別 女生變選項2'), ('王品云', '/profile.php?id=100001701070269', '邱品勛問卷是不是放錯了'), ('邱品勛', '/profile.php?id=100002458246114', '黃彥鈞許智超康銘揚 （Louis Yang）周哲偉施吟儒 （Yin-Ju Shih）許佳暄高菲兒 （高菲）李頫劉柏毅許筑涵 （Hannah Hsu）快來救救我的期末 嗚嗚 也祝你們中獎!!!!'), ('黃思文', '/profile.php?id=100003474270513', '陳柏安 黃子席'), ('康銘揚', '/profile.php?id=100003364707234', '許智超 黃彥鈞 星巴克喝起來'), ('Melvin Xuan', '/melvinxuan816', '星巴克喝起來 Claudia Tung Crystal Wee'), ('王品云', '/profile.php?id=100001701070269', '星巴克抽起來！ 陳毓珊 呂佳穎'), ('張菀庭', '/paula.chang.222', '星巴克喝起來 葉諠潔李容蘋'), ('Chung Fiona', '/chung.fiona.90', 'KaHei Chui張珮慈室友們救救我的期末❤️'), ('Chung Fiona', '/chung.fiona.90', 'Kelvin YapHowHow Jia JianTan Margin 小大一們幫忙填個 ❤️'), ('林心瑜', '/rhoda980224', '星巴克抽起來！ 吳奕柔 蘇子淳'), ('陳品潔', '/profile.php?id=100004430224605', '星巴克抽起來!陳信甫 Cht Yang'), ('徐藝庭', '/xu.t.ting.7', '星巴克抽起來! 林余柔 葉楹茹'), ('Chung Fiona', '/chung.fiona.90', 'Eva LaiKhor Yi YingTan Jou TingZyin ChoyRayne HohShiyuan Sy 大家有空的話幫忙填喔'), ('Claire Wang', '/xiao.xu.315', '謝竣竤黃芝穎徐湘淇方小瑀徐郁淳幫我填～～～～～❤️'), ('林佳融', '/profile.php?id=100002739680101', '倪芃宥 劉溦洵 星巴克喝起來'), ('許智超', '/witty.hsu', '星巴克喝起來！邱品勛 周新淳'), ('Crystal Ooi', '/jin0812', '星巴克抽起來！ Tina Huang Athena Wong'), ('陳姿吟', '/profile.php?id=100000528432603', '星巴克抽起來！ 陳怡安 蘇梅子'), ('王喬奕', '/profile.php?id=100004299759970', '星巴克抽起來! 陳宥滏 葉彥志'), ('Claire Wang', '/xiao.xu.315', '蔡雨華汪佩璇康育誠Allan Chen～～～'), ('Yvan Cai', '/yvan.cai.9', '星巴克抽起來! 楊彩柔謝育真喝咖啡打報告'), ('Zyin Choy', '/Zyinchoy', '星巴克抽起來！Ng Angie Lim Saw Yu'), ('吳芸安', '/profile.php?id=100003081041782', '星巴克抽起來！李季柔劉誼名'), ('Weeyi Lim', '/weeyi.lim.1', 'Yimin Hsieh 邱明欣'), ('Kelvin Yap', '/kelvinyapjk', '星巴克喝起來 Chey Siew Hui Yong Kai Wen'), ('陳詠晴', '/profile.php?id=100003473812196', '星巴克抽起來！Jo Yin Liao陳詠君'), ('何瑄芳', '/profile.php?id=100001720903109', '蔡喬羽 蔡瑞紘 劉書妤 簡敬堂 李思儀 李銘翰 星巴克抽起來！幫幫我室友Chung Fiona的期末🙏🙏🙏'), ('王意涵', '/miffy.wang.50', '星巴克抽起來！楊晴心 王品云'), ('史純睿', '/ray.shih.54', '星巴克抽起來! 王易達林琮軒'), ('Michael Wo', '/michael.wo.39','大推特推 徐丰毓Judy Chang李頫羅亞帆～～～～'), ('Chung Fiona', '/chung.fiona.90', 'Sophie Ellen Vincent Tjoe guys please ask ur friends for help 😄'), ('Weeyi Lim', '/weeyi.lim.1', 'Yimin Hsieh 邱明欣星巴克抽起來！'), ('陳信杰', '/profile.php?id=100001030551919', '星巴克抽起來!陳冠云黃勇誌'), ('洪振旂', '/alexpetertom', '星巴克抽起來! Jojo Chen 賴映竹'), ('張博涵', '/profile.php?id=100004785340097', '星巴克抽起來！Bryan Wang 葉孟昀'), ('陳欣妤', '/profile.php?id=100003493913557', '星巴克抽起來！黃欣儀闕千蘋'), ('黃郁茹', '/yuju.huang.756', '星巴克抽起來 楊岱瑾鐘曼綾'), ('許庭瑄', '/profile.php?id=100007970101021', '星巴克抽起來！ 曹瑩琇 楊博傑'), ('陳怡安', '/profile.php?id=100005487766723', '星巴克抽起來！蘇梅子 陳姿吟'), ('楊喬茵', '/profile.php?id=100000361832779', '星巴克抽起來! 葉明瑜孫靖媛'), ('徐毓', '/yhsu2', '星巴克抽起來！ 黃齡葦黃子庭'), ('Lala Chi', '/profile.php?id=100004356125645', '星巴克抽起來！陳信杰 林韋岑'), ('林亭', '/profile.php?id=100001936611960', '星巴克抽起來！ 金喆义 秦昌慈'), ('劉冠履', '/profile.php?id=100009986258453', '星巴克抽起來! 葉明瑜 孫靖媛'), ('Jia Yu Cheng', '/jiayu.cheng.5', '星巴克抽起來！胡馨文陳思諪'), ('高士昌', '/scott.kao.73', '星巴克抽起來！愷宸張蘇晏加'), ('林韋岑', '/profile.php?id=100000474291276', '星巴克抽起來！Lala Chi 林品萱'), ('Hoi Ping Goh', '/hoiping.goh', '星巴克抽起來！How Jia JianBeeKee Soon'), ('吳貞慧', '/profile.php?id=100002109118707', '星巴克抽起來！沈宛臻古孟君'), ('林余柔', '/yuzo8866', '星巴克抽起來！ 徐藝庭 傅有萱'), ('許佩琪', '/profile.php?id=100002511869301', '星巴克抽起來！楊雅筑Rita Yang'), ('How Jia Jian', '/jjhow17', '星巴克抽起來！Terry Lee Anis Wong'), ('愷宸張', '/profile.php?id=100003804896982', '星巴克抽起來！ 蘇晏加 Kulas Isin'), ('林芯妘', '/profile.php?id=100003728904355', '星巴克抽起來!潘羿辰 謝沅沅'), ('簡志軒', '/profile.php?id=100006113199773', '星巴克抽起來！許睿恩王慈昱'), ('張珮慈', '/yoolite','星巴克抽起來！ 彭湘晴 葉洧彤'), ('謝宜憫', '/profile.php?id=100004056912711', '星巴克抽起來！ 邱明欣 Chi Cheng'), ('周筠容', '/profile.php?id=100002395696030', '星巴克抽起來！ 丁紫芸 葉欣'), ('黃筠雅', '/profile.php?id=100002394356065', '星巴克抽起來!劉亭均何季蓉'), ('呂菱', '/arielluuu', '星巴克抽起來！ 黃心瑜 余沁容'), ('Khor Yi Ying', '/yiying1219', 'Tan Jou Ting Zyin Choy星巴克喝起來'), ('Angel Hsu', '/angel.hsu.3591', '星巴克抽起來！ 林亞嬛 Sherlyn Tania'), ('黃柏銘','/pming1226', '星巴克抽起來！黃千凱 （黃柾泰） Jing Wen'), ('王筠婷', '/profile.php?id=100003148398913', '星巴克抽起來！林佩萱郎曉言'), ('KaHei Chui', '/kahei.chui.5', '星巴克抽起來! 黃俊瑋Wong Hoi Ian'), ('盧昱均', '/yuchun.lu.5', '星巴克抽起來！ 林顯宗 盧昱佑'), ('Jing Yang', '/profile.php?id=100002124153086', '星巴克抽起來！ 李汶珈陳俞靜'), ('Nancy Lu','/lu.nancy.1', '星巴克抽起來！陳欐佳翁許方'), ('徐丰毓', '/edward.hsu.1217', '星巴克抽起來 吳知耕 陳昱愷'), ('何怡萱', '/chy880718', '星巴克抽起來！范馨之洪嘉君'), ('蔣其叡', '/ray.chiang.71', '星巴克抽起來！ShaoYu Hsu 楊品葦'), ('林旻', '/min.lin.50746', '星巴克抽起來! 王思尹李芷崴'), ('葉明諺', '/mingyen.yeh.5', '星巴克抽起來! 陳宴馨江美樺'), ('周祈鈞', '/profile.php?id=100009568613443', '星巴克抽起來！葉馨謝弦'), ('張皓鈞', '/profile.php?id=100000703535228', '星巴克抽起來！尹可親徐樹紅'), ('高鈺惠', '/ivy19900503', '星巴克抽起來！游子頤錢瑋'), ('謝巧琳', '/profile.php?id=100000494577498','星巴克抽起來！ Cheah Bei Yi黃雪瑜'), ('陳思諪', '/cwendy830818', '星巴克抽起來！ Jia Yu Cheng 胡馨文'), ('商婕瑜', '/jamie.shang.7', '星巴克抽起來！魏語欣 徐慕薇'), ('林孟璇', '/sherry.lin.896', '星巴克抽起來！ 鄧雅云 邱華奕'), ('王雅琳','/profile.php?id=100003541445645', '鄭佑瑩周葦星巴克抽起來！'), ('陳秀玲', '/profile.php?id=100009155445602', '星巴克抽起來！朱子涵 陳竫涵'), ('丁紫芸', '/uternalsummer', '星巴克抽起來 傅靖文 Hsun Hui Wang'), ('蘇宥婕', '/profile.php?id=100000442011179', '星巴克抽起來！何思妘張瑜君'), ('顧采薇', '/profile.php?id=100003126297107', '星巴克抽起來! Tan Jia Shin Daisy Ho'), ('陳彥穎', '/profile.php?id=100003811547336', '星巴克抽起來! 闕珮庭 林侑萱'), ('Shiyuan Sy', '/shiyuan.sy', '星巴克抽起來! Annabelle Choo 黃雪瑜'), ('徐郁淳', '/profile.php?id=100000915669304', '星巴克抽起來！陳芝儀林欣儒'), ('周韋伶', '/weiling.zhou2', '星巴克抽起來！Chou Yuhsun Tina Huang'), ('Annabelle Choo', '/annabellechooxl', '王妤如 鄭之毓 星巴克抽起來！'), ('羅亞帆', '/profile.php?id=100001466886832', '星巴克抽起來！ Jack Lee 張以臻'), ('黃妍婷', '/profile.php?id=100004162204699', '星巴克抽起來！陳琪 Athena Wong'), ('莊筑茵', '/profile.php?id=100000391609220', '星巴克抽起來葉致均林思妤'), ('李宜璉', '/profile.php?id=100002701763522', '星巴克抽起來！李雨璇 蔡之寧'), ('黃禹晴', '/profile.php?id=100006165698298', '星巴克抽起來！黃郁文黃琦軒'), ('余修誠', '/profile.php?id=1329335195', '星巴克抽起來！李佳蔚楊宗政'), ('彭佳文', '/rizu1867', '星巴克抽起來！ 范馨之劉蕙榕 （Camille Liu）'), ('陳昱愷', '/profile.php?id=100002324028159', '星巴克抽起來 劉誠新蘇致瑋 我也好想做問卷😫'), ('施吟儒', '/yinju.shih.3', 'Done李欣容謝佳樺'), ('蔡喜善', '/profile.php?id=100002436548346', '星巴克抽起來! 王品云 王意涵'), ('丁希彤', '/claireting714', '星巴克抽起來趙芳瑀羅倩如'), ('陳彥華', '/profile.php?id=100003491228030', '星巴克抽起來 梁永強 Yucheng James Chu'), ('蘇蘇', '/profile.php?id=100000350261939', '星巴克抽起來！陳孟緯郭令瑜'), ('周采瑄', '/profile.php?id=100002612675055', '星巴克抽起來！全書亞Hamber Chang'), ('全書亞', '/profile.php?id=100003672586531', '星巴克抽起來周采瑄 方韻雯'), ('思穎', '/zhong.ying.9', '吉他社星巴克抽起來！拯救期末大作戰哈哈哈鄭雅云蕭伊涵林莉雯林承懌邱致柔朱光愷Cindy Lin劉玉孝Alex Yin洪振傑丁顯翔徐子瑤還有好多人喔歡迎大家來抽獎！！'), ('劉玉孝', '/profile.php?id=100004019411436', '洪振傑 林承懌感謝我ㄅ\n星巴克抽起來'), ('葉洧彤', '/ye.zi.980', '胡馨尹吳昱弘星巴克抽起來！'), ('邱致柔', '/amy.chiu.125', '朱易宣張文姿填問卷救室友思穎星巴克抽起來！'), ('楊恭豪', '/sun.how.71', '星巴克抽起來！ 彭文亭 （WenTing Peng） 吳柏穎'), ('Hui Yee', '/Huiyee1998', '星巴克抽起來！Zyin ChoyRuo Thung'), ('Tan Margin', '/tan.margin.7', '星巴克抽起來！Duyen Vu Đào Anh Minh'), ('洪振傑', '/profile.php?id=100000400612298', '李優群 林緯程 星巴克抽起來！'), ('Yi Qi Goh', '/yiqi.gohelf', '星巴克抽起來！Hui Yee Hoi Ping Goh'), ('袁咏仪', '/jenny.g.jenny.3', '星巴克抽起來！BeeKee Soon Jo An'), ('Stacie Hsiao', '/stacie.hsiao', '紀妤岫施泯嘉星巴克抽起來！'), ('紀妤岫', '/rumvu', '星巴克抽起來！Stacie Hsiao邱聖雅'), ('Ruo Thung', '/ruo.tong', 'Eu Jing Fei Hoi Ping Goh星巴克抽起來！'), ('楊晏婷', '/pa.zou.73', '黃顗蓁 Sara Wu 星巴克抽起來'), ('陳彥慈', '/profile.php?id=100000586324433', '星巴克抽起來！劉北辰馬允中'), ('蔡佳茜', '/profile.php?id=100007083107521', '星巴克抽起來 Eric Ni 劉子琪'), ('梁艦尤', '/profile.php?id=100002023988441', '林彥廷 李治融'), ('林宜萱', '/sandylin.lin.92', '星巴克抽起來！黃大瑋 謝孟慈'), ('劉品婕', '/profile.php?id=100001432904325', '星巴克抽起來! 江佩芸何硯涵'), ('高巧玲', '/linda.kao.969', '星巴克抽起來!劉繡慈王珉婕'), ('劉繡慈', '/profile.php?id=100004122428050', '星巴克抽起來！高巧玲 黃冠穎'), ('詹珮渝', '/carol011629', '星巴克抽起來！ 李承樺 Tsung Chen'), ('吳智穎', '/aaronlove1211', '星巴克抽起來！張雅涵 張馨文'), ('陳伯霏', '/profile.php?id=100001309787880', '星巴克抽起來！ Godest Wang 黃品瑄'), ('黃品瑄', '/cheynehuang', '星巴克抽起來! 游皓鈞林勉'), ('蕭子勤', '/profile.php?id=100000359172345', '星巴克抽起來！ 宋弘軒張郁怜'), ('陳巧蓉', '/ysesst95182', '星巴克抽起來！Bryson Caw 朱尹亘'), ('陳品婕', '/jessicayoya', '星巴克抽起來！Jacky Huang李梓翔'), ('鄭淨伃', '/profile.php?id=100006362441315', '徐維勵 施瑀嫺星巴克抽起來！'), ('王偉力', '/godest.wang', '星巴克抽起來！ 于其弘 周俐廷'), ('Shu Lian', '/shu.lian.5', 'Hong DaTan Jia Shin 星巴克抽起來！'), ('Tan Jia Shin', '/tan.jiashin', '星巴克抽起來！ 卓桐 鍾詠倫'), ('王泓詠', '/profile.php?id=100001694300374', '星巴克抽起來 林韋岑 劉紘與'), ('李昀', '/profile.php?id=100003402272483', '星巴克抽起來！ 陳昕 張珈漩'), ('張芳瑄', '/1997jennie', '星巴克抽起來！ 許東溢 鮑威宇'), ('黃語萱', '/profile.php?id=100002916605910', '黃浩瑀 陳宜涵 星巴克抽起來!'), ('范瑜庭', '/tina1226tina', '陳奐君 吳念蓁 星巴克抽起來！'), ('吳念蓁', '/profile.php?id=100000594528788', '古欣璇張榛芸星巴克抽起來！'), ('李鎧碩', '/ken.lee.1884', '星巴克抽起來！馬愷辰洪尹謙'), ('高慧君', '/profile.php?id=100013876578152', '陳昱臻 王懿柔 星巴克抽起來！'), ('蔡智伃', '/profile.php?id=100000369982431', '黃如霜朱翌甄星巴克抽起來！'), ('江芳瑜', '/profile.php?id=100002598245297', '星巴克抽起來！郭沛萱 陳品璇'), ('GloryLiang', '/glory.liang.9', '星巴克抽起來！許綺珊 黃郁茹'), ('愷欣', '/AdelineTin1205', '星巴克抽起來！ 鍾詠倫 Yong Kai Wen'), ('邱明欣', '/profile.php?id=100003615537778', '星巴克抽起來!Yimin HsiehChi Cheng'), ('林欣儒', '/profile.php?id=100003302436199', '星巴克抽起來！郭嘉茵 陳韋君'), ('陳奕君', '/199526pig', '蘇毓涵徐若庭星巴克抽起來！'), ('吳恩庭', '/enting.wu1', '星巴克抽起來！ 顏于傑吳恩庭'), ('蘇毓涵', '/katie.sue.940', '陳奕君徐若庭星巴克抽起來！'), ('李昱萱', '/profile.php?id=100002037107245', '星巴克抽起來！ 魏家琳 關雅文 （Maggie Guan）'), ('羅歆瑜', '/pluviophilerusty', '星巴克抽起來！ 張博涵 （Teresa Chang）王桂芳'), ('田佳欣', '/HaHaApril999', '郭子禎 湯芸藻 星巴克抽起來！'), ('陳潔慧', '/profile.php?id=100003653177937', 'Paula Liao 謝羽蓁星巴克抽起來！'), ('王桂芳', '/profile.php?id=100002846095042', '星巴克抽起來！張博涵 羅歆瑜'), ('張雅淇', '/vicky.chang.1048', '星巴克抽起來！林沛瑩 許家菱')]
    
    if 'csv_options' in req:
        options = req['csv_options']
        index = 0 if options['type']=="name" else 1
        legal_list = csv_filter.run(options['data'], index, legal_list)

    legal_list = [ {'name': d[0], 'url': d[1], 'comment': d[2]} for d in legal_list ]   # cast to json
    print(legal_list)
    return Response(json.dumps(legal_list),  mimetype='application/json')

@app.route('/lottery', methods=['POST'])
def get_lottery():
    req = request.get_json()
    try:
        winner = lottery.run(req['prize'], req['legal_list'])
        return Response(json.dumps(winner),  mimetype='application/json')
    except KeyError:
        return "請先爬取中獎名單！", 400

@app.route('/test')
def apptest():
    return render_template('test.html')

if __name__ == "__main__":
    app.config['ENV'] = "development"
    app.config['DEBUG'] = True
    app.run(port=3000)