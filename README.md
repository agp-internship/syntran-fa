# syntran-fa
Syntatic Transformer in Farsi.

This project's main goal is to clon the parsing trick based methods for data augmentation in question answering domain from English (as you can find in refrences) to Persian. We aim to first make a module which can get a question and it's corresponding answer and then return the paraphrased version of if it. Look at bellow examples:

| Question | Answer (Main) | Answer (1) | Answer (2) | ... | Answer (n) |
|:--------:|:-------------:|:----------:|:----------:|:---:|:----------:|
| چه کسی لامپ را اختراع کرد؟ | ادیسون | ادیسون تلفن را اختراع کرد | لامپ به وسیله ادیسون اختراع شد | ... | اختراع تلفن کار ادیسون بود |


## References
1. [Fluent Response Generation for Conversational Question Answering](https://aclanthology.org/2020.acl-main.19) (Baheti et al., ACL 2020)
2. [Good Question! Statistical Ranking for Question Generation](https://aclanthology.org/N10-1086) (Heilman & Smith, NAACL 2010)
3. [Accurate Unlexicalized Parsing](https://aclanthology.org/P03-1054) (Klein & Manning, ACL 2003)
