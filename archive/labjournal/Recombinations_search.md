# Поиск мутаций

Наши библиотеки были обработаны *bcftools* с параметрами Depth = 10, Qual = 30.

```
$ bcftools mpileup -f {genome} {input_filename} | bcftools call -cv -Ou | bcftools filter -i \"DP>{depth} & %QUAL>{quality}\" > {output_filename}
```

Файлы получились чересчур большими, поэтому было решено дополнительно отфильтровать их на экзом (несортированный bed-файл MedExome TargetCapture):

```
vcftools --vcf {input_filename} --bed {region} --out {output_filename} --recode
```

Далее библиотеки обрабатывались в VEP со всеми возможными параметрами.

## Нейрофиброматоз I типа у пациента 1-9

**Гены (hg19):**

* NF1, chr17:29,421,945-29,709,134
* NF2, chr22:29,999,545-30,094,589

### NF1

Результаты поиска [здесь](./scripts_results/1-9_NF1_search.csv).
Они были пропущены через VEP со всеми возможными параметрами.
Результаты [здесь](./scripts_results/1-9_NF1_vep.csv).

Ничего значимого не найдено.

### NF2

Результаты поиска [здесь](./scripts_results/1-9_NF2_search.csv).
Они были пропущены через VEP со всеми возможными параметрами.
Результаты [здесь](./scripts_results/1-9_NF2_vep.csv).

Ничего значимого не найдено.

## Ген CFTR у пациента 1-1

CFTR: chr7:117,120,148- 117,307,162

### Результаты

Миссенс-мутация в chr7:117,267,786.
Глубина покрытия участка - 16, мутация видна в 4 ридах (25%), после эмпирического анализа на ПЦР-дубликаты - в 1 из 5.
Данные частоты по популяциям отсутствуют во всех БД.
Скорее всего, ошибка секвенирования.

![Mutation IGV](./scripts_results/1-1_CFTR_missense1.png)

Все прочие мутации имеют низкий импакт и/или высокую частоту встречаемости в популяции.
[Полные результаты](./scripts_results/1-1_CFTR_vep.csv).

## Братья с умственной отсталостью

Были смержены таблицы, а затем вручную отобраны гены, связанные с умственной отсталостью и агрессией.
Все они были вручную проверены в IGV.

| Chrom | Position  | Ref | Alt | Genotype | Type | Symbol | Phenotypes_x | Total AF |
|:------|:----------|:---:|:---:|:---------|:-----|:-------|:-------------|:--------:|
| chr10 | 283578    | G   | T   | 0/1 | missense | ZMYND11 | Mental retardation, AD | 0.00016 |
| chr10 | 131639111 | C   | T   | 0/1 | missense | EBF3 | Hypotonia, ataxia, and delayed development syndrome, AD | 0.00012 |
| chr16 | 3819294   | C   | T   | 0/1 | missense | CREBBP | Menke-Hennekam syndrome 1, 618332 (3); Rubinstein-Taybi syndrome 1, AD | 0.00823 |
| chr17 | 7750177   | T(ACC)x13 | T(ACC)x15 | 0/1 | inframe insertion | KDM6B | Neurodevelopmental disorder with coarse facies and mild distal skeletal abnormalities, AD | - |
| chr17 | 17697093  | CCA(GCA)x13 | CCA(GCA)x12 | 0/1 | inframe deletion | RAI1 | Smith-Magenis syndrome, AD, Isolated cases | - |
| chr2 | 165984281  | T   | C   | 0/1 | missense | SCN3A | Epilepsy, familial focal, with variable foci, AD; Epileptic encephalopathy, early infantile, AD | 0.00023 |
| chr20 | 57428804  | A   | G   | 0/1 | missense | GNAS | McCune-Albright syndrome, somatic, mosaic; Osseous heteroplasia, progressive, AD; Pituitary adenoma, multiple types, somatic; Pseudohypoparathyroidism, AD; | 0.00699 |
| chr22 | 51135989  | GTT | G, GCCCCTT, GCCCCGCGCCCGGCCCCTT | 1/1 | splice acceptor, frameshift | SHANK3 | Phelan-McDermid syndrome, AD; Schizophrenia, AD  | - |

## Мутации из отчёта

1. Sample 1-1:
	* Chr4:62129501-62308035 -- не найдено.
	* Chr14:22598026-22964922 -- не найдено.

2. Sample 1-2:
	* Chr14:20253739-20376267 -- не найдено.

3. Samples 1-34 & 1-5:
	* Chr2:242886386-243007359 -- не найдено.
	* Chr6:32485173-32604038 -- не найдено.
	* Chr14:22536979-22964922 -- chr14:22934907, missense, TRDC. Вряд ли связан с заболеванием.

# Протокол подготовки таблиц

1. Что делать с ПЦР-дубликатами?

Было решено всё-таки применить PicardTools и посмотреть результаты.

```bash
PicardCommandLine MarkDuplicates REMOVE_DUPLICATES=true \
	M=/dev/datasets/FairWind/_results/bowtie/duplicates_experiment/sample-1-5_metrics.txt \
	I=/dev/datasets/FairWind/_results/bowtie/bam/sample-1-5_sorted.bam \
	O=/dev/datasets/FairWind/_results/bowtie/duplicates_experiment/sample-1-5_dupless.bam
```

Ради эксперимента был почищен сэмпл 1-5, в результате получилось 26% дубликатов, что совпадает с данными полученными при очистке PicardTools других библиотек.

2. Обе библиотеки -- с дубликатами и без -- были подвергнуты Filter Call и отфильтрованы на экзом.
Для обеих минимальная глубина была взята 10.

```bash
bcftools mpileup --threads 12 -f /dev/datasets/FairWind/_db/hg19/hg19.fa /dev/datasets/FairWind/_results/bowtie/duplicates_experiment/sample-1-5_dupless.bam | bcftools call --threads 12 -cv -Ou | bcftools filter --threads 12 -i "DP>10 & QUAL>30" | vcftools --vcf - --recode --recode-INFO-all --bed /dev/datasets/FairWind/_db/MedExome_hg19_capture_targets.sorted.bed --out /dev/datasets/FairWind/_results/bowtie/duplicates_experiment/sample-1-5_dupless_exome.vcf
```

Результаты проверки гетерозиготных снипов:

![Depth 10..50](./scripts_results/sample-1-5_exome_10-50.svg)
![Depth 50+](./scripts_results/sample-1-5_exome_50-inf.svg)

В результате решено применить PicardTools, затем отфильтровать следующим образом: DP>30, QUAL>30, количество альт. аллеля -- не менее 20%.

Результаты были проверены скриптом.
На графике видно, что новое выражение действительно отсекает аллели <20%.
Тем не менее возникают некоторые вопросы касательно фильтрации: несмотря на то, что мы применили более жёсткую фильтрацию, объём файлов получился в 2-3 раза больше.

![Depth 10..50](./scripts_results/sample-1-5_dupless_FilterCalls_DP30-QUAL30-ALT02_10-50.svg)
![Depth 50+](./scripts_results/sample-1-5_dupless_FilterCalls_DP30-QUAL30-ALT02_50-inf.svg)

**upd:** Причина выяснена.
В старых файлах vcftools автоматически чистил поле INFO, в новых оно сохранно.
Сравнение по количеству строк:

| Sample       | Dups, % | DP>10 & %QUAL>30 | Dupless, DP>30 & %QUAL>30 & ((DP4[2]+DP4[3])/DP)>0.2 | Rate    |
|:-------------|--------:|-----------------:|-----------------------------------------------------:|--------:|
| sample-1-1   | 26,9342 | 564762           | 15539                                                | 0,02751 |
| sample-1-2   | 25,4489 | 651248           | 17189                                                | 0,02639 |
| sample-1-3-4 | 49,5173 | 1759190          | 30187                                                | 0,01715 |
| sample-1-5   | 26,9395 | 856959           | 23989                                                | 0,02799 |
| sample-1-6   | 26,8407 | 817575           | 20357                                                | 0,02489 |
| sample-1-7-8 | 25,4693 | 671131           | 17653                                                | 0,02630 |
| sample-1-9   | 26,8077 | 786237           | 19742                                                | 0,02510 |

## Данные из Томска

В процессе выяснилось, что есть специальные инструменты для лучшего анализа bam-файлов.
Например, Qualimap.

Qualimap требует какие-то библиотеки R.
Я их установил и забыл, поэтому подробно писать не буду.

Qualimap отказался кушать наш target capture, поэтому пришлось произвести сервировку блюда:

```bash
awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$4,0,"."}' MedExome_hg19_capture_targets.sorted.bed > MedExome_hg19_capture_targets_sorted_FOR_HIS_MAGESTY_QUALIMAP.bed
```

Настройка:

```bash
#!/bin/bash

QUALIMAP_FOLDER="/dev/datasets/FairWind/_tools/qualimap_v2.2.1"
INPUT_FOLDER="/dev/datasets/FairWind/_results/60m/PRIMARY_ANALYSIS_13D/bam_sorted"
REPORT_FOLDER="/dev/datasets/FairWind/_results/60m/PRIMARY_ANALYSIS_13D/qualimap_reports"
EXOME="/dev/datasets/FairWind/_db/MedExome_hg19_capture_targets_sorted_FOR_HIS_MAGESTY_QUALIMAP.bed"

mkdir -l $REPORT_FOLDER

for name in 'dinara_38_S4_60M_sorted' 'dinara_38_S4_60M_sorted_dupless' 'sample-1-1_60M_sorted' 'sample-1-1_60M_sorted_dupless' 'sample-1-3_60M_sorted' 'sample-1-3_60M_sorted_dupless'
do

# SKIP DUPLICATES
$QUALIMAP_FOLDER/qualimap bamqc -bam $INPUT_FOLDER/"$name".bam --java-mem-size=20G \
	-c --feature-file $EXOME --outside-stats \
	-outdir $REPORT_FOLDER -outfile "$name"_report_skipdup.pdf -outformat PDF \
	--skip-duplicated --skip-dup-mode 2 ;

# NOT SKIP
$QUALIMAP_FOLDER/qualimap bamqc -bam $INPUT_FOLDER/"$name".bam --java-mem-size=20G \
	-c --feature-file $EXOME --outside-stats \
	-outdir $REPORT_FOLDER -outfile "$name"_report_notskip.pdf -outformat PDF ;

echo "$name" is ready.

done 
```

Отчёты по файлам доступны здесь ([архив](./scripts_results/reports_60Mtest.zip))

## 1-9

Из библиотек с удалёнными дубликатами были получены 4 мутации с низкой или неизвестной встречаемостью по БД.
Их импакт оценивается как LOW или MODIFIER.

Две мутации подтверждены эмпирически (цифры со слэшем -- глубина в необработанных bam-файлах и с удалёнными дубликатами соответственно):

| CHROM | POS      | REF | ALT | DP    | REF_DP | ALT_DP |
|:------|:---------|:---:|:---:|:-----:|:------:|:------:|
| chr17 | 29615616 | A   | G   | 71/46 | 37/21  | 34/25  |
| chr22 | 30067246 | G   | A   | 30/23 | 14/11  | 16/12  |

Ещё две -- сомнительно:

* chr22:30024129, CTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGT>CTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGTGT
* chr22:30060360, CCACACACACACACACACACACACACACACACACACA>CCACACACACACACACACACACACACACACACACA

## Дубликаты

Выяснилось, что оценка количества дубликатов сильно разнится.

Было решено найти способ, который находил бы максимальное количество.

1. Смена стратегии PicardTools

Picard был запущен с параметром `DUPLICATE_SCORING_STRATEGY=TOTAL_MAPPED_REFERENCE_LENGTH`.
Но смена стратегии ничего не дала.
Более того, смена стратегии нахождения дубликатов даже уменьшила их количество -- 17% против 26%.

## Покрытие

Подготовка:

```bash
for file in /dev/datasets/FairWind/_results/60m/PRIMARY_ANALYSIS_13D/coverage/full/*.txt; do grep "^all" $file > "$file".all; done
```

Результаты:

1. Геном:

| Sample                                           |   Non-coverage, % |   Middle |   Median |   Coverage 75% |   Coverage 90% |   Coverage 95% |
|:-------------------------------------------------|:-----------------:|:--------:|:--------:|:--------------:|:--------------:|:--------------:|
| dinara_38_S4_60M                                 |           56.0558 |  3.29033 |        0 |              0 |              0 |              0 |
| dinara_38_S4_60M_dupless                         |           56.0618 |  1.98961 |        0 |              0 |              0 |              0 |
| sample-1-1_60M                                   |           54.5764 |  2.65077 |        0 |              0 |              0 |              0 |
| sample-1-1_60M_dupless                           |           54.5796 |  2.18179 |        0 |              0 |              0 |              0 |
| sample-1-3_60M                                   |           30.5193 |  4.47836 |        2 |              0 |              0 |              0 |
| sample-1-3_60M_dupless                           |           30.5225 |  3.60706 |        2 |              0 |              0 |              0 |

2. Не экзом:

| Sample                                           |   Non-coverage, % |   Middle |   Median |   Coverage 75% |   Coverage 90% |   Coverage 95% |
|:-------------------------------------------------|:-----------------:|:--------:|:--------:|:--------------:|:--------------:|:--------------:|
| dinara_38_S4_60M                                 |           56.7183 |  1.62982 |        0 |              0 |              0 |              0 |
| dinara_38_S4_60M_dupless                         |           56.7244 |  1.15082 |        0 |              0 |              0 |              0 |
| sample-1-1_60M                                   |           55.1877 |  2.25654 |        0 |              0 |              0 |              0 |
| sample-1-1_60M_dupless                           |           55.1908 |  1.94458 |        0 |              0 |              0 |              0 |
| sample-1-3_60M                                   |           30.7146 |  3.80275 |        2 |              0 |              0 |              0 |
| sample-1-3_60M_dupless                           |           30.7179 |  3.20984 |        2 |              0 |              0 |              0 |

3. Экзом:

| Sample                                           |   Non-coverage, % |    Middle |   Median |   Coverage 75% |   Coverage 90% |   Coverage 95% |
|--------------------------------------------------|-------------------|-----------|----------|----------------|----------------|----------------|
| dinara_38_S4_60M                                 |           0.10141 | 111.993   |       86 |             55 |             35 |             26 |
| dinara_38_S4_60M_dupless                         |           0.10143 |  56.5586  |       52 |             36 |             25 |             19 |
| sample-1-1_60M                                   |           7.17837 |  28.3723  |       15 |              5 |              2 |              0 |
| sample-1-1_60M_dupless                           |           7.18048 |  17.8307  |       12 |              5 |              2 |              0 |
| sample-1-3_60M                                   |           0.09335 |  48.8947  |       38 |             24 |             15 |             10 |
| sample-1-3_60M_dupless                           |           0.09346 |  30.0374  |       27 |             18 |             12 |              9 |


![Coverage 60M](./scripts_results/graph_60M_191105.svg)

![Coverage 60M](./scripts_results/graph_60M_exome_191107.svg)

Обогащение:

| Sample                                           | Exome    | NOT Exome | Enrichment |
|--------------------------------------------------|----------|-----------|------------|
| dinara_38_S4_60M                                 | 111.993  | 1.62982   | 68.71495   |
| dinara_38_S4_60M_dupless                         | 56.5586  | 1.15082   | 49.14634   |
| sample-1-1_60M                                   | 28.3723  | 2.25654   | 12.57336   |
| sample-1-1_60M_dupless                           | 17.8307  | 1.94458   | 9.16943    |
| sample-1-3_60M                                   | 48.8947  | 3.80275   | 12.85772   |
| sample-1-3_60M_dupless                           | 30.0374  | 3.20984   | 9.35791    |

## Удаление пробелов из имен

Команда:

```bash
INPUT_FOLDER="/dev/datasets/FairWind/_results/cut/bridgeless"; OUTPUT_FOLDER="/dev/datasets/FairWind/_results/cut/bridgeless_SL"; mkdir -p $OUTPUT_FOLDER; cd $INPUT_FOLDER; for file in *.fastq.gz; do ( zcat $INPUT_FOLDER/$file | grep -oh "^[^ ]*" | gzip -c - > $OUTPUT_FOLDER/$file; echo $file is done. ) & done
```

## Выравнивание неразрезанных ридов

Команда:

```bash
boomer;
Logo "Uncut Align";
THREADS=10;
GENOME="/dev/datasets/FairWind/_db/hg19/hg19.fa"
INPUT_DIR="/dev/datasets/FairWind/_results/cut/bridgeless";
SAM_DIR="/dev/datasets/FairWind/_results/cut/uncut_sam";
BAM_DIR="/dev/datasets/FairWind/_results/cut/uncut_bam";
mkdir -p $SAM_DIR;
mkdir -p $BAM_DIR;
for var in '1-1' '1-2' '1-3' '1-4' '1-5' '1-6' '1-7' '1-8' '1-9';
do {
start_time=$(StartTime);
bwa mem -t $THREADS -v 1 $GENOME $INPUT_DIR/sample-"$var"_R1_Bridgeless.fastq.gz $INPUT_DIR/sample-"$var"_R2_Bridgeless.fastq.gz | tee $SAM_DIR/sample-"$var".sam | samtools view -bS -@ $THREADS - | samtools sort -@ $THREADS -O BAM - > $BAM_DIR/sample-"$var"_sorted.bam;
echo "Sample "$var" is ready "$(Timestamp $start_time)"";
} done
```

### Как выравнивает BWA

BWA выравнивает химерный рид в несколько мест.
Затем он выделяет главное выравнивание и пишет его в **soft-clipped** режиме, а другой выровненный кусок он пишет с тем же именем, но с флагом **supplementary** и в **hard-clipped** режиме.

Выравнивание идёт значительно эффективнее и в случае химерных ридов сравнимо с таковым при разрезании и скармливании ридов bowtie, но и гораздо медленнее (в ~2 раз).

## Удаление дубликатов

```bash
boomer;
Logo "Dup Remove";
INPUT_FOLDER="/dev/datasets/FairWind/_results/cut/uncut_bam";
OUTPUT_FOLDER="/dev/datasets/FairWind/_results/cut/uncut_bam_dupless";
mkdir -p $OUTPUT_FOLDER;
for file in $INPUT_FOLDER/*.bam;
do {
start_time=$(StartTime);
PicardCommandLine MarkDuplicates REMOVE_DUPLICATES=true M=$OUTPUT_FOLDER/$(FileBase $file)_metrics.txt I=$file O=$OUTPUT_FOLDER/$(FileBase $file)_dupless.bam;
echo "Sample "$(FileBase $file)" is ready "$(Timestamp $start_time)"";
} done
```

Обновлённая команда.
Удаление дубликатов идёт через стадию пересортировки по queryname.

```bash
boomer;
output_folder="/dev/datasets/FairWind/_results/cut/uncut_picard";
mkdir -p $output_folder;
mkdir -p $output_folder/queryname_sorted;
for file in /dev/datasets/FairWind/_results/cut/uncut_sam/*.sam;
do PicardCommandLine SortSam SO=queryname I=$file O=$output_folder/queryname_sorted/$(FileBase $file).bam;
done;
Seal $output_folder/queryname_sorted;
mkdir -p $output_folder/queryname_dupless;
for file in $output_folder/queryname_sorted/*.bam;
do PicardCommandLine MarkDuplicates REMOVE_DUPLICATES=true M=$output_folder/queryname_dupless/$(FileBase $file)_metrics.txt I=$file O=$output_folder/queryname_dupless/$(FileBase $file).bam;
done;
Seal $output_folder/queryname_dupless;
mkdir -p $output_folder/coordinate_dupless;
for file in $output_folder/queryname_dupless/*.bam;
do PicardCommandLine SortSam SO=coordinate I=$file O=$output_folder/coordinate_dupless/$(FileBase $file)_sorted.bam;
done;
Seal $output_folder/coordinate_dupless;
```

## Freebayes

```bash
boomer;
Logo "Filter Calls";
out_dir="/dev/datasets/FairWind/_results/cut/filtercalls";
exome="/dev/datasets/FairWind/_db/MedExome_hg19_capture_targets.sorted.bed";
ref="/dev/datasets/FairWind/_db/hg19/hg19.fa";
mkdir -p $out_dir;
for file in /dev/datasets/FairWind/_results/cut/uncut_picard/strandless_sorted/*.bam;
do {
out=$(echo ""$out_dir"/"$(FileBase $file)"_0minc10maxc200.vcf");
freebayes -0 --min-coverage 10 --max-coverage 200 -f $ref -t $exome -b $file -v $out;
} done
```

Далее файлы были профильтрованы по **QUAL** > 20.

## vcfallelicprimitives

```bash
boomer;
Logo "Primitive Calls";
out_dir="/dev/datasets/FairWind/_results/cut/filtercalls_primitive";
mkdir -p $out_dir;
for file in /dev/datasets/FairWind/_results/cut/filtercalls_qual20/*.vcf;
do {
out=$(echo ""$out_dir"/"$(FileBase $file)"_primitive.vcf");
vcflib vcfallelicprimitives $file > $out;
} done
```

Результаты работы:

```
BEFORE:
chr1	899932	.	AGGGGGGCGCGGGTC	AGGGGTCCGCAGGTC	509.966	.	AB=0;ABP=0;AC=2;AF=1;AN=2;AO=16;CIGAR=5M2X3M1X4M;DP=21;DPB=21.8;DPRA=0;EPP=3.55317;EPPR=0;GTI=0;LEN=15;MEANALT=4;MQM=59.125;MQMR=0;NS=1;NUMALT=1;ODDS=7.42288;PAIRED=0.875;PAIREDR=0;PAO=1;PQA=38.3333;PQR=38.3333;PRO=1;QA=594;QR=0;RO=0;RPL=10;RPP=5.18177;RPPR=0;RPR=6;RUN=1;SAF=7;SAP=3.55317;SAR=9;SRF=0;SRP=0;SRR=0;TYPE=complex	GT:DP:AD:RO:QR:AO:QA:GL	1/1:21:0,16:0:0:16:594:-53.4254,-4.81648,0

AFTER:
chr1	899937	.	G	T	509.966	.	AC=2;AF=1;LEN=1;TYPE=snp	GT	1|1
chr1	899938	.	G	C	509.966	.	AC=2;AF=1;LEN=1;TYPE=snp	GT	1|1
chr1	899942	.	G	A	509.966	.	AC=2;AF=1;LEN=1;TYPE=snp	GT	1|1
```

Делеции:

```
BEFORE:
chr1	1420569	.	GCCCTCCCTG	GCCTG	295.639	.	AB=0.466667;ABP=3.29983;AC=1;AF=0.5;AN=2;AO=14;CIGAR=1M5D4M;DP=30;DPB=23;DPRA=0;EPP=5.49198;EPPR=3.0103;GTI=0;LEN=5;MEANALT=1;MQM=59.9286;MQMR=54.75;NS=1;NUMALT=1;ODDS=68.0734;PAIRED=1;PAIREDR=1;PAO=0;PQA=0;PQR=0;PRO=0;QA=494;QR=599;RO=16;RPL=11;RPP=12.937;RPPR=11.6962;RPR=3;RUN=1;SAF=8;SAP=3.63072;SAR=6;SRF=10;SRP=5.18177;SRR=6;TYPE=del	GT:DP:AD:RO:QR:AO:QA:GL	0/1:30:16,14:16:599:14:494:-35.7353,0,-45.0125

AFTER:
chr1	1420569	.	GCCCTC	G	295.639	.	AC=1;AF=0.5;LEN=5;TYPE=del	GT	0|1
```


## 20-120 dupless

```bash
boomer;
Logo "SORT!";
output_folder="/dev/datasets/FairWind/_results/cut/uncut_picard/20-120strandless_sorted";
mkdir -p $output_folder;
for file in /dev/datasets/FairWind/_results/cut/uncut_picard/20-120strandless/*.bam;
do PicardCommandLine SortSam SO=coordinate I=$file O=$output_folder/$(FileBase $file).bam;
done;
Seal $output_folder;
```

```bash
boomer;
Logo "20-120 strandless coverage";
FAI="/dev/datasets/FairWind/_db/hg19/hg19.fa.fai";
NOT_EXOME="/dev/datasets/FairWind/_db/NOT_MedExome_hg19.bed";
EXOME="/dev/datasets/FairWind/_db/MedExome_hg19_capture_targets.sorted.bed";
OUTPUT_PATH="/dev/datasets/FairWind/_results/cut/uncut_picard/20-120strandless_coverage";
mkdir -p $OUTPUT_PATH;
for var in /dev/datasets/FairWind/_results/cut/uncut_picard/20-120strandless_sorted/*.bam;
do {
bedtools coverage -hist -sorted -g $FAI -a $NOT_EXOME -b $var > $OUTPUT_PATH/$(FileBase $var)_NotExomeCoverage.txt;
bedtools coverage -hist -sorted -g $FAI -a $EXOME -b $var > $OUTPUT_PATH/$(FileBase $var)_ExomeCoverage.txt;
} done
```
Результаты (**Sample 1-5**):

Not Exome:

| Sample    |   Non-coverage, % |   Middle |   Median |   Coverage 75% |   Coverage 90% |   Coverage 95% |
|-----------|-------------------|----------|----------|----------------|----------------|----------------|
| 20000000  |           76.6676 | 0.470739 |        0 |              0 |              0 |              0 |
| 40000000  |           63.3146 | 0.93929  |        0 |              0 |              0 |              0 |
| 60000000  |           54.1483 | 1.40686  |        0 |              0 |              0 |              0 |
| 80000000  |           47.3194 | 1.87457  |        1 |              0 |              0 |              0 |
| 100000000 |           41.9619 | 2.34179  |        1 |              0 |              0 |              0 |
| 120000000 |           37.6379 | 2.80842  |        1 |              0 |              0 |              0 |

![image](./scripts_results/20-120strandless_NotExome_graph.svg)

Exome:

| Sample    |   Non-coverage, % |   Middle |   Median |   Coverage 75% |   Coverage 90% |   Coverage 95% |
|-----------|-------------------|----------|----------|----------------|----------------|----------------|
| 20000000  |          14.907   |  5.70202 |        4 |              2 |              0 |              0 |
| 40000000  |           5.93654 | 11.4352  |        8 |              4 |              1 |              0 |
| 60000000  |           3.05398 | 17.2108  |       12 |              6 |              2 |              1 |
| 80000000  |           1.79655 | 22.9267  |       16 |              8 |              3 |              2 |
| 100000000 |           1.15451 | 28.6234  |       20 |             10 |              5 |              3 |
| 120000000 |           0.76931 | 34.3574  |       24 |             12 |              6 |              3 |

![image](./scripts_results/20-120strandless_Exome_graph.svg)

## Annovar

Загрузка списка доступных БД:

```bash
perl annotate_variation.pl -downdb -buildver hg19 -webfrom annovar avdblist humandb/
```

Таблица:

```bash
perl table_annovar.pl ./sample-1-1_strand-filtered_sorted_0minc10maxc200_QUAL20_primitive.vcf ./humandb -buildver hg19 -protocol knownGene,ensGene,refGene,abraom,AFR.sites.2015_08,ALL.sites.2015_08,AMR.sites.2015_08,ASN.sites.2012_04,avgwas_20150121,avsift,avsnp150,cadd13,cg69,clinvar_20190305,cosmic70,dann,dbnsfp35c,dbscsnv11,EAS.sites.2015_08,eigen,esp6500_all,EUR.sites.2015_08,exac03,fathmm,gene4denovo201907,gerp++,gme,gnomad211_genome,gwava,hrcr1,icgc21,intervar_20180118,kaviar_20150923,ljb26_all,mcap13,mitimpact24,MT_ensGene,nci60,popfreq_all_20150413,regsnpintron,revel,SAS.sites.2015_08,snp142 --operation g,g,g,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f --remove --vcfinput --thread 10
```
