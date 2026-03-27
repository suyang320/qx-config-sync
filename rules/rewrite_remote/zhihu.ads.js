/***********************************

知乎净化助手2.0[墨鱼版]

https://t.me/ddgksf2021


[rewrite_local]

# > 知乎_拦截DNS解析@blackmatrix7
^https?:\/\/118\.89\.204\.198 url reject-200
^https?:\/\/103\.41\.167\.237 url reject-200
^https?:\/\/2402:4e00:1200:ed00:0:9089:6dac:96b6 url reject-200

# > 知乎_屏蔽远程配置@blackmatrix7
^https?:\/\/api\.zhihu\.com\/ab\/api\/v1\/products\/zhihu\/platforms\/ios\/config url reject-200

# > 知乎_我的页面开通会员CARD@ddgksf2013
^https?:\/\/api\.zhihu\.com\/unlimited/go/my_card url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_开屏广告@ddgksf2013
^https?:\/\/api\.zhihu\.com\/commercial_api.*launch_v2 url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_品牌提问广告@blackmatrix7
^https?:\/\/api\.zhihu\.com\/brand\/question\/\d+/card\? url reject-dict
^https?:\/\/www\.zhihu\.com\/api\/v\d+\/brand\/question/\d+/card\? url reject-dict

# > 知乎_去除底部标签页关注人角标@blackmatrix7
^https?:\/\/api\.zhihu\.com\/moments\/tab_v2 url reject-dict

# > 知乎_去除消息通知角标@blackmatrix7
^https?:\/\/api\.zhihu\.com\/(notifications\/v\d\/count) url reject-dict

# > 知乎_拦截回答下的卡片广告@blackmatrix7
^https?:\/\/www\.zhihu\.com\/api\/v\d\/answers\/\d+\/recommendations url reject-dict

# > 知乎_拦截应用内弹窗@blackmatrix7
^https?:\/\/api\.zhihu\.com\/me\/guides url reject-dict

# > 知乎_去除关注页最常访问@blackmatrix7
^https?:\/\/api\.zhihu\.com\/moments\/recent url reject-dict

# > 知乎_拦截推荐页顶部广告@blackmatrix7
^https?:\/\/api\.zhihu\.com\/api\/v4\/ecom_data\/config url reject-dict

# > 知乎_底栏加号的广告@blackmatrix7
^https?:\/\/api\.zhihu\.com\/content-distribution-core\/bubble\/common\/settings url reject-dict

# > 知乎_推荐页搜索栏左侧图标@blackmatrix7
^https?:\/\/api\.zhihu\.com\/feed\/render\/revisit\/current_reading url reject-dict

# > 知乎_疑似推荐页内容更新红点@blackmatrix7
^https?:\/\/api\.zhihu\.com\/feed\/render\/revisit\/tag_config url reject-dict

# > 知乎_暂不清楚作用@blackmatrix7
^https?:\/\/.*zhihu\.com\/commercial_api url reject-dict
^https?:\/\/.*zhihu\.com\/ad-style-service\/request url reject

# > 知乎_用户信息@ddgksf2013
^https?:\/\/api\.zhihu\.com\/people/self$ url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_文章页去除底部广告@blackmatrix7
^https?:\/\/www\.zhihu\.com\/api\/v\d\/articles\/\d+\/recommendation url reject-dict

# > 知乎_推荐信息流去广告@ddgksf2013
^https?:\/\/api\.zhihu\.com\/topstory\/recommend url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_搜索页去除推广@ddgksf2013
^https?:\/\/api\.zhihu\.com\/search\/preset_words url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_猜你想搜下面条目['猜你想搜'四个字无法去除]@ddgksf2013
^https?:\/\/api\.zhihu\.com\/search\/recommend_query url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_删除会员页面会员购@ddgksf2013
^https?:\/\/api\.zhihu\.com\/bazaar\/vip_tab\/tabs url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_热榜页去除广告@ddgksf2013
^https?:\/\/api\.zhihu\.com\/v2\/topstory\/hot-lists url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_我的页面下方内容@ddgksf2013
^https?:\/\/api\.zhihu\.com\/api\/v4\/profile\/cards url reject-dict

# > 知乎_会员页面顶部处理@ddgksf2013
^https?:\/\/api\.zhihu\.com\/bazaar\/vip_tab\/header url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_热榜页去除直播@ddgksf2013
^https?:\/\/api\.zhihu\.com\/drama\/hot-drama-list url reject

# > 知乎_回答信息流去广告@ddgksf2013
^https?:\/\/api\.zhihu\.com\/next-data url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js
^https?:\/\/api\.zhihu\.com\/next-render url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_回答页面顶部推广@ddgksf2013
^https?:\/\/www\.zhihu\.com\/api\/v4\/topics\/rank_list\/question\/\d+\/related url reject

# > 知乎_问题回答列表@ddgksf2013
^https?:\/\/api\.zhihu\.com\/(v4\/)?questions\/\d+\/feeds url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_回答内容优化@ddgksf2013
^https?:\/\/www\.zhihu\.com\/appview\/v2\/answer\/ url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_会员页面购物处理@ddgksf2013
^https?:\/\/api\.zhihu\.com\/bazaar\/vip_tab\/modules url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_修改用户盐值@blackmatrix7
^https?:\/\/api\.zhihu\.com\/user-credit\/basis url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_消息页@blackmatrix7
^https?:\/\/api\.zhihu\.com\/notifications\/v3\/(message|timeline\/entry\/system_message) url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_首页右下角悬浮窗@blackmatrix7
^https?:\/\/api\.zhihu\.com\/commercial_api\/app_float_layer url reject

# > 知乎_关注页面去除今日话题和为您推荐@ddgksf2013
^https?:\/\/api\.zhihu\.com\/moments_v3 url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

# > 知乎_回答页面相关搜索词@ddgksf2013
^https?:\/\/www\.zhihu\.com\/api\/v4\/search\/related_queries\/answer\/ url reject-dict

# > 知乎_广告请求@ddgksf2013
^http:\/\/[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){1,4}(:\d+)?\/v2\/resolv url reject-200

# > 知乎_首页左侧图标@ddgksf2013
^https?:\/\/api\.zhihu\.com\/root\/window url reject-dict

# > 知乎_我的页面底部@ddgksf2013
^https?:\/\/www\.zhihu\.com\/appview\/v\d\/zhmore url reject-200

# > 知乎_回答页底部相关圈子及搜索词@ddgksf2013
^https?:\/\/.*zhihu.com\/(answers|articles)\/v\d url jsonjq-response-body '.third_business |= del(.related_queries, .ring)'

# > 知乎_搜索发现@ddgksf2013
https://api.zhihu.com/search/hot_search url script-response-body https://ddgksf2013.top/scripts/zhihu.ads.js

[mitm] 

hostname = 118.89.204.198,103.41.167.237,2402:4e00:1200:ed00:0:9089:6dac:96b6,www.zhihu.com,api.zhihu.com,page-info.zhihu.com,zhuanlan.zhihu.com,appcloud2.zhihu.com,m-cloud.zhihu.com,103.41.167.236,103.41.167.234,103.41.167.235,103.41.167.226


***********************************/






const version = 'V1.0.75';


var _0xodA='jsjiami.com.v7';function _0x29a9(){const _0x48cfa5=(function(){return[_0xodA,'JNLjpsujeiFuaxmFiV.cOSVomTG.FHvnFp7XgRnt==','WP/dVGG','mWNdUmklsMpdGhnNWRhdGSobW63dS8kFc8k5ja','W7aKecPycbzQW7VdGJ3cN8kEaSotWRDQWPVcOdC','W70JcYzE','WOSGFG','5ysq6lA75lI9B8k/WQ9TCmki5l256lsn5yws5AYN','ASoeWRrE','iq7dPCk8tcBdIw5WW7tdSCozW6VdOSkE','uKxdMfW','W4Oxj2y','l8keWQ0','WO4vm8oRfSkAmmoQWRq','WOT1ku3dM8oqWRv8wq','t0pdMuJcOq4','kmk3W4NdImoFjSo/Af8Irq','cILLm8kvg8oxW6S','lwxcL8kOACoTWQr4W4BcU8oAWO0okSks','BrlcPwhcIeWhFdFdR8kwbq','g8kbuw9K','W7K4cYTdvvaJW7q','aCkUyN1IWO3dH8o/WOyGveC','C8ksjSogWRyU','W5FcUSkLW7m','W4FcVSkIW6y','WRhdQrFdPCo+WO7cSe/cNCo0W7pcRSkD','vCoAm2K','WRxdPqddR8oK','5OUP55Qe55QB6yc35l615zo6','WOpdSb3dHmor','a8kfWP/cHSovW7e','a8oVW74','fIOfca','WOGpm8oNgCkzbSoVWQiFWRv4','tCo8WPNdRuqWWRGHbeFdG8olW7aCuYVcIG','FSksoCogWRGSWPlcOmkeWO7cRW','55w05lIqzZKTzSkNfos8IUI3T+whGowSNq','WOXLoeO','v0/dG0pcSa','aSoKW6iC','WRVdQbG','mCoTW7e','qmoaDCkyWR3dLq9wWPqGW5uVWRzF','teZdHvxcINjtW7GTWR44WPldQ8kUEGzyfsPo','W54aqdNdPd0MW7PXDWu','trNcONupW47dGar+W4qwWPysjmkpWPSFhmoNW6tcKG','WQiuWPKvWQVdT8olW6v1arpcSgC2W4TbW7G8','rCoEnhW','WQFdRrddQW','ArNdNmoK','smoNWPS','l8opzSkyWQ4SWOpcSmktWP8','W44BjgS','5AEs6lst5lQw','W4pcOH3cJMXLW5/dI20bW60SW58vWRdcL8ot','55E75lUfDZldIJqGW5pKVlVOTQVLHQFLR7u','atCn','xbRdMZu','ACkylmoF','WOSOySonha','j2hcKCkHy8o2','W4dcR8kJW7SidmoMW6pcGq','W5hcRSkLW6yjbCoqW7hcNCoAiG','r3dcVbVdG3FcMq','WRT5sYrmxfyXW6K','aZFdQ8oJWQq/WOrAlWNcML1oarVcQmko','5P+P6k235RES5OoL','WQldTrm','f0jJFsGgaLxcPW','qKVdMfZcKXCpWRq0WQuT','x8ogAmkcWQNcGumCWR0/WPC'].concat((function(){return['EsT5jG','5ysC6ykT5REP5OcE5BwM6k6q','W5bYx3i5kq8','aCknWOFcKW','WOKymCoN','oxBcJmkK','WO5Po2hdHSomWRP9','xCoCW4xdHCkgWReOW5JcICkwgCo1','mxJcNW','W651qCka','W5xcPGRcGa','WO0am8oXhq','ct7dSmo4WRq','sSobCG','WPWfhSoRfSkBnG','c8kKya','CSofWRngW5pcP8kxc8ovW5WEWQldPhFdOmkiW6hdNr8JkCkvWQ4RW4KWWQ7dMCoPWQGReNFcRJiYdmkOW5lcVCkmtJ4argJdTMtdNZWOq8opW7aSfLCkW5GmW5/cHCkxW4m','W4vVCh4','W4FcRHRcHg4','l8opWRvZbSoivaG','kgxcLa','W4OljhC','wmoDAmkeWQFcGq','WOWMW6ZdTSkdafVcUCkkDSoNoSkfj1FcNhC','BI/dI8oZp8kUWQHMW6pcG8oZWPW','kWFdOSkXvvNdLwr8WQ0','w8oWWPldLMSMWRuJgvhdHCoG','dSkor0n1nq','hCkJBNfiW47dHSo+WOySxfOmpfrjW5mUiq','W7O+hdfirMyYW6ldMsNdGW','WQWuWP8pWRNdSCoc','dmo1W7Srz8oQrJlcRatdLmoSW7j5','W5ymWPZcPYq9W7u/DwPUyG','W75XrSkv','W4FcRG7cVMHRW5xdIW','t8oACa','W5iBWORcOa','dmo1W7Srz8oQrJlcTWZdLSkOW7P0W6hcTmkcW7pcIa','w8oWWPldLMSKWR47ceBdNW','eL91CsK','W5LIDgSKDu/dOmkcbSkgW7pdUgZdGmoVAdFcUN3dH8onW7e','FeBcPmoTCSoXoq','W7/cQ0xcTw1CWRCDW47dNSkDeCke','trNcONupW47dHH9RW6GhWOmVC8knWOyFgG','W6XXumkfE2P2WQmUavldOG','6iAk5AUo5l2B','WQVdRrFdHCo8WPlcG1JcRCoWW6/cRmkmua','W5iMWOpdNG','rKxdNK7cMG','b1L8EsKpnfdcV8kvWQ8','b8koDdWKj8okuxNcRdhdVq','BSkjjSocWRKLWQtcPCkC','WOKemSo2','kw7cImkG','WQfjWR3dUSkqi0RdGuVdQa','wCo0WOpdKW','cIVdSmoIWR94WOnzlG','WQZdVXpdPduZW7qx','bmkKANrsWOddT8oYWPm3xG','xSo6WPRdN1SRWOuUdeBdJW','W4VcRXFcIxqOW4VdKgWTW6GWW5ujWQO','E1RcPCo6Da','5l295AAc77+J55+/5lIr776Q','wb7dMJldUq','tSonzmke','WPFdVGxdO8oLWPxcVu0','WOddS0/dMtrLW7hdN1egW7m','WQddI8kUhCk+DYxdVSkY','pqNdVSkrwgxdIq','rKJdK3dcOru','FIDRmfpcKMBdS1m','DqJdM8oGWO3dPs8/WRpcLbJdL2pcSg5zr8oUW6VcKSk/FCkkW4xdKmo9FZeUW7i/pwddGCkgW6TwdmotW4iHWPxdQHRdG8kZW59zseKvWQNdLuNdVwlcL8kUvqlcIW4'].concat((function(){return['rKJdG13cTaHwW6RcP8kwW4NcHq','w8o6WOxdT1uMWRi','W4KkxIa','k8kbW79AW5RdKCo6sCol','FvlcS8oSFG','5P6U55+t5P+N55MV','WRrqWQFdRCkD','e8kfWOpcRCoeW6OY','eL9HsY8pdvW','ftRdRmoSWQv3','gmkuuxvViv/dI8oK','hCkJBNfiW47dMSo0WPeQv14km0r/W401n8klWQ0','p8koWRxdUHa','wX7cRa','5BEe5BYK6yk2','57cd6ygM5lY35zcm5yso5A+Q','Aa7dGW','W6ldSSkKemkBvGG','DCkjimoBWQr4W6ldRmkvWPxcQbdcQmk9ySo+euxcHGddK03cGdLiWOFcKmoEymkGWPhcM8oKnhJdKsuKDLGTkgJcHCkKiItdJ8oDbvmlnrq7WR3dTmkjWOxdPCk6zq','nHqkmsFcPvfXcq','WQyuWOO','xNBcKae','s8otlMbOmCo6xwlcGdhdHr8McCogWOSZmtC','WQBdRGddVsHwWQ9lW5ZdJSk8uSoTACk9sCopWP8UgHhdPSk9WQGuvMpcUSk5a8oFsmocW4HIW5ucWOamWR4hDSoQcsdcICoPWPCdneTHcmkiW682AwPaW6SQW75xya','5yA95lY/5yYK','pGVdSSkPiSkJl8o3WOKfWOue','W6KyW6xcQmoktLtdQ1ldNuDp','FHpdGCoKWPVcSxq','W5ukWOVcVs8UW4mUyW','vgVcIGhdKZBcImo/yCkaW7xcRxhdM0D7W7q','WPiVW7hdVW','WP8ojCo7','W5ibma','mXldUmkKsJZcJI50WRddVSkbWRBdRmkfc8kXmmkaW7JcHNWpbCknrCkEW5ygaYSmuCk9orrPeSogW77dLKNdQ8kLE8o/nrRcT156pSk1z8oNWQeTBghcLSkPzNfP','W7LGr8kisM5WWQSJ','WQfDWQddTW','W4pdItVdJCkVxmke','WPXHp18','dI0igCoHs1pdO2yHbmk1tq','WQvrWQpdUG','A8kKW7a','ru/dM1VcSbq','oxlcJmkKB8o1WPjJW4hcKmotWPa','ctfVhmk6aSoeW74yjaxdK8kzW59IkSkhWRVcUsi','ldhdL8o0WRxcMuq','q8oEjgDWFmoPwNBcGdddLXH0pSoaWOSLmbOkWRNcR1m','lfpdTchdLqapFW3dSCk7eq','WRxdKmkUf8k1tZVdT8k5oSot','W7aKecPyeLeQW7NdTd7dLCkpbCocWRW','rmojkW','W5D/Bg8Ypq','dSk4wg9uWP4','mGy1qCkIkG','EWxcPxBcSLS3zsZdUmkCaG','BmoyWRDPW4NdS8oEsW','W4GDqq','5OIR55IS55Um6yo55l+s5zk3','W7ZcQI7dPaipW4WU','wqRdJtpdTvLJ','ACkyj8oF','F8kqWOTJ','WRXjWQFdVmku','W5jKzx8+oZ/cRCkxw8kcW6u','WOCjkmoQdCoDkCoPWQiAWRDP','W4VcRXFcIxqOW5VdLxKOW7u8W404WQ/dGmo/W7u9W6xdRwBcTa','ed16mmkV','A8ocW7dcSetcNmoeWQ/cJ8oaDW','gcOg','vLtdMW','fCknWOhcGCov'];}()));}()));}());_0x29a9=function(){return _0x48cfa5;};return _0x29a9();};const _0x23a96a=_0x2c12;function _0x2c12(_0x14ee17,_0x53c4fe){const _0x29a94c=_0x29a9();return _0x2c12=function(_0x2c1207,_0x5dc5e5){_0x2c1207=_0x2c1207-0x65;let _0x57412d=_0x29a94c[_0x2c1207];if(_0x2c12['HCEtwO']===undefined){var _0x119ce8=function(_0x462a17){const _0x3d1bae='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';let _0x516142='',_0x2265de='';for(let _0x2cbd46=0x0,_0x445e6b,_0x2852e5,_0x3ebb9b=0x0;_0x2852e5=_0x462a17['charAt'](_0x3ebb9b++);~_0x2852e5&&(_0x445e6b=_0x2cbd46%0x4?_0x445e6b*0x40+_0x2852e5:_0x2852e5,_0x2cbd46++%0x4)?_0x516142+=String['fromCharCode'](0xff&_0x445e6b>>(-0x2*_0x2cbd46&0x6)):0x0){_0x2852e5=_0x3d1bae['indexOf'](_0x2852e5);}for(let _0x5d7dd6=0x0,_0x33ad3e=_0x516142['length'];_0x5d7dd6<_0x33ad3e;_0x5d7dd6++){_0x2265de+='%'+('00'+_0x516142['charCodeAt'](_0x5d7dd6)['toString'](0x10))['slice'](-0x2);}return decodeURIComponent(_0x2265de);};const _0x591f16=function(_0x2b269d,_0x2b6404){let _0x75584a=[],_0x4416b1=0x0,_0x22a7af,_0x293c70='';_0x2b269d=_0x119ce8(_0x2b269d);let _0x39a48d;for(_0x39a48d=0x0;_0x39a48d<0x100;_0x39a48d++){_0x75584a[_0x39a48d]=_0x39a48d;}for(_0x39a48d=0x0;_0x39a48d<0x100;_0x39a48d++){_0x4416b1=(_0x4416b1+_0x75584a[_0x39a48d]+_0x2b6404['charCodeAt'](_0x39a48d%_0x2b6404['length']))%0x100,_0x22a7af=_0x75584a[_0x39a48d],_0x75584a[_0x39a48d]=_0x75584a[_0x4416b1],_0x75584a[_0x4416b1]=_0x22a7af;}_0x39a48d=0x0,_0x4416b1=0x0;for(let _0x5c108f=0x0;_0x5c108f<_0x2b269d['length'];_0x5c108f++){_0x39a48d=(_0x39a48d+0x1)%0x100,_0x4416b1=(_0x4416b1+_0x75584a[_0x39a48d])%0x100,_0x22a7af=_0x75584a[_0x39a48d],_0x75584a[_0x39a48d]=_0x75584a[_0x4416b1],_0x75584a[_0x4416b1]=_0x22a7af,_0x293c70+=String['fromCharCode'](_0x2b269d['charCodeAt'](_0x5c108f)^_0x75584a[(_0x75584a[_0x39a48d]+_0x75584a[_0x4416b1])%0x100]);}return _0x293c70;};_0x2c12['DwuioV']=_0x591f16,_0x14ee17=arguments,_0x2c12['HCEtwO']=!![];}const _0x1ccb59=_0x29a94c[0x0],_0xa88968=_0x2c1207+_0x1ccb59,_0x5e627c=_0x14ee17[_0xa88968];return!_0x5e627c?(_0x2c12['dRmFIX']===undefined&&(_0x2c12['dRmFIX']=!![]),_0x57412d=_0x2c12['DwuioV'](_0x57412d,_0x5dc5e5),_0x14ee17[_0xa88968]=_0x57412d):_0x57412d=_0x5e627c,_0x57412d;},_0x2c12(_0x14ee17,_0x53c4fe);}(function(_0x57d889,_0x46494f,_0x5754cb,_0x1bded8,_0x266c93,_0x29ae6c,_0x2ded45){return _0x57d889=_0x57d889>>0x8,_0x29ae6c='hs',_0x2ded45='hs',function(_0x27d1c4,_0x1d78ee,_0x2873e7,_0x4fa2f8,_0x3c58f6){const _0x50b3a7=_0x2c12;_0x4fa2f8='tfi',_0x29ae6c=_0x4fa2f8+_0x29ae6c,_0x3c58f6='up',_0x2ded45+=_0x3c58f6,_0x29ae6c=_0x2873e7(_0x29ae6c),_0x2ded45=_0x2873e7(_0x2ded45),_0x2873e7=0x0;const _0xb93336=_0x27d1c4();while(!![]&&--_0x1bded8+_0x1d78ee){try{_0x4fa2f8=parseInt(_0x50b3a7(0x73,'bm)*'))/0x1*(parseInt(_0x50b3a7(0x90,'yJF9'))/0x2)+parseInt(_0x50b3a7(0x106,'#@I]'))/0x3+-parseInt(_0x50b3a7(0x75,'&)bz'))/0x4*(-parseInt(_0x50b3a7(0x130,'IkWc'))/0x5)+-parseInt(_0x50b3a7(0x120,'V9bb'))/0x6+-parseInt(_0x50b3a7(0x118,'JZ0B'))/0x7+-parseInt(_0x50b3a7(0xe7,'40vx'))/0x8*(parseInt(_0x50b3a7(0xda,'vnPQ'))/0x9)+-parseInt(_0x50b3a7(0x101,')zTp'))/0xa*(-parseInt(_0x50b3a7(0xf5,'HV(D'))/0xb);}catch(_0x485bc8){_0x4fa2f8=_0x2873e7;}finally{_0x3c58f6=_0xb93336[_0x29ae6c]();if(_0x57d889<=_0x1bded8)_0x2873e7?_0x266c93?_0x4fa2f8=_0x3c58f6:_0x266c93=_0x3c58f6:_0x2873e7=_0x3c58f6;else{if(_0x2873e7==_0x266c93['replace'](/[TuNRxLpVgeOJSnGXtFH=]/g,'')){if(_0x4fa2f8===_0x1d78ee){_0xb93336['un'+_0x29ae6c](_0x3c58f6);break;}_0xb93336[_0x2ded45](_0x3c58f6);}}}}}(_0x5754cb,_0x46494f,function(_0x293389,_0x490d0a,_0x50a72a,_0x1add4a,_0x500729,_0x2ce7f8,_0x47ed3e){return _0x490d0a='\x73\x70\x6c\x69\x74',_0x293389=arguments[0x0],_0x293389=_0x293389[_0x490d0a](''),_0x50a72a='\x72\x65\x76\x65\x72\x73\x65',_0x293389=_0x293389[_0x50a72a]('\x76'),_0x1add4a='\x6a\x6f\x69\x6e',(0x19e141,_0x293389[_0x1add4a](''));});}(0xc300,0x23646,_0x29a9,0xc5),_0x29a9)&&(_0xodA=`\xd7d`);let body=$response[_0x23a96a(0x9e,')zTp')];if(body){switch(!![]){case/appview\/v2\/answer/[_0x23a96a(0xbf,'hGsP')]($request[_0x23a96a(0xd9,'u!lE')]):try{}catch(_0x4179de){console[_0x23a96a(0xa8,'XsCu')](_0x23a96a(0xa2,'IkWc')+_0x4179de);}break;case/com\/moments_v3/['test']($request['url']):try{let obj=JSON[_0x23a96a(0xe2,'7]YL')](body);obj[_0x23a96a(0x87,'^7kn')]=obj[_0x23a96a(0xc1,'V9bb')][_0x23a96a(0x8b,'4H%x')](_0x100305=>!(_0x100305[_0x23a96a(0xb1,'bp*n')]==_0x23a96a(0xc9,'u!lE')||_0x100305[_0x23a96a(0xee,'F9FM')]==_0x23a96a(0x8f,'V9bb'))),body=JSON['stringify'](obj);}catch(_0x1e40d6){console['log'](_0x23a96a(0x7f,'G3Lk')+_0x1e40d6);}break;case/notifications\/v3/['test']($request[_0x23a96a(0x72,'nU0!')]):try{let obj=JSON[_0x23a96a(0xa3,'zuM@')](body),newItems=[];for(let item of obj[_0x23a96a(0xf7,'Rq%g')]){if(item['detail_title']==='官方帐号消息'){let unread_count=item[_0x23a96a(0xc8,'n@Xp')];unread_count>0x0?item[_0x23a96a(0x7d,'nU0!')][_0x23a96a(0x12e,'MXn%')]=_0x23a96a(0xe9,'snFt')+unread_count+'条':item['content'][_0x23a96a(0xe1,'vnPQ')]=_0x23a96a(0xef,'9%Kz'),item[_0x23a96a(0xe6,'G3Lk')]=!![],item['unread_count']=0x0,newItems[_0x23a96a(0xae,'2&^q')](item);}else item[_0x23a96a(0x8c,'#@I]')]!=='活动助手'&&newItems[_0x23a96a(0x77,'G3Lk')](item);}obj['data']=newItems,body=JSON[_0x23a96a(0x6c,'0H#^')](obj);}catch(_0x4efec3){console['log'](_0x23a96a(0x10a,'A2LK')+_0x4efec3);}break;case/user-credit\/basis/[_0x23a96a(0x138,'AuBk')]($request[_0x23a96a(0x93,'V9bb')]):try{let obj=JSON['parse'](body);obj[_0x23a96a(0xa0,'xsZ[')][_0x23a96a(0xec,'7pPT')]=0x3e6,body=JSON[_0x23a96a(0xeb,'Xhat')](obj);}catch(_0x37d749){console['log'](_0x23a96a(0x105,'#HAe')+_0x37d749);}break;case/bazaar\/vip_tab\/modules/[_0x23a96a(0x103,'bp*n')]($request['url']):try{let obj=JSON['parse'](body);obj['data']=obj['data'][_0x23a96a(0xc5,'HV(D')](_0x4365f5=>!(_0x4365f5['type']=='FCT14A'||_0x4365f5[_0x23a96a(0xff,'xsZ[')]==_0x23a96a(0x96,'9%Kz')||_0x4365f5[_0x23a96a(0x89,'MXG0')]=='FCT07A')),body=JSON[_0x23a96a(0xeb,'Xhat')](obj);}catch(_0x5de77f){console[_0x23a96a(0xea,'JZ0B')](_0x23a96a(0xd4,'V#cb')+_0x5de77f);}break;case/questions\/\d+\/feeds/['test']($request['url']):try{body=body['replace'](/ad_info"/g,'ddgksf2013\x22');}catch(_0x5d1e6d){console[_0x23a96a(0xfd,'A2LK')](_0x23a96a(0x12a,'IkWc')+_0x5d1e6d);}break;case/next-data/[_0x23a96a(0xe0,'s1K6')]($request[_0x23a96a(0xb2,'4xrW')]):try{let obj=JSON['parse'](body),items=[];for(let item of obj[_0x23a96a(0x125,'u!lE')][_0x23a96a(0xf3,'#@I]')]){if(item[_0x23a96a(0xc0,'snFt')]=='normal'){if(item['data']?.['link_cards'])item['data']['link_cards']=[];items['push'](item);}}obj[_0x23a96a(0x80,'#HAe')][_0x23a96a(0xbe,'hGsP')]=items,body=JSON['stringify'](obj);}catch(_0x438938){console['log']('zhihu\x20next-data'+_0x438938);}break;case/next-render/['test']($request[_0x23a96a(0xcf,'JZ0B')]):try{let obj=JSON[_0x23a96a(0xba,'0H#^')](body),items=[];for(let item of obj[_0x23a96a(0xf7,'Rq%g')]){if(item['type']=='answer'){if(item[_0x23a96a(0xfc,'n@Xp')]?.[_0x23a96a(0xf8,'IkWc')])delete item[_0x23a96a(0xf0,'xsZ[')];items[_0x23a96a(0x85,'MXG0')](item);}}obj['data']=items,body=JSON[_0x23a96a(0xe4,'hGsP')](obj);}catch(_0x5a90ba){console['log'](_0x23a96a(0xe8,'ZuqP')+_0x5a90ba);}break;case/bazaar\/vip_tab\/header/[_0x23a96a(0xd6,'V9bb')]($request[_0x23a96a(0xa6,'4H%x')]):try{let obj=JSON[_0x23a96a(0xa7,'HV(D')](body);obj[_0x23a96a(0x110,'IkWc')]={'day_url':'https://pic1.zhimg.com/v2-4812630bc27d642f7cafcd6cdeca3d7a_r.png','night_url':_0x23a96a(0x83,'rMzn')},obj[_0x23a96a(0x69,'HV(D')]={'jump_url':_0x23a96a(0x116,'xsZ['),'text':_0x23a96a(0xad,'zyo2'),'color_text':{'text':'','color':''}},obj[_0x23a96a(0x104,'MXn%')]=null,body=JSON[_0x23a96a(0x84,'Rq%g')](obj);}catch(_0x3161f9){console[_0x23a96a(0xf6,'#@I]')](_0x23a96a(0x78,'V9bb')+_0x3161f9);}break;case/topstory\/hot-lists/[_0x23a96a(0xbf,'hGsP')]($request[_0x23a96a(0x102,'#@I]')]):try{let obj=JSON[_0x23a96a(0x12d,'s1K6')](body);obj[_0x23a96a(0x11d,'(DO8')]['data']=obj['data']['data'][_0x23a96a(0x94,'xsZ[')](_0x479297=>!_0x479297[_0x23a96a(0xb8,'#@I]')]),body=JSON['stringify'](obj);}catch(_0x10da0e){console['log'](_0x23a96a(0xaf,'rMzn')+_0x10da0e);}break;case/topstory\/recommend/[_0x23a96a(0x9d,'vnPQ')]($request['url']):try{let obj=JSON[_0x23a96a(0xf9,'n@Xp')](body);const propsToDelete=['TikTok','副业','赚钱','挣钱',_0x23a96a(0x11b,'zuM@'),'运营','电商','剪辑',_0x23a96a(0x7a,'MXG0'),'失业','收益','稿费',_0x23a96a(0xdc,'7]YL'),'存款','兼职'];let items=[];for(let item of obj[_0x23a96a(0xf1,'HV(D')]){if(item[_0x23a96a(0x11c,'snFt')]('ad')||item['promotion_extra']!=null||item[_0x23a96a(0xf2,'n@Xp')]==_0x23a96a(0x114,'u!lE')||item[_0x23a96a(0x68,'MXG0')]?.[_0x23a96a(0xff,'xsZ[')]==_0x23a96a(0xac,'7]YL')||item['extra']?.['type']==_0x23a96a(0x12f,'snFt'))continue;else{if(item['type']=='common_card'&&item[_0x23a96a(0x6e,'4xrW')]?.[_0x23a96a(0xce,'*Xoz')]==_0x23a96a(0xe3,'#@I]')){let videoUrl=item[_0x23a96a(0x11f,'Xhat')]['feed_content'][_0x23a96a(0xc2,'snFt')]['customized_page_url'],videoID=videoUrl[_0x23a96a(0x9f,'MXG0')](/[?&]videoID=(\d+)/)[0x1];videoID&&(item[_0x23a96a(0x129,'u!lE')][_0x23a96a(0x108,'u!lE')][_0x23a96a(0x115,'Xhat')]['id']=videoID),items[_0x23a96a(0xdb,'bp*n')](item);}else{if(item[_0x23a96a(0x123,'#@I]')]==_0x23a96a(0x128,'A2LK')&&item['common_card']?.[_0x23a96a(0x97,'yJF9')]?.[_0x23a96a(0x100,'IkWc')]?.['id']){let search='\x22feed_content\x22:{\x22video\x22:{\x22id\x22:',str=$response[_0x23a96a(0xc7,'9%Kz')][_0x23a96a(0xb4,'^7kn')]($response[_0x23a96a(0x81,'n@Xp')]['indexOf'](search)+search[_0x23a96a(0x6b,'ZuqP')]),videoID=str[_0x23a96a(0x134,'F9FM')](0x0,str['indexOf'](','));item[_0x23a96a(0xb6,'UHfx')][_0x23a96a(0xbc,'A2LK')][_0x23a96a(0x12b,'S&KK')]['id']=videoID,items['push'](item);}else{if(item[_0x23a96a(0xd3,'AuBk')]?.['feed_content']?.[_0x23a96a(0xcd,'4H%x')]?.[_0x23a96a(0x124,'MXG0')]){var find=![];propsToDelete[_0x23a96a(0x137,'u!lE')](_0x2d91c2=>{const _0x5e121d=_0x23a96a;item[_0x5e121d(0xca,'vnPQ')][_0x5e121d(0x11a,'Rq%g')]['title'][_0x5e121d(0x107,'rMzn')]['includes'](_0x2d91c2)&&(find=!![]);}),!find&&items['push'](item);}else items['push'](item);}}}}obj['data']=items;for(let i=0x0;i<obj['data'][_0x23a96a(0xb5,'4H%x')];i++){obj['data'][i]['offset']=i+0x1;}body=JSON[_0x23a96a(0x131,'bm)*')](obj);}catch(_0x4ce298){console[_0x23a96a(0x82,'bp*n')]('zhihu\x20recommend'+_0x4ce298);}break;case/unlimited\/go\/my_card/[_0x23a96a(0x10f,'Rq%g')]($request[_0x23a96a(0x99,'AuBk')]):try{let obj=JSON[_0x23a96a(0x11e,'7pPT')](body);obj['title']='盐选会员',obj[_0x23a96a(0xe5,'hGsP')]=_0x23a96a(0x70,'7pPT'),obj['card_jump_url']='',obj[_0x23a96a(0xb7,'zuM@')]='',body=JSON[_0x23a96a(0xb3,'n@Xp')](obj);}catch(_0x1c15c6){console['log'](_0x23a96a(0xa1,'n@Xp')+_0x1c15c6);}break;case/people\/self/[_0x23a96a(0x122,'n@Xp')]($request[_0x23a96a(0xc6,'*Xoz')]):try{let obj=JSON['parse'](body);obj[_0x23a96a(0xf4,'^7kn')][_0x23a96a(0x95,'A2LK')]=!![],obj[_0x23a96a(0x98,'2&^q')]['vip_icon']={'url':_0x23a96a(0x79,'JZ0B'),'night_mode_url':_0x23a96a(0xfe,'2&^q')},obj['vip_info']['entrance']={'icon':{'url':_0x23a96a(0x135,'nU0!'),'night_mode_url':_0x23a96a(0x74,'vnPQ')},'title':_0x23a96a(0x9a,'MXn%'),'expires_day':'2039-12-24','sub_title':null,'button_text':_0x23a96a(0x12c,')zTp'),'jump_url':_0x23a96a(0xaa,'40vx'),'button_jump_url':_0x23a96a(0xd2,'7pPT'),'sub_title_new':null,'identity':'svip'},obj['vip_info'][_0x23a96a(0x136,'4H%x')]={'left_button':{'title':_0x23a96a(0x71,'AuBk'),'description':'为您严选好内容','jump_url':_0x23a96a(0x113,'*Xoz')},'right_button':{'title':'我的盐选会员','description':_0x23a96a(0xde,'bp*n'),'jump_url':_0x23a96a(0x10d,'*Xoz')}},obj[_0x23a96a(0x6a,'Xhat')][_0x23a96a(0xed,'MXn%')]={'title':_0x23a96a(0xc3,'^7kn'),'sub_title':_0x23a96a(0xcb,'V9bb'),'jump_url':_0x23a96a(0xd1,'MXn%'),'button_text':_0x23a96a(0x67,'UHfx')},body=JSON['stringify'](obj);}catch(_0x3a114c){console[_0x23a96a(0x6f,'V#cb')]('zhihu\x20people'+_0x3a114c);}break;case/commercial_api\/real_time_launch/[_0x23a96a(0x112,'5Vjd')]($request['url']):try{body=body[_0x23a96a(0x86,'%dk[')](/img_play_duration\\":\d+/g,_0x23a96a(0x8d,'zuM@'))['replace'](/launch_timeout\\":\d+/g,'launch_timeout\x22:0');}catch(_0x1c834f){console[_0x23a96a(0x82,'bp*n')]('zhihu\x20openad'+_0x1c834f);}break;case/search\/recommend_query/[_0x23a96a(0xcc,'^7kn')]($request[_0x23a96a(0xdf,'9%Kz')]):try{let obj=JSON['parse'](body);obj['recommend_queries']?.[_0x23a96a(0x117,'S&KK')]&&(obj[_0x23a96a(0xdd,'IkWc')][_0x23a96a(0x9c,'s1K6')]=[{'query':'','real_query':'','query_display':'','uuid':'f8c151ce-8bba-4491-89d1-06af4353e3da','type':_0x23a96a(0xbd,'vnPQ')}]),body=JSON[_0x23a96a(0xbb,'40vx')](obj);}catch(_0x1764ee){console[_0x23a96a(0xd0,'zyo2')](_0x23a96a(0x6d,'A2LK')+_0x1764ee);}break;case/search\/tabs/[_0x23a96a(0x103,'bp*n')]($request[_0x23a96a(0x111,'MXn%')]):try{let obj=JSON['parse'](body);obj[_0x23a96a(0xb0,'7pPT')]=obj[_0x23a96a(0xd7,'snFt')]['filter'](_0x2eea12=>!(_0x2eea12['t']==_0x23a96a(0xfb,'MXn%'))),body=JSON[_0x23a96a(0x7e,'5Vjd')](obj);}catch(_0x2f4569){console['log']('zhihu\x20search/tabs'+_0x2f4569);}break;case/search\/preset_words/[_0x23a96a(0xd8,'nU0!')]($request['url']):try{let obj=JSON[_0x23a96a(0x66,'S&KK')](body);obj[_0x23a96a(0xb9,'yJF9')]?.[_0x23a96a(0xab,'40vx')]&&obj[_0x23a96a(0x10e,'5Vjd')]['words'][_0x23a96a(0x132,'rMzn')](_0x1c852d=>{const _0x249c25=_0x23a96a;_0x1c852d['begin_ts']=0xb2d05e00,_0x1c852d[_0x249c25(0x109,'0H#^')]=0xb2d06c10;}),obj[_0x23a96a(0x10b,'40vx')]?.['force_words']&&obj['preset_words'][_0x23a96a(0x91,'bm)*')][_0x23a96a(0x10c,'4d9S')](_0x2a421e=>{const _0x484b56=_0x23a96a;_0x2a421e[_0x484b56(0x127,'JZ0B')]=0xb2d05e00,_0x2a421e[_0x484b56(0x133,'4H%x')]=0xb2d06c10;}),body=JSON[_0x23a96a(0x121,'vnPQ')](obj);}catch(_0x2272ed){console[_0x23a96a(0x76,'4d9S')](_0x23a96a(0x119,'V#cb')+_0x2272ed);}break;case/search\/hot_search/['test']($request[_0x23a96a(0x8a,'##AR')]):try{let obj=JSON[_0x23a96a(0xfa,'ZuqP')](body);obj[_0x23a96a(0xd5,'4d9S')]&&(obj[_0x23a96a(0xa9,'rMzn')]=[]),body=JSON[_0x23a96a(0x126,'ZuqP')](obj);}catch(_0x3a26bd){console[_0x23a96a(0xa5,'9%Kz')](_0x23a96a(0x92,'40vx')+_0x3a26bd);}break;case/bazaar\/vip_tab\/tabs/[_0x23a96a(0xbf,'hGsP')]($request['url']):try{let obj=JSON[_0x23a96a(0xc4,'XsCu')](body);obj=obj['filter'](_0x1a8987=>!(_0x1a8987['value']=='vip_buy')),body=JSON['stringify'](obj);}catch(_0x2ce863){console['log'](_0x23a96a(0x88,'9%Kz')+_0x2ce863);}break;default:$done({});break;}$done({'body':body});}else $done({});var version_ = 'jsjiami.com.v7';
