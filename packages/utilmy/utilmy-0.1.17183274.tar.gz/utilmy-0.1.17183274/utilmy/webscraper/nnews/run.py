""" 
#### install pip install fire utilmy 




### URL sample:

        https://finance.yahoo.com/news/nvidia-microsoft-google-and-others-partner-with-us-government-on-ai-research-program-160111850.html


        https://www.businesswire.com/news

        https://www.prnewswire.com

        https://news.google.com/search?q="Microsoft".%20partnership%20site%3Aprnewswire.com&hl=en-US&gl=US&ceid=US%3Aen

        https://www.prnewswire.com/news-releases/unicef-announces-new-partnership-with-microsoft-to-address-education-crisis-affecting-displaced-and-refugee-children-and-young-people-300719648.html

        https://www.prnewswire.com/news-releases/cognizant-and-microsoft-announce-global-partnership-to-expand-adoption-of-generative-ai-in-the-enterprise-and-drive-industry-transformation-302123026.html

        https://news.google.com/search?q="Microsoft"%20%20"partnership"%20site%3Aprnewswire.com&hl=en-US&gl=US&ceid=US%3Aen

        https://finance.yahoo.com/quote/MSFT/press-releases/

        https://news.microsoft.com/category/press-releases/

        https://www.prnewswire.com/search/news/?keyword=partnership&pagesize=25&page=7

        https://www.prnewswire.com/search/news/?keyword=Microsoft&page=1&pagesize=100





"""
if "imports":

    import os, time, traceback, warnings, logging, sys, sqlite3
    warnings.filterwarnings("ignore")
    import requests
    from bs4 import BeautifulSoup as Soup

    import json, pandas as pd, numpy as np
    from dataclasses import dataclass
    ############################################
    from utilmy import pd_read_file, os_makedirs, pd_to_file
    from utilmy import log



urlstr2="""
https://3dprint.com/109310/airbus-autodesk-dividing-wall/amp/
https://3dprintingindustry.com/news/creo-5-0-brings-materialise-integration-autodesk-compatibility-130803/
https://aecmag.com/reality-capture-modelling/esri-uk-partners-with-tetra-tech-on-indoor-mapping/
https://aws.amazon.com/blogs/apn/maintaining-a-health-and-wellness-repository-with-a-blockchain-based-health-monitoring-solution/
https://aws.amazon.com/blogs/database/bungkusit-uses-amazon-qldb-and-veridoc-globals-isv-technology-to-improve-the-customer-and-delivery-agent-experience/
https://aws.amazon.com/blogs/database/how-specright-uses-amazon-qldb-to-create-a-traceable-supply-chain-network/
https://bakkt.com/newsroom/bakkt-and-global-payments-announce-strategic-alliance
https://blogs.nvidia.com/blog/microsoft-build-optimized-ai-developers/
https://channellife.com.au/story/beyondtrust-and-jamf-to-enhance-mac-endpoint-security
https://cioafrica.co/liquid-c2-becomes-africas-first-google-cloud-interconnect-provider/
https://coincentral.com/partnering-with-consensys-amazon-web-services-launches-kaleido-blockchain-platform/
https://cryptoslate.com/tron-integrated-with-amazon-web-services-to-accelerate-blockchain-adoption/
https://cxotoday.com/press-release/deloitte-and-nexxiot-form-alliance-to-provide-the-blockchain-infrastructure-to-digitize-logistics-supply-chain/
https://elblog.pl/2024/06/09/ramat-gan-expands-ai-learning-program-in-elementary-schools-with-google-and-technion-partnership/
https://en.prnasia.com/releases/apac/mindtree-joins-hyperledger-to-accelerate-blockchain-development-253520.shtml
https://fashionunited.uk/news/retail/jd-com-partners-with-inditex-and-launches-massimo-dutti-store/2024060475877
https://ffnews.com/newsarticle/global-payments-enters-definitive-agreement-to-acquire-evo-payments/
https://fintechnews.ch/fintechusa/global-payments-signs-deal-to-acquire-mineraltree-for-us500-million/48815/
https://hitconsultant.net/2022/01/13/gsk-launches-accelerated-clinical-trial-with-tempus/
https://iberianlawyer.com/garrigues-and-microsoft-sign-a-strategic-collaboration-agreement-to-drive-innovation-and-the-use-of-ai/
https://ibsintelligence.com/ibsi-news/bursa-malaysia-digital-asset-and-vmware-blockchain-to-develop-dematerialization-proof-of-concept/
https://im-mining.com/2018/10/16/bentley-systems-new-digital-twin-partnership-atos/
https://innovation-village.com/microsoft-collaborates-with-cyber-shujaa-to-upskill-100-kenyan-students-in-cybersecurity/
https://investors.bakkt.com/news/news-details/2022/Bakkt-and-Global-Payments-Announce-Strategic-Alliance/default.aspx
https://investors.bentley.com/news-releases/news-release-details/wsb-and-bentley-systems-offer-new-digital-construction
https://investors.globalpayments.com/news-events/press-releases/detail/447/global-payments-and-commerzbank-announce-joint-venture-in
https://ir.amd.com/news-events/press-releases/detail/1198/amd-instinct-mi300x-accelerators-power-microsoft-azure
https://ir.meetipower.com/news-releases/news-release-details/ipower-enhances-supersuite-platform-capabilities-amazon
https://manufactur3dmag.com/agnikul-partners-with-eos-to-accelerate-in-house-3d-printing-of-rocket-engines/
https://manufacturingdigital.com/lean-manufacturing/morgan-motor-company-embraces-consumer-customisation-autodesks-3d-design-solutions
https://mundogeo.com/en/2022/11/03/nearabl-adopts-the-bentley-itwin-platform-to-expand-infrastructure-deployments/
https://new.abb.com/news/detail/69186/abb-and-ibm-to-bolster-cybersecurity-for-industrial-operations
https://new.abb.com/news/detail/85887/abb-working-with-aws-to-develop-digitally-integrated-all-electric-operations-for-net-zero-emissions-mining
https://news.microsoft.com/2020/10/19/bentley-systems-expands-alliance-with-microsoft-to-accelerate-infrastructure-digital-twin-innovations/
https://news.microsoft.com/apac/2020/03/12/bentley-systems-microsoft-and-schneider-electric-re-imagine-future-workplaces-with-sensors-sustainability-iot-and-ai/
https://news.microsoft.com/en-sg/2024/05/21/microsoft-collaborates-with-enterprise-singapore-ai-singapore-and-the-infocomm-media-development-authority-to-accelerate-ai-transformation-for-smes-with-ai-pinnacle-program/
https://news.sap.com/2024/06/sap-business-ai-meta-open-source-models/
https://news.vmware.com/technologies/vmware-blockchain-is-bringing-ethereum-to-the-enterprise
https://newsroom.accenture.com/news/2018/accenture-and-thales-demonstrate-how-blockchain-technology-can-secure-and-simplify-aerospace-and-defense-supply-chains
https://newsroom.accenture.com/news/2019/accenture-and-generali-employee-benefits-apply-blockchain-technology-aiming-to-transform-the-reinsurance-process-for-captive-services#:~:text=MILAN%3B%20April%2016%2C%202019%20%E2%80%93,data%20and%20reduces%20processing%20errors
https://newsroom.trendmicro.com/2019-06-11-Trend-Micro-Collaborates-with-DOCOMO-to-Launch-Security-for-IoT-Devices-Fully-Protecting-Business-Users-Connected-Experience
https://newsroom.trendmicro.com/2021-07-07-Trend-Micro-Announces-New-Collaboration-with-Microsoft-to-Safeguard-Cybersecurity
https://nextpittsburgh.com/business-tech-news/pitt-focuses-on-improving-manufacturing-with-ansys-additive-manufacturing-research-laboratory-dedication/
https://press.aboutamazon.com/aws/2024/6/ascend-money-drives-financial-inclusion-across-southeast-asia-using-ai-on-aws
https://roboticsandautomationnews.com/2022/07/27/hexagon-and-esab-to-help-manufacturers-optimise-robotic-welding-processes/53522/
https://siliconangle.com/2024/06/05/five9-integrates-salesforce-evolve-cx-platform/
https://smartmaritimenetwork.com/2022/09/05/hoegh-autoliners-first-to-pilot-kongsberg-digital-twin-system/
https://solarquarter.com/2024/06/12/repsol-and-microsoft-seal-230-mw-renewable-energy-deal-with-six-vppas-accelerating-green-transformation-in-spain/#:~:text=Sign%20in-,Repsol%20and%20Microsoft%20Seal%20230%20MW%20Renewable%20Energy%20Deal%20with,Accelerating%20Green%20Transformation%20in%20Spain
https://techcrunch.com/2024/06/06/google-partners-with-rapidsos-to-enable-911-contact-through-rcs/
https://techcrunch.com/2024/06/10/apple-brings-chatgpt-to-its-apps-including-siri/
https://thepaypers.com/online-payments/apexx-global-partners-with-global-payments-on-bnpl--1256444
https://thepaypers.com/online-payments/apexx-global-partners-with-global-payments-on-bnpl--1256444
https://thepaypers.com/payments-general/banco-carrefour-partners-global-payments-for-payments-agreement--1249504?utm_source=dlvr.it&utm_medium=twitter
https://thepaypers.com/payments-general/global-payments-partners-with-visa--1264755
https://thepaypers.com/payments-general/global-payments-partners-with-visa--1264755
https://timestabloid.com/shiba-inu-joins-apple-netflix-amazon-disney-at-cdsa-to-enhance-content-security/
https://venturebeat.com/business/cupix-digital-twin-plugs-into-autodesk-bim-360-for-3d-builder-workflows/
https://via.tt.se/pressmeddelande/3332336/fukui-computer-partners-with-bentley-systems-to-promote-digital-transformation-in-japans-infrastructure-field?publisherId=259167
https://www.3dnatives.com/en/aetrex-3d-printed-shoe-insoles-100920205/
https://www.afr.com/technology/asx-signs-mou-with-vmware-to-support-blockchain-rollout-20190826-p52kpo
https://www.ajc.com/business/economy/global-payments-merge-with-tsys-tie-georgia-fintech-firms/eq1DfaXdcBj75T243O5B8H/
https://www.ansys.com/news-center/press-releases/9-7-2023-ansys-global-partnership-with-f1-in-schools
https://www.apple.com/newsroom/2024/06/apple-books-becomes-official-audiobook-home-for-reeses-book-club/
https://www.architectmagazine.com/technology/earthcam-announces-expanded-autodesk-partnership_o
https://www.arcweb.com/blog/strategic-collaboration-agreement-aws-drive-sustainable-industrial-transformation-announced
https://www.autodesk.com/products/fusion-360/blog/autodesk-cadence-integration-pcb-design-3d-modeling/
https://www.automation.com/en-us/articles/november-2020/siemens-additive-manufacturing-polymers-eos
https://www.barracuda.com/company/news/2023/barracuda-cork-cyber-warranty-customers-msps
https://www.bitdefender.com/news/ckh-innovations-opportunities-development-partners-with-bitdefender-to-provide-mobile-security-services.html
https://www.blockchaintechnology-news.com/2023/05/deloitte-and-bnp-paribas-join-consortium-in-creating-blockchain-network-for-financial-market/
https://www.braskem.com.br/news-detail/braskem-and-made-in-space-to-send-plastics-recycler-to-international-space-station
https://www.braskem.com.br/usa/news-detail/braskem-and-divedesign-partner-to-develop-a-custom-3d-printed-k9-quad-cart-for-rescue-dog-wobbly-hannah
https://www.businesswire.com/news/home/20180926005246/en/Constellation-Joins-Hyperledger
https://www.businesswire.com/news/home/20181015005268/en/Siemens-and-Bentley-Systems-Announce-PlantSight%E2%84%A2-Digital-Twin-Cloud-Services
https://www.cnbc.com/2024/06/07/gm-costco-auto-program-evs.html
https://www.cnbctv18.com/market/stocks/tanla-platforms-partners-vodafone-idea-to-deploy-blockchain-enabled-platform-11730752.htm
https://www.coindesk.com/business/2023/05/09/digital-asset-announces-launch-of-global-blockchain-network-with-deloitte-goldman-and-others/
https://www.cointrust.com/market-news/itau-unibanco-advances-digital-asset-services-with-aws-blockchain-technology
https://www.commercialpaymentsinternational.com/news/global-payments-signs-multi-year-agreement-with-wells-fargo/
https://www.constructionbriefing.com/news/hexagon-to-partner-with-the-nemetschek-group-to-drive-adoption-of-digital-twins/8036224.article
https://www.consultancy-me.com/news/8505/roland-berger-and-microsoft-team-up-for-end-to-end-ai
https://www.consultancy.asia/news/880/cathay-pacific-launch-blockchain-powered-rewards-app-with-accenture
https://www.crypto-news-flash.com/chainlink-teams-up-with-amazon-to-build-the-future-ecosystem-of-web3-and-beyond/
https://www.cryptoground.com/a/linux-foundation-unveils-a-blockchain-based-platform-for-american-association-of-insurance-services
https://www.cryptoninjas.net/2019/05/07/blockchain-privacy-layer-qedit-partners-with-vmware-ant-financial-and-rgax/
https://www.designnews.com/3d-printing/materialise-and-arcelormittal-partner-to-enhance-metal-3d-printing
https://www.digitalengineering247.com/article/ansys-and-nvidia-extend-cae-collaboration/engineering-computing
https://www.electronicdesign.com/technologies/embedded/software/article/21264271/machine-design-siemens-ibm-get-their-assets-in-order
https://www.enr.com/articles/52546-autodesk-partners-with-ioffice-spaceiq-on-asset-operations
https://www.ey.com/en_gl/newsroom/2024/06/ey-announces-alliance-with-docusign-to-offer-clients-intelligent-agreement-management
https://www.f5.com/company/news/press-releases/telefonica-tech-f5-launch-new-service-protect-apps
https://www.finextra.com/newsarticle/44246/mastercard-and-bunq-forge-ai-open-banking-partnership
https://www.forescout.com/press-releases/belden-expands-forescout-partnership-to-protect-industrial-and-critical-infrastructure-from-cyber-threat/
https://www.forescout.com/press-releases/forescout-and-arista-networks-join-forces-to-deliver-zero-trust-security/
https://www.fox19.com/2024/06/06/kroger-clermont-senior-services-partner-teach-online-grocery-shopping/
https://www.fujitsu.com/global/about/resources/news/press-releases/2020/0515-01.html#:~:text=Leveraging%20Fujitsu's%20proprietary%20security%20technology,enabling%20asset%20transfers%20and%20recovery
https://www.gcimagazine.com/brands-products/hair-care/news/22911857/function-of-beauty-lands-on-amazon-brings-target-pro-lines-to-dtc
https://www.geoweeknews.com/news/bentley-esri-announce-major-integrations-with-nvidia-omniverse
https://www.geoweeknews.com/news/digital-twin-platform-smartviz-now-powered-by-bentley-s-itwin
https://www.gim-international.com/content/news/bentley-systems-and-worldsensing-sign-strategic-agreement
https://www.globalpayments.com/insights/2019/09/18/global-payments-and-tsys-merge
https://www.gpsworld.com/103265-2/
https://www.gpsworld.com/dcu-bentley-partner-for-3d-smart-city-research-initiative/
https://www.gruppotim.it/en/press-archive/market/2024/PR-TIM-and-GOOGLE-CLOUD-6-June-2024.html
https://www.hyperledger.org/announcements/2019/09/11/consensys-joins-hyperledger-as-a-premier-member
https://www.ibm.com/blog/transforming-telecom-tower-workflows-with-ibm-digital-twin-platform-on-aws/
https://www.investing.com/news/company-news/google-cloud-oracle-partner-for-multicloud-services-93CH-3480117
https://www.itpro.com/cloud/software-as-a-service-saas/356648/global-payments-to-boost-fintech-services-with-aws
https://www.johnlewispartnership.media/pressrelease/jlp/details/17387
https://www.kongsbergdigital.com/resources/kongsberg-digital-signs-agreement-with-exxonmobil-to-explore-use-of-kognitwin-r-energy-dynamic-digital-twin-saas-solution
https://www.ledgerinsights.com/accenture-zurich-blockchain-surety-bonds-insurance/
https://www.linkedin.com/pulse/dublin-airport-takes-off-construction-cloud-digital-a8fuc/
https://www.ltts.com/press-release/digital-twin-Microsoft-Bentley-Systems
https://www.ltts.com/press-release/LTTS-and-Ansys-set-up-CoE-for-Digital-Twin
https://www.mastercard.com/news/eemea/en/newsroom/press-releases/press-releases/en/2024/may/mastercard-and-hsbc-middle-east-accelerate-travel-payment-innovation-through-bank-s-first-wholesale-travel-program/
https://www.militaryaerospace.com/commercial-aerospace/article/55055117/eva-air-and-panasonic-in-ifec-deal-for-54-aircraft
https://www.morningstar.com/news/business-wire/20240610288244/pega-to-expand-genai-framework-with-google-cloud-aws-to-allow-for-enterprise-generative-ai-choice
https://www.msspalert.com/news/thales-kyndryl-partner-for-security-incident-response
https://www.nasdaq.com/articles/global-payments-announces-mixed-results-strategic-partnership-with-google-2021-02-08
https://www.nonstoplocal.com/spokane/news/blue-cross-of-idaho-partners-with-amazon-for-pharmaceuticals/article_9d638725-0e4e-5414-872d-19847894bdb5.html
https://www.offshore-energy.biz/heerema-renews-contract-with-kongsberg-digital-in-support-of-crane-simulator/
https://www.oilfieldtechnology.com/digital-oilfield/22112019/adnoc-and-honeywell-to-undertake-predictive-maintenance-project/
https://www.oracle.com/in/corporate/pressrelease/niti-aayog-oracle-pilot-real-drug-supply-chain-with-blockchain-iot-2018-09-28.html#:~:text=In%20order%20to%20fight%20the,to%20pilot%20a%20real%20drug
https://www.packworld.com/rigid/containers-closures/news/22911890/plastipak-packaging-kraft-heinz-moves-to-100-rpet-containers-for-mayo-miracle-whip#:~:text=In%20the%20United%20States%2C%20KRAFT,carbon%20emissions%20of%20the%20packaging.
https://www.panasonic.aero/press-release/
https://www.pinkbike.com/news/sram-produces-generative-design-prototype-cranks-in-partnership-with-autodesk.html
https://www.press.bmwgroup.com/global/article/detail/T0439464EN/bmw-group-partners-with-dassault-syst%C3%A8mes-to-bring-the-3dexperience-platform-to-its-future-engineering-platform?language=en
https://www.prnewswire.com/il/news-releases/assembrix-partners-with-eos-beamit-3t-additive-manufacturing-and-boeing-to-demonstrate-the-secured-cross-continent-distributed-additive-manufacturing-879047609.html
https://www.pymnts.com/news/b2b-payments/2018/currencycloud-cashplus-smb-payments/
https://www.qna.org.qa/en/News-Area/News/2024-06/11/0044-gco-signs-mou-with-amazon-ads-to-support-qatar's-digital-economy#:~:text=Doha%2C%20June%2011%20(QNA),of%20Qatar's%20digital%20transformation%20journey.
https://www.rcrwireless.com/20231218/internet-of-things-4/vodafone-deloitte-intro-blockchain-iot-service-to-streamline-trust-in-supply-chains
https://www.salesforce.com/news/stories/aston-martin-ai-data/
https://www.ship-technology.com/news/dassault-shi-smart-digital-shipyard/
https://www.slalom.com/us/en/who-we-are/newsroom/salesforce-partnership-customer-ai-transformation
https://www.sportcal.com/news/copa-america-to-air-on-amazon-prime-video-in-japan/#:~:text=This%20represents%20Prime%20Video's%20first,up%20in%20the%20Japanese%20market.&text=The%20Amazon%20Prime%20Video%20streaming,July%2C%20it%20has%20been%20revealed.
https://www.tahawultech.com/industry/technology/vodafone-and-block-gemini-collaborate-on-blockchain-solution/
https://www.tctmagazine.com/additive-manufacturing-3d-printing-news/etihad-airways-3d-print-aircraft-parts-abu-dhabi-eos-polymer/
https://www.telekom.com/en/media/media-information/archive/deutsche-telekom-joined-the-global-hyperledger-member-community-556598
https://www.tenable.com/press-releases/tenable-and-siemens-energy-expand-collaboration-on-ot-cybersecurity
https://www.tenable.com/press-releases/tenable-integrates-with-google-cloud-security-command-center
https://www.thalesgroup.com/en/group/investors/press_release/thales-and-google-cloud-announce-strategic-partnership-jointly
https://www.thalesgroup.com/en/worldwide/security/press_release/thales-completes-acquisition-imperva-creating-global-leader
https://www.thalesgroup.com/en/worldwide/security/press_release/thales-teams-nozomi-networks-expand-cyber-incident-detection
https://www.thehindubusinessline.com/markets/coforge-shares-rise-with-new-ai-innovation-hub-collaboration-with-microsoft/article68198994.ece
https://www.timesofisrael.com/hp-to-install-israeli-cybersecurity-software-in-next-generation-computers/
https://www.trendingtopics.eu/bulgarian-blockchain-developer-limechain-joins-ibm-and-accenture-in-an-exclusive-hyperledger-club/
https://www.uipath.com/newsroom/uipath-integrates-with-microsoft-copilot-for-microsoft-365#:~:text=UiPath%2520is%2520one%2520of%2520the,own%2520custom%2520copilot%252Dlike%2520experience.
https://www.vanguardngr.com/2020/01/building-collapse-corbon-partners-bim-autodesk-to-digitise-housing-construction/
https://www.vodafone.com/news/technology/vodafone-sumitomo-corporation-launch-economy-of-things-venture
https://www.vodafone.com/news/technology/vodafone-teams-up-with-deutsche-telekom-and-telefonica-to-unlock-roaming-blockchain-benefits
https://www.wipro.com/partner-ecosystem/bentley/
https://www.zdnet.com/article/siemens-alphabets-chronicle-forge-cybersecurity-partnership/



"""





def urls_fetch_text(urlstr=""):
    ##########################################################
    # pip install  newspaper3k pygooglenews

    from newspaper import Article

    urlstr = urlstr2

    urls = urlstr.split("\n")
    urls = [url for url in urls if len(url) >10 ]
    urls = np_remove_dup(urls)
    # URL of the article
    #url = 'https://www.bbc.com/news/world-us-canada-59944889'
    #url = "https://news.microsoft.com/category/press-releases/"
    #url = "https://news.microsoft.com/2024/06/03/hitachi-and-microsoft-enter-milestone-agreement-to-accelerate-business-and-social-innovation-with-generative-ai/"

    urlfail= []
    res = [ ]
    for url in urls:
        try :
            article = Article(url)

            #### Download and parse the article
            article.download()
            article.parse()

            #### Print the article's text
            txt = article.text

            res.append({
              'url': url,
              'text': text
            })

            if len(txt) < 100:
                urlfail.append(e)    


        except Exception as e:
            urlfail.append(e)    

    urlfail = pd.DataFrame(urlfailed, columns="url")
    pd_to_file(urlfail, dirout +"/url_fail.csv", index=False, show=1)

    res = pd.DataFrame(res)
    pd_to_file(res, dirout +"/url_text.csv", sep="\t", index=False, show=1)



import newspaper
from newspaper import news_pool

def urls_fetch_text(urlstr=""):
    urls = urlstr.split("\n")
    urls = [url for url in urls if len(url) > 10]
    urls = np_remove_dup(urls)  # Assuming np_remove_dup is a function you've defined to remove duplicates

    papers = [newspaper.build(url) for url in urls]
    news_pool.set(papers, threads_per_source=2)  # Set 2 threads per source
    news_pool.join()  # Start the download process

    results = []
    for paper in papers:
        for article in paper.articles:
            try:
                article.parse()  # Parse the article to access the text
                results.append({
                    'url': article.url,
                    'text': article.text
                })
            except Exception as e:
                results.append({
                    'url': article.url,
                    'error': str(e)
                })

    return results

def test1():
    # Example usage
    urlstr = "https://www.bbc.com/news/world-us-canada-59944889\nhttps://news.microsoft.com/category/press-releases/"
    results = urls_fetch_text(urlstr)
    print(results)



#####################################################################################################
def test1():
    urls = urls_fetch_prnweswire( keywords=" microsoft", tag_filter='microsoft')









#####################################################################################################
def galert_get_feed(url_rss):
    """    
    """    
    r = requests.get(url_rss)
    soup = Soup(r.text,'xml')
    
    id_alert = [x.text for x in soup.find_all("id")[1:len(soup.find_all("id"))]]
    title_alert = [x.text for x in soup.find_all("title")[1:len(soup.find_all("title"))]]
    published_alert = [x.text for x in soup.find_all("published")]
    update_alert = [x.text for x in soup.find_all("updated")[1:len(soup.find_all("updated"))]]
    link_alert = [[x["href"].split("url=")[1].split("&ct=")[0]] for x in soup.find_all("link")[1:len(soup.find_all("link"))]]
    content_alert = [x.text for x in soup.find_all("content")]



    df = pd.DataFrame(compiled_list, columns = ["ID", "Title", "Published on:", "Updated on", "Link", "Content"])
    return df 
    # df.to_excel('new_alerts.xlsx', header=True, index=False)



def np_remove_dup(xlist):
    l2= []
    for x in xlist:
        if x not in l2:
              l2.append(x)
    return l2


def urls_extract(base_url ):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    urls = [link['href'].lower() for link in links ]

    urls = np_remove_dup(urls)
    log(urlk)
    log("N_urls:", len(urls))
    return urls



def urls_fetch_prnweswire(keywords=" microsoft", tag_filter='microsoft', pagemax=2):

    keywords = keywords.replace(" ", "+")     

    prefix   = "https://www.prnewswire.com"
    url0     = 'https://www.prnewswire.com/search/news/?keyword={keywords}&page={k}&pagesize=200'
    url0     = url0.replace("{keywords}", keywords )
    
    urls2=[]
    for k in range(1, pagemax+1):
       urlk = url0.replace("{k}", str(k))
       urls = urls_extract(urlk)

       ### Custom Filter
       urls = [ link for link in urls if link.startswith('/news-releases/')]
       urls = [ prefix + url for url in urls if ".html" in url ]
       urls = [ x for x in urls if tag_filter in x ]
       # urls = [ x for x in urls if x not in set(urls2) ]

       urls2 = urls2 + urls

    log("N_prnewsire: ", len(urls2))   
    return urls2





############################################################################################
def urls_fetch_yahoonews( keywords="microsoft" ):

    val = { "microsoft":"MSFT"}.get(keywords)
    url = f"https://finance.yahoo.com/quote/{val}/press-releases/"
    DIV_QUERY_SELECTOR = 'div.content.svelte-j87knz'
    H3_TAG = 'h3.clamp.svelte-j87knz'
    DIV_PUBLISHING = 'div.publishing.font-condensed.svelte-1k3af9g'
    A_TAG = 'a.subtle-link'

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_timeout(5000)

        url_list = []
        items = page.query_selector_all(DIV_QUERY_SELECTOR)

        for item in items:
            try:
                title_element = item.query_selector(H3_TAG)
                if title_element:
                    title = title_element.inner_text()
                    link  = item.query_selector(A_TAG).get_attribute('href')
                    date_element = item.query_selector(DIV_PUBLISHING)
                    if date_element:
                        date_text = date_element.inner_text()
                        url_list.append({
                            'title': title,
                            'link': link,
                            'date': date_text
                        })
            except Exception as e:
                print(f"Error: {e}")
                continue

        browser.close()

    url_list = pd.DataFrame(url_list)         
    return url_list




def urls_fetch_microsoftnews(url = "https://news.microsoft.com/category/press-releases/"):
    TAG_ARTICLE = 'article.category-press-releases'
    TAG_DIV = 'div.c-paragraph-3.c-meta-text'
    A_TAG = 'a.f-post-link.c-heading-6.m-chevron'

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        url_list = []
        items = page.query_selector_all(TAG_ARTICLE)

        for item in items:
            try:
                date_element = item.query_selector(TAG_DIV)
                title_element = item.query_selector(A_TAG)
                if title_element and date_element:
                    date  = date_element.inner_text().strip()
                    title = title_element.inner_text().strip()
                    link  = title_element.get_attribute('href')
                    url_list.append({
                        'title': title,
                        'link': link,
                        'date': date
                    })
            except Exception as e:
                print(f"Error: {e}")
                continue

        browser.close()

    url_list = pd.DataFrame(url_list)         
    return url_list



def urls_fetch_googlenews(keywords="microsoft funding",):

    urlp = "https://news.google.com/search?q="
    keys = keywords.replace(" ", "%20" )
    url = f"{urlp}{keys}&hl=en-US&gl=US&ceid=US%3Aen"
    ### "https://news.google.com/search?q=". &hl=en-US&gl=US&ceid=US%3Aen"

    ARTICLE_SELECTOR = 'article.IFHyqb'
    TITLE_SELECTOR = 'a.JtKRv'
    LINK_SELECTOR = 'a.JtKRv'
    DATE_SELECTOR = 'time.hvbAAd'

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        url_list = []
        items = page.query_selector_all(ARTICLE_SELECTOR)

        for item in items:
            try:
                title_element = item.query_selector(TITLE_SELECTOR)
                link_element = item.query_selector(LINK_SELECTOR)
                date_element = item.query_selector(DATE_SELECTOR)

                if title_element and link_element and date_element:
                    title = title_element.inner_text().strip()
                    link = link_element.get_attribute('href')
                    date = date_element.inner_text().strip()
                    url_list.append({
                        'title': title,
                        'link': link,
                        'date': date
                    })
            except Exception as e:
                print(f"Error: {e}")
                continue

        browser.close()

    url_list = pd.DataFrame(url_list)    
    return url_list





def test5():
    from utilmy import pd_to_file ### pip instlal utilmy
    df_urls = urls_fetch_yahoonews()
    pd_to_file(df_urls,'finance_url_list.csv', index=False, show=1)

    df_urls = urls_fetch_microsoftnews()
    pd_to_file(df_urls,'finance_url_list.csv', index=False, show=1)

    df_urls = urls_fetch_googlenews()
    pd_to_file(df_urls,'finance_url_list.csv', index=False, show=1)




def get_final_url(url):
    try:
        response = requests.get(url)
        return response.url
    except requests.RequestException as e:
        return str(e)


def test4():
    # Example usage
    url = "http://example.com"  # Replace with the URL you want to check
    final_url = get_final_url(url)
    print("Final URL:", final_url)







####################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()







"""

Google News Search parameters (The Missing Manual)
There is a severe lack of documentation of Google News Search’s query parameters. Here is the most comprehensive list I am aware of. A number of these overlap with Google Search’s query parameters. I exclude any Google Search parameters that don’t make sense in the context of Google News Search. These parameters are primarily of interest to anyone querying Google News for articles using its RSS and Atom output formats.

Search
The following query parameters control Google’s interpretation of keywords. Although as_epq may be attractive for some use cases, it breaks sorting by date (scoring=n) when output is “rss” or “atom”, so stick with q for consistent sorting. Update: It seems the as_* parameters don’t work when output is “rss” or “atom”.

q=TERMS retrieve results with all of the terms. Alias: as_q
as_epq=TERMS retrieve results with the exact phrase
as_oq=TERMS retrieve results with at least one of the words
as_eq=TERMS retrieve results without the terms
as_occt=SECTION retrieve results where my terms occur…
any anywhere in the article
title in the headline of the article (same as using “allintitle:” in q)
body in the body of the article (same as using “allintext:” in q)
url in the URL of the article (same as using “allinurl:” in q)
Filter
The following query parameters filter results by Google News edition, topic, location, date, news source or author.

ned=EDITION limits results to a specific edition. Possible values: editions
topic=TOPIC limits results to a specific topic. Possible values: topics
geo=LOCATION limits results to a specific location
detect_metro_area determines location based on IP
a city, state, country, or US zip code
as_drrb=q retrieves articles added by Google News…
as_qdr=a anytime
as_qdr=h last hour
as_qdr=d last day
as_qdr=w past week
as_qdr=m past month
as_qdr=y past year
as_drrb=b retrieves articles added by Google News between…
as_minm=NUM minimum month. Possible values: [1, 12]
as_mind=NUM minimum day. Possible values: [1, 31]
as_maxm=NUM maximum month. Possible values: [1, 12]
as_maxd=NUM maximum day. Possible values: [1, 31]
as_nsrc=SOURCE limits results to a specific news source (same as using “source:” in q)
as_nloc=LOCATION limits results to news sources from a specific location (same as using “location:” in q)
as_author limits results to a specific author (same as using “author:” in q)
The as_ddrb family of parameters is occasionally set using the tbs parameter when using the web interface. You do not need to learn the tbs syntax. Note that as_nloc and geo are not synonymous.

Boost
I’m not confident that these parameters do anything when output is “rss” or “atom”, but here they are for completeness.

gl=COUNTRY boosts search results from a specific country of origin. Possible values: country codes
gll=LATITUDE,LONGITUDE boosts search results near that point. Latitude and longitude must be integer microdegrees. In otherwords, multiply each number by a million and round to the nearest integer.
gr=REGION boosts search results from a specific region. Possible values: province codes
gm=METRO boosts search results from a specific metropolitan area. Possible values: metro codes
gpc=ZIPCODE boosts search results from a specific zip code. gl must be “us”.
gcs=CITY boosts search results from a specific city. Possible values: city names in the United States and worldwide
Order
scoring=ORDER sorts search results. Default: “r”. Alias: “as_scoring”
"r" by relevance
"n" by date (newest first)
"d" by date (newest first) with duplicates
"o" by date (oldest first)
Paginate
num=NUM retrieves NUM results. Default: 10. Possible values: if q present [1,100], otherwise [1, 30]
start=OFFSET retrieves results starting from OFFSET. NUM plus OFFSET must be less than 1000, otherwise you will get zero results. Ignored if output is “rss” or “atom”. Default: 0. Requires q.
Output
output=FORMAT sets the output format
rss retrieves RSS feed
atom retrieves Atom feed
hl=LANGUAGE sets host language. Default: “us”. Possible values: languages
hdlOnly=1 displays headlines only
qsid=ID used in combination with cf=q. Update: This feature has been removed.
In older versions of Google News, it was possible to change the output of the web interface using a cf parameters. It no longer seems to work, but it is here for completeness. Note that when output is set to “rss” or “atom”, this parameter is in fact ignored.

cf=CODE
all retrieve any content
q retrieve only quotes. Requires qsid. Update: This feature has been removed.
i retrieve only images
b retrieve only blogs








Google tracking
Google uses parameters to track how users are using the web interface, which may include aq, authuser, btnmeta_news_search, edchanged, client, rls, oi, oq, resnum, sa, source, sourceid, swrnum, tab. You don’t need to worry about these, unless you want to bias Google’s internal statistics on user behavior.

Google Search
If using the web interface, performing a keyword search from Google News will redirect you to a Google Search page. The tbm=nws query parameter informs Google to display news results only.

Undocumented
I haven’t yet figured out what these do, but their impact seems minimal. If you have a clue, please mention it in the comments!

pz is usually set to 1. Default: 1. Possible values: [0, 1]
ict Possible values: “ln”, “itn0”, “tnv0”
csid
Deprecated
The following parameters work only on the deprecated Google News Search API.

v=1.0 sets the API version. Possible values: “1.0”
rsz=SIZE sets results size
small retrieves four results
large retrieves eight results
userip sets user’s IP as an abuse counter-mesure
callback runs JavaScript callback
context sets callback context
key sets API key
Sources
Search Protocol Reference, Google
Google WebSearch Protocol Reference for Google Site Search, Google
Google News Search API: JSON Developer’s Guide, Google
Creating a Custom News Search Widget Using the Google Search API, AdobePress
Google Search URL Parameters – Query String Anatomy, BlueGlass










    https://www.danielherediamejias.com/google-alerts-outreach-python/

    On today’s post I am going to show you how you can make use of Google Alerts with Python and how you can set up an automated workflow to reach out to some websites that might mention your brand or a term closely related to your business but not linking to your site.

    Basically, what we are going to do on this post is:

    Learning how to install the library google-alerts for Python.
    Setting up some alerts and parsing the RSS feed which is generated with the matches.
    Downloading the matches as an Excel file.
    Scraping the URLs and searching for a contact URL or an email address to make contact with these sites and ask for a link.
    Does this automated workflow sound interesting? Let’s get started then!

    1.- Installing google-alerts for Python
    First of all, we will need to install google-alerts for Python and seed our Google Alerts session. The command that we will need to run on our terminal to install google-alerts is:

    1
    pip install google-alerts
    After this, we will need to input our email address and our password by running the command:

    1
    google-alerts setup --email <your-email-addressl> --password '<your-password>'
    Finally to seed the Google Alerts session we will need to download the version number 84 of Chrome Driver and the version 84 of Google Chrome (be careful with not replacing the current version of Google Chrome when downloading and installing the version 84). Unfortunately, this needs to be done because this library has not been updated since 2020 and it is not compatible with the new versions of Google Chrome and Chrome Driver.

    When both Chrome Driver v84 and Google Chrome v84 have been installed, we can already run the following command to seed our Google Alerts session.

    1
    google-alerts seed --driver /tmp/chromedriver --timeout 60
    This command will open a Selenium webdriver session to log us into Google Alerts.

    2.- Creating our first alert
    Once the session is seeded, we can already use Jupyter notebook and Python to play around. We will first need to authenticate:


    from google_alerts import GoogleAlerts
    
    ga = GoogleAlerts('<your_email_address>', '<your password>')
    ga.authenticate()
    When the authentication is completed, we can create our first alert. For example for the term Barcelona in Spain:

    1
    ga.create("Barcelona", {'delivery': 'RSS', "language": "es", 'monitor_match': 'ALL', 'region' : "ES"})
    If the alert is created successfully, then it will return an object specifying the term, the language, the region, the match type and the RSS link for that alert:


    Very sadly I have not been able to create an alert which would monitor a term for all the countries because if I leave the language and region arguments empty it sets USA and English as default region and language.

    If at some point we lose track of the alerts that are active, we can list them with:

    1
    ga.list()
    And if we would like to delete an alert which is no longer useful or redundant, we can delete it by using the monitor_id and running:

    1
    ga.delete("monitor_id")
    3.- Parsing the RSS feed
    In order to parse the RSS feed we will use requests and beautifulsoup and we will extract the ID, the title, the publication date, the update date, the URL and the abstract for each alert. This data is structured as a XML file.


    import requests
    from bs4 import BeautifulSoup as Soup
    
    r = requests.get('<your RSS feed>')
    soup = Soup(r.text,'xml')
    
    id_alert = [x.text for x in soup.find_all("id")[1:len(soup.find_all("id"))]]
    title_alert = [x.text for x in soup.find_all("title")[1:len(soup.find_all("title"))]]
    published_alert = [x.text for x in soup.find_all("published")]
    update_alert = [x.text for x in soup.find_all("updated")[1:len(soup.find_all("updated"))]]
    link_alert = [[x["href"].split("url=")[1].split("&ct=")[0]] for x in soup.find_all("link")[1:len(soup.find_all("link"))]]
    content_alert = [x.text for x in soup.find_all("content")]
    
    compiled_list = [[id_alert[x], title_alert[x], published_alert[x], update_alert[x], link_alert[x], content_alert[x]] for x in range(len(id_alert))]
    With this piece of code we will get an individual list for each metric and a compiled list with all the metrics by alert.

    If we would like to, we can download the alerts as an Excel file with Pandas:


    import pandas as pd
    
    df = pd.DataFrame(compiled_list, columns = ["ID", "Title", "Published on:", "Updated on", "Link", "Content"])
    df.to_excel('new_alerts.xlsx', header=True, index=False)
    This will create an Excel document that will look like:


    4.- Reaching out to the sites
    From my point of view, using Google Alerts with Python can be specially useful when trying to automate a process to reach out to sites when they mention a brand or a specific term that can be closely related to a brand or product. With Python, we can iterate over the list of URLs, scrape them and intend to find a contact page or an email address to contact these sites. In case of finding an email address, even the delivery of an email could also be automated with Python or any other outreach tool.

    We can use this piece of code to find those strings that contain “@” (very likely email addresses) and contact pages. The filter to leave out some strings that might contain “@” but not be an email address can be polished, for now I only excluded those strings which are PNG images:


    import re
    
    for iteration in link_alert:
        
        request_link = requests.get(iteration[0])
        soup = Soup(request_link.text,'html')
    
        body = soup.find("body").text
        match = [x for x in re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', body) if ".png" not in x]
        
        contact_urls = []
        links = soup.find_all("a")
        for y in links:
            if "contact" in y.text.lower():
                contact_urls.append(y["href"])
        
        iteration.append([match])
        iteration.append([contact_urls])
    Lastly, we can iterate over the list of email addresses and use a piece of code that I published on this article about what to do with your outputs when running Python scripts, which uses email.encoder to send emails with a message like:


    from email import encoders
    from email.message import Message
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.text import MIMEText
    import smtplib 
    
    #We enter the password, the email adress and the subject for the email
    msg = MIMEMultipart()
    password = '<your email address password>'
    msg['From'] = "<your email address>"
    msg['To'] = "<Receiver email address>"
    
    #Here we set the message. If we send an HTML we can include tags
    msg['Subject'] = "Daniel Heredia - Thank you so much!"
    message = "<p>Dear lady or Sir<p>,<br><br><p>I would like to thank your for the mention of my brand on your article: " + URL + " and I would like to ask you if it were possible to include a link pointing to my website https://www.danielherediamejias.com to enable those users that are interested in my brand to get to know about me.</p><br><br><p>Thank you so much in advance!</p>"
    
    #It attaches the message and its format, in this case, HTML
    msg.attach(MIMEText(message, 'html'))
    
    #It creates the server instance from where the email is sent
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    
    #Login Credentials for sending the mail
    server.login('<your email address>', password)
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


"""
