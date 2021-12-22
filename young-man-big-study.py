import requests
from lxml import etree
import os, sys


class BigStudy(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'Connection': 'keep-alive',
            'Host': 'news.cyol.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
        }
        self.list = ['第十二季第十期：加强中华儿女大团结', '第十二季第九期：习近平生态文明思想的生动实践', '青年大学习特辑：学习党的十九届六中全会精神', '第十二季第八期：进行具有许多新的历史特点的伟大斗争', '第十二季第七期：归根到底是因为马克思主义行', '第十二季第六期：江山就是人民，人民就是江山', '第十二季第五期：办好中国的事情，关键在党', '第十二季第四期：伟大的建党精神', '第十二季第三期：在中华大地上全面建成小康社会', '第十二季第二期：中华民族几千年历史上最恢宏的史诗', '第十二季第一期：新时代是奋斗者的时代', '第十一季第二十期：不负时代，不负韶华，不负党和人民的殷切期望！', '第十一季第十九期：迈向中华民族伟大复兴的关键一步', '第十一季第十八期：踏平坎坷成大道，斗罢艰险又出发', '第十一季第十七期：打铁必须自身硬', '青年大学习特辑：学习习近平总书记在庆祝中国共产党成立100周年大会上的重要讲话', '第十一季第十五期：中华民族近代以来最伟大的梦想', '第十一季第十四期：在新形势下坚持和发展中国特色社会主义', '第十一季第十三期：中国特色社会主义阔步向前', '第十一季第十二期：伟大的历史转折', '第十一季第十一期：党对中国社会主义建设道路的探索', '第十一季第十期：社会主义好', '第十一季第九期：抗美援朝 保家卫国', '第十一季第八期：中国人民从此站立起来了', '第十一季第七期：一切为了新中国，一切为了人民', '第十一季第六期：加强党的建设，开展整风运动', '第十一季第五期：全民族抗战的中流砥柱', '第十一季第四期：伟大的长征', '第十一季第二期：打倒列强除军阀', '第十一季第一期：开天辟地的大事变', '第十季第十期：人类历史上的伟大壮举', '第十季第九期：脱贫致富终究要靠贫困群众用自己的辛勤劳动来实现', '第十季第八期：坚持从严要求 促进真抓实干', '第十季第七期：绿水青山就是金山银山', '第十季第六期：致富不致富，关键看干部', '第十季特辑：最鲜活的现实明证，最生动的实践写照']

    def getTitleList(self):
        self.list = []
        for page in range(1,3):
            url = "http://news.cyol.com/gb/channels/vrGlAKDl/index.html"
            if page != 1:
                url = "http://news.cyol.com/gb/channels/vrGlAKDl/index_"+str(page)+".html"
            response = self.session.get(url=url)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                html = etree.HTML(response.text)
                for i in range(1, 30):
                    result = html.xpath("//li[" + str(i) + "]/h3/a/text()")
                    sub_url = html.xpath("//li[" + str(i) + "]/h3/a/@href")
                    if len(result) != 0:
                        sub_response = self.session.get(url=sub_url[0])
                        sub_response.encoding = 'utf-8'
                        sub_html = etree.HTML(sub_response.text)
                        pre_titles = sub_html.xpath("/html/head/title/text()")
                        if len(pre_titles) != 0:
                            pre_title = pre_titles[0].split("”")
                            if len(pre_title) == 2:
                                pre_title = pre_title[1]
                                if pre_title == "特辑":
                                    pre_title = "青年大学习" + pre_title
                                title = pre_title + "：" + result[0].split("：")[1]
                                self.list.append(title)
                                print(title)
                    else:
                        break
            else:
                break
        print(self.list)

    def generateHTML(self):
        head = open('head.txt', 'r',encoding='utf-8')
        tail = open('tail.txt', 'r',encoding='utf-8')
        jifen_file = open('jifen.txt', 'r', encoding='utf-8')
        html = open("jifen.html", 'w',encoding="utf-8")
        html.write(head.read()+"\n")
        html.write("    <div class=\"integral_box _shadow_box\">\n      <div class=\"btn link\">积分说明</div>\n      ")
        jifen = jifen_file.read()
        html.write(jifen)
        html.write("<small>积分</small>   <!-- 积分数量 -->\n    </div>\n    <div class=\"title\"><span>积分详情</span></div>\n    <div class=\"list\">\n")
        for i in range(0,len(self.list)):
            html.write("      <div class=\"item self_clear\">\n        <div class=\"r\">\n          +1分\n        </div>\n        <span class=\"ovh_1\">\n          学习　")
            html.write(self.list[i]+"\n")
            html.write("        </span>\n      </div>\n")
        html.write("      <div class=\"no_more\">—　正在加载　—</div>\n    </div>\n")
        html.write(tail.read())
        html.close()
        tail.close()
        head.close()
        jifen_file.close()
        jifen_file = open('jifen.txt', 'w', encoding='utf-8')
        jifen_file.write(str(int(jifen)+1))
        jifen_file.close()


if __name__ == "__main__":
    bigStudy = BigStudy()
    # bigStudy.getTitleList()
    bigStudy.generateHTML()

