import glob
from importlib.metadata import FileHash 
from knowledgegraph.nlpmodel import service_two_extraction
import requests
import time
"""
headers = {'Content-Type': 'application/binary'}
data = open('knowledgegraph/file/2203.09510v1.pdf', 'rb').read()
response = requests.post('http://cermine.ceon.pl/extract.do', headers=headers, data=data)
 
files = glob.glob('knowledgegraph/file/*.pdf', recursive=True)
for fh in files:
    print(fh)
    time.sleep(1)
    headers = {'Content-Type': 'application/binary'}
    data = open(fh, 'rb').read()
    response = requests.post('http://cermine.ceon.pl/extract.do', headers=headers, data=data)
    print(len(response.content))
    print("done")

import requests
import json
from requests.structures import CaseInsensitiveDict
import textwrap

texta = " Daniel Adiwardana, Minh-Thang Luong, David R So, Jamie Hall, Noah Fiedel, Romal Thoppilan, et al. 2020. Towards a human-like open-domain chatbot. arXiv preprint arXiv:2001.09977.  Siqi Bao, Huang He, Fan Wang, Hua Wu, and Haifeng Wang. 2020. PLATO: Pre-trained dialogue generation model with discrete latent variable. In Proceedings of ACL.  How deeply your girlfriend loves you!My girlfriend and I had a big quarrel yesterday.I really cantlearncalculus.,I always get the first place, and that drives me crazy.\x0cJames Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A. Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, Demis Hassabis, Claudia Clopath, Dharshan Kumaran, and Raia Hadsell. 2017. Overcoming catastrophic forgetting in neural networks. Proceedings of the NAS.  Katherine Lee, Daphne Ippolito, Andrew Nystrom, Chiyuan Zhang, Douglas Eck, Chris Callison-Burch, and Nicholas Carlini. 2021. Deduplicating training data makes language models better. arXiv preprint arXiv:2107.06499.  Mike Lewis, Yinhan Liu, Naman Goyal, Marjan Ghazvininejad, Abdelrahman Mohamed, Omer Levy, Veselin Stoyanov, and Luke Zettlemoyer. 2020a. BART: denoising sequence-to-sequence pretraining for natural language generation, translation, and comprehension. In Proceedings of ACL.  Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, et al. 2020b. Retrieval-augmented generation for knowledge-intensive nlp tasks. In Proceedings of NeurIPS.  Margaret Li, Jason Weston, and Stephen Roller. 2019. Acute-eval: Improved dialogue evaluation with optimized questions and multi-turn comparisons. arXiv preprint arXiv:1909.03087.  Yu Li, Baolin Peng, Yelong Shen, Yi Mao, Lars Liden, Zhou Yu, and Jianfeng Gao. 2021. Knowledge-grounded dialogue generation with a unified knowledge representation. arXiv preprint arXiv:2112.07924.  Siyang Liu, Chujie Zheng, Orianna Demasi, Sahand Sabour, Yu Li, Zhou Yu, Yong Jiang, and Minlie Huang. 2021. Towards emotional support dialog systems. In Proceedings of ACL.  Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. RoBERTa: A robustly optimized BERT pretraining approach. arXiv preprint arXiv:1907.11692.  Zeming Liu, Haifeng Wang, Zheng-Yu Niu, Hua Wu, Wanxiang Che, and Ting Liu. 2020. Towards conversational recommendation over multi-type dialogs. In Proceedings of ACL.  Yixin Nie, Mary Williamson, Mohit Bansal, Douwe Kiela, and Jason Weston. 2021. I like fish, especially dolphins: Addressing contradictions in dialogue modeling. In Proceedings of ACL.  Sinno Jialin Pan and Qiang Yang. 2009. A survey on  transfer learning. TKDE.  Fabio Petroni, Tim Rocktaschel, Sebastian Riedel, Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and Alexander Miller. 2019. Language models as knowledge bases? In Proceedings of EMNLP.  Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. 2018. Improving language understanding by generative pre-training. OpenAI Technical report.  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. 2019. Language models are unsupervised multitask learners. OpenAI Technical report.  Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. 2020. Exploring the limits of transfer learning with a unified text-to-text transformer. JMLR.  Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. 2020. ZeRO: Memory optimizations toward training trillion parameter models. In Proceedings of SC20.  Hannah Rashkin, Eric Michael Smith, Margaret Li, and Y-Lan Boureau. 2019. Towards empathetic opendomain conversation models: A new benchmark and dataset. In Proceedings of ACL.  Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He. 2020. DeepSpeed: System optimizations enable training deep learning models with In Proceedings of over 100 billion parameters. KDD.  Stephen Roller, Emily Dinan, Naman Goyal, Da Ju, Mary Williamson, Yinhan Liu, Jing Xu, Myle Ott, Eric Michael Smith, Y-Lan Boureau, and Jason Weston. 2021. Recipes for building an open-domain chatbot. In Proceedings of EACL.  Sahand Sabour, Chujie Zheng, and Minlie Huang. 2022. CEM: Commonsense-aware empathetic response generation. In Proceedings of AAAI.  Yunfan Shao, Zhichao Geng, Yitao Liu, Junqi Dai, Fei Yang, Li Zhe, Hujun Bao, and Xipeng Qiu. 2021. CPT: A pre-trained unbalanced transformer for both chinese language understanding and generation. arXiv preprint arXiv:2109.05729.  Hao Sun, Zhenru Lin, Chujie Zheng, Siyang Liu, and Minlie Huang. 2021a. PsyQA: A Chinese dataset for generating long counseling text for mental health support. In Findings of ACL.  Hao Sun, Guangxuan Xu, Jiawen Deng, Jiale Cheng, Chujie Zheng, Hao Zhou, Nanyun Peng, Xiaoyan Zhu, and Minlie Huang. 2021b. On the safety of conversational models: Taxonomy, dataset, and benchmark. arXiv preprint arXiv:2110.08466.  Ilya Sutskever, Oriol Vinyals, and Quoc V. Le. 2014. Sequence to sequence learning with neural networks. In Proceedings of NeurIPS.  Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du,  \x0cet al. 2022. LaMDA: Language models for dialog applications. arXiv preprint arXiv:2201.08239.  Shuohuan Wang, Yu Sun, Yang Xiang, Zhihua Wu, Siyu Ding, Weibao Gong, Shikun Feng, Junyuan Shang, Yanbin Zhao, Chao Pang, et al. 2021a. ERNIE 3.0 Titan: Exploring larger-scale knowledge enhanced pre-training for language understanding and generation. arXiv preprint arXiv:2112.12731.  Xiaoyang Wang, Chen Li, Jianqiao Zhao, and Dong Yu. 2021b. Naturalconv: A chinese dialogue dataset towards multi-turn topic-driven conversation. arXiv preprint arXiv:2103.02548.  Yida Wang, Pei Ke, Yinhe Zheng, Kaili Huang, Yong Jiang, Xiaoyan Zhu, and Minlie Huang. 2020. A large-scale chinese short-text conversation dataset. In Proceedings of NLPCC.  Sean Welleck, Jason Weston, Arthur Szlam, and Kyunghyun Cho. 2019. Dialogue natural language inference. In Proceedings of ACL.  Shaohua Wu, Xudong Zhao, Tong Yu, Rongguo Zhang, Chong Shen, Hongli Liu, Feng Li, Hong Zhu, Jiangang Luo, Liang Xu, et al. 2021. Yuan 1.0: Large-scale pre-trained language model in arXiv preprint zero-shot and few-shot learning. arXiv:2110.04725.  Wenquan Wu, Zhen Guo, Xiangyang Zhou, Hua Wu, Xiyuan Zhang, Rongzhong Lian, and Haifeng Wang. 2019. Proactive human-machine conversation with explicit conversation goal. In Proceedings ACL.  Jing Xu, Da Ju, Margaret Li, Y-Lan Boureau, Jason Weston, and Emily Dinan. 2020. Recipes for arXiv preprint safety in open-domain chatbots. arXiv:2010.07079.  Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Russ R Salakhutdinov, and Quoc V Le. 2019. XLNet: Generalized autoregressive pretraining for language understanding. In Proceedings of NeurIPS.  Wei Zeng, Xiaozhe Ren, Teng Su, Hui Wang, Yi Liao, Zhiwei Wang, Xin Jiang, ZhenZhang Yang, Kaisheng Wang, Xiaoda Zhang, et al. 2021. Pangu: Large-scale autoregressive pretrained chinese language models with auto-parallel computation. arXiv preprint arXiv:2104.12369.  Saizheng Zhang, Emily Dinan, Jack Urbanek, Arthur Szlam, Douwe Kiela, and Jason Weston. 2018. Personalizing dialogue agents: I have a dog, do you have pets too? In Proceedings of ACL.  Yizhe Zhang, Siqi Sun, Michel Galley, Yen-Chun Chen, Chris Brockett, Xiang Gao, Jianfeng Gao, Jingjing Liu, and William B Dolan. 2020. DIALOGPT: Large-scale generative pre-training for conversational response generation. In Proceedings of ACL (demo).  Zhengyan Zhang, Yuxian Gu, Xu Han, Shengqi Chen, Chaojun Xiao, Zhenbo Sun, Yuan Yao, Fanchao Qi, Jian Guan, Pei Ke, et al. 2021a. CPM-2: Largescale cost-effective pre-trained language models. AI Open.  Zhengyan Zhang, Xu Han, Hao Zhou, Pei Ke, Yuxian Gu, Deming Ye, Yujia Qin, Yusheng Su, Haozhe Ji, Jian Guan, et al. 2021b. CPM: A large-scale generative chinese pre-trained language model. AI Open.  Zhuosheng Zhang, Hanqing Zhang, Keming Chen, Yuhang Guo, Jingyun Hua, Yulong Wang, and Ming Zhou. 2021c. Mengzi: Towards lightweight yet arXiv ingenious pre-trained models for chinese. preprint arXiv:2110.06696.  Chujie Zheng, Yong Liu, Wei Chen, Yongcai Leng, and Minlie Huang. 2021. CoMAE: A multi-factor hierarchical framework for empathetic response generation. In Findings ACL.  Hao Zhou, Pei Ke, Zheng Zhang, Yuxian Gu, Yinhe Zheng, Chujie Zheng, Yida Wang, Chen Henry Wu, Hao Sun, Xiaocong Yang, et al. 2021. EVA: An open-domain chinese dialogue system with large-scale generative pre-training. arXiv preprint arXiv:2108.01547.  Hao Zhou, Chujie Zheng, Kaili Huang, Minlie Huang, and Xiaoyan Zhu. 2020. KdConv: A Chinese multi-domain dialogue dataset towards multi-turn In Proceedings of knowledge-driven conversation. ACL.  A Contributions  Yuxian Gu and Jiaxin Wen implemented the basic models and conducted strategies comparison experiments.  Hao Sun and Yi Song designed the data cleaning pipeline and constructed the pre-training data.  Jiaxin Wen, Yuxian Gu, Zheng Zhang and Jianzhu Yao conducted the model evaluation.  Yuxian Gu, Jiaxin Wen, Hao Sun, Pei Ke and Chujie Zheng wrote the paper.  Minlie Huang designed and led the research.  Xiaoyan Zhu and Jie Tang provided valuable advises to the research."


def extract_author(Text):

    chunks = textwrap.wrap(Text,100, break_long_words=False)
    authors=[]
    for chunk in chunks:
        url = "http://localhost:8072/parse.do"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = "reference="+chunk
        resp = requests.post(url, headers=headers, data=data)
        content = resp.text
        if "author" in content: 
            temp = content.split("author = {")[1].split("},")[0]
            temp = [x for x in temp.split(",") if len(x.strip())>2 and x.strip().isupper()]
    return authors"""

#print(extract_author(texta))
#result = service_two_extraction.ServiceTwo('knowledgegraph/file/2203.09361v1.pdf').get_references()

