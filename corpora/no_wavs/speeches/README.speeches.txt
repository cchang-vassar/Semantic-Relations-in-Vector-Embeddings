IBM Debater(R): Recorded Debating Dataset
=========================================
V4, October 2019

** Note: this folder does not contain the audio (wav) files **

This folder contains 200 audio speeches and their automatic and manual transcripts as described in [2]. The recordings process is detailed in [3].
The speeches argue in favor (pro) or against (con) 50 different topics. Total duration of speeches: 13 hours, 45 minutes.
The annotation layer described in [1] is performed on these speeches.

Folders:
wav: Audio files (speeches) (not present in "no_wavs" release)
wav.asr: Raw ASR transcripts
wav.asr.txt: Post-processed ("clean") ASR transcripts
trs: Manual transcripts (Transcriber's format)
trs.txt: Processed (clean) manual transcripts ("references")

Other files:
* transcription-guidelines.pdf: describes the guidelines used in the transcription process.

Naming convention:
<Speaker's name>_<motion id>_<short topic desc>_<pro/con>_opening_<optional opponent name>.<optional transcriber name>.<extension>
E.g.: james_1264_human-cloning_pro_opening.dean.trs
The transcriber name is included only for transcribed files (.trs and .trs.txt files).
The opponent name is given only for speeches contesting the discussed controversial topic.

Notes:
* The speeches release in [2] includes 200 new speeches, in addition to 60 speeches released in [3].
* The speeches in this release were automatically transcribed using Watson Speech to Text.
* The dataset includes speeches arguing both in favor (pro) and against (con) a given topic.

====================================================================
[1] Matan Orbach, Yonatan Bilu, Ariel Gera, Yoav Kantor, Lena Dankin, Tamar Lavee, Lili Kotlerman, Shachar Mirkin, Michal Jacovi, Ranit Aharonov and Noam Slonim. A Dataset of General-Purpose Rebuttal. EMNLP 2019.
https://arxiv.org/abs/1909.00393
[2] Shachar Mirkin, Guy Moshkowich, Matan Orbach, Lili Kotlerman, Yoav Kantor, Tamar Lavee, Michal Jacovi, Yonatan Bilu, Ranit Aharonov and Noam Slonim. Listening Comprehension over Argumentative Content. EMNLP 2018.
https://www.aclweb.org/anthology/D18-1078
[3] Shachar Mirkin, Michal Jacovi, Tamar Lavee, Hong-kwang Kuo, Samuel Thomas, Leslie Sager, Lili Kotlerman, Elad Venezian and Noam Slonim. A Recorded Debating Dataset. LREC 2018.
https://arxiv.org/abs/1709.06438v2
