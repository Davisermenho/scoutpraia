---
source_id: SRC_RAG_STRUCTURED_FILE
titulo: Reducing hallucination in structured outputs via Retrieval-Augmented Generation
organizacao: NAACL Industry Track
tipo: Referência de IA/RAG
nivel_de_confiabilidade: C conceitual / fase 2
arquivo_original: docs/sources/2024.naacl-industry.19.pdf
arquivo_processado_logico: beach_handball_ai/fontes/05_processado/documentos_markdown/MD_PROCESSADO__SRC_RAG_STRUCTURED_FILE.md
texto_extraido_por: pdftotext -layout
status: revisado_manual_artigo_tabelas_principais_ok
data_processamento: 2026-06-11
---

# SRC_RAG_STRUCTURED_FILE

## Titulo de origem

Reducing hallucination in structured outputs via Retrieval-Augmented Generation

## Nota de revisao manual

O artigo preservou as seções centrais e as tabelas principais; diagramas e exemplos visuais seguem melhor representados no PDF.

## Texto extraido

Reducing hallucination in structured outputs via Retrieval-Augmented
                                                 Generation

                                  Patrice Béchard                                    Orlando Marquez Ayala
                                    ServiceNow                                            ServiceNow
                          patrice.bechard@servicenow.com                        orlando.marquez@servicenow.com



                                       Abstract

                     A current limitation of Generative AI (GenAI)
                     is its propensity to hallucinate. While Large
                     Language Models (LLM) have taken the world
                     by storm, without eliminating or at least reduc-
                     ing hallucination, real-world GenAI systems
                     will likely continue to face challenges in user
                     adoption. In the process of deploying an enter-
                     prise application that produces workflows from
                     natural language requirements, we devised a
                     system leveraging Retrieval-Augmented Gen-
                     eration (RAG) to improve the quality of the
                     structured output that represents such work-
                     flows. Thanks to our implementation of RAG,
                     our proposed system significantly reduces hal-           Figure 1: Sample structured output (JSON) to generate
                     lucination and allows the generalization of our          given a natural language requirement.
                     LLM to out-of-domain settings. In addition,
                     we show that using a small, well-trained re-             Such is the public concern for LLMs producing hal-
                     triever can reduce the size of the accompanying          lucinations that the Cambridge Dictionary chose
                     LLM at no loss in performance, thereby mak-              hallucinate as its Word of the Year in 2023 (Cam-
                     ing deployments of LLM-based systems less                bridge, 2023). Retrieval-Augmented Generation
                     resource-intensive.
                                                                              (RAG) is a well-known method that can reduce hal-
                                                                              lucination and improve output quality, especially
                1    Introduction
                                                                              when generating the correct output requires access
                With the advent of Large Language Models                      to external knowledge sources (Gao et al., 2024).
                (LLMs), structured output tasks such as converting               In this work, we describe how, in the process
                natural language to code or to SQL have become                of building a commercial application that converts
                commercially viable. A similar application is trans-          natural language to workflows, we employ RAG
                lating a natural language requirement to a work-              to improve the trustworthiness of the output by re-
                flow, a series of steps along with logic elements             ducing hallucination. Workflows are represented as
                specifying their relationships. These workflows               JSON documents where each step is a JSON object.
                encapsulate processes that are executed automati-             Figure 1 shows an example of a text requirement
                cally upon certain conditions, thereby increasing             and its associated JSON document. For simplic-
                employee productivity. While enterprise systems               ity, we include only the basic properties needed
                offer such functionality to automate repetitive work          to identify a step along with properties indicating
                and standardize processes, the barrier to entry is            the relationship between steps. Besides the work-
                high, as building workflows requires specialized              flow steps, there may also be a trigger step that
                knowledge. Generative AI (GenAI) can lower this               determines when the workflow should start, and
                barrier since novice users can specify in natural lan-        sometimes this trigger requires a database table
                guage what they want their workflows to execute.              name. Hallucination in this task means generating
                   However, as with any GenAI application, using              properties such as steps or tables that do not exist.
                LLMs naively can produce untrustworthy outputs.                  While fine-tuning a sufficiently large LLM can
                                                                          228
Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 6:
                                                              Industry Track), pages 228–238
                                             June 16-21, 2024 ©2024 Association for Computational Linguistics


produce reasonably good workflows, the model               queries and documents are unstructured data and
may hallucinate, particularly if the natural language      thus share the same semantic space. In our case, the
input is out-of-distribution. As the nature of enter-      queries are unstructured (natural language) and the
prise users requires them to customize their appli-        documents (JSON objects) are structured. Our re-
cations, in this case by adding their own type of          trieval training is similar to Structure Aware DeNse
workflow steps, a commercial GenAI application             ReTrievAl (SANTA), which proposes a training
needs to minimize the out-of-distribution mismatch.        method to align the semantics between code and
While one could fine-tune the LLM per enterprise,          text (Li et al., 2023b).
this may be prohibitively expensive due to the high
infrastructure costs of fine-tuning LLMs. Another             Generating structured data falls within the realm
consideration when deploying LLMs is their foot-           of Structured Output tasks, which consist of gen-
print, making it preferable to deploy the smallest         erating a valid structured output from natural lan-
LLM that can perform the task.                             guage, such as text-to-code, text-to-SQL (Zhong
   Our contributions are the following:                    et al., 2017; Yu et al., 2018; Wang et al., 2020)
                                                           or if-then program synthesis (Quirk et al., 2015;
    • We provide an application of RAG in work-            Liu et al., 2016; Dalal and Galbraith, 2020). They
      flow generation, a structured output task.           are challenging as they not only require generating
    • We show that using RAG reduces hallucina-            output that can be parsed, but also entities or field
      tion and improves results.                           values that exist in a given lexicon; otherwise the
    • We demonstrate that RAG allows deploying             resulting output cannot be interpreted or compiled.
      a smaller LLM while using a very small re-           For simple database schemas or small lexicons, this
      triever model, at no loss in performance.            extra information can be included in the prompt.
                                                           However, in our task the available pool of steps that
                                                           can be part of a workflow is potentially very large
2    Related Work
                                                           and customizable per deployment, thereby making
Retrieval-Augmented Generation is a common                 in-context learning impractical.
approach to limit generation of false or outdated
information in classical NLP tasks such as question           With the arrival of LLMs, these tasks have be-
answering and summarization (Lewis et al., 2020;           come more accessible. In particular, Code LLMs
Izacard and Grave, 2021; Shuster et al., 2021). In         enable developers to write code faster by providing
the GenAI era, it refers to a process where relevant       instructions to the LLM to generate code snippets
information from specific data sources is retrieved        (Chen et al., 2021; Nijkamp et al., 2022; Li et al.,
prior to generating text; the generation is then based     2023a; Roziere et al., 2023). These models, trained
on this retrieved information (Gao et al., 2024). Our      on large datasets of source code (Kocetkov et al.,
work differs from standard RAG as we apply it to           2022), have acquired broad knowledge of many
a structured output task. Instead of retrieving facts,     programming languages and have been shown to
we retrieve JSON objects that could be part of the         perform better at tasks that necessitate reasoning
JSON output document. Providing plausible JSON             (Madaan et al., 2022). Since the JSON schema to
objects to the LLM before generation increases the         represent workflows is domain-specific, we cannot
likelihood that the output JSON properties exist           use these models off-the-shelf. While fine-tuning
and that the generated JSON can be executed.               them on a small dataset increases the quality of
   A crucial ingredient of RAG is the retriever since      results, extra steps are required to reduce hallucina-
its output will be part of the LLM input. Compared         tion and support out-of-domain queries.
to classical methods such as TF-IDF or BM25 that
use lexical information, Dense Retrieval has been             Lastly, an alternative and complementary tech-
shown to be more effective as it maps the semantics        nique to reduce hallucination with LLMs is Guided
to a multidimensional space where both queries and         Generation using tools such as Outlines (Willard
documents are represented (Reimers and Gurevych,           and Louf, 2023). A sufficiently expressive context-
2019; Gao et al., 2021; Karpukhin et al., 2020;            free grammar could ensure that the steps generated
Xiong et al., 2020). These retrievers are often            by the model exist, but it does not provide extra
used in open-domain question answering systems             knowledge as to which steps the flow should in-
(Guu et al., 2020; Lee et al., 2019), where both           clude given the natural language query.
                                                         229


Figure 2: High-level architecture diagram showing how the user query is used by both the retriever and the LLM to
generate the structured JSON output.

3   Methodology                                           the retrieval results greatly. Similarly, fine-tuning
                                                          a model using our domain-specific data allows the
Figure 2 depicts the high-level architecture of our       retriever to learn the nuances and technicalities of
RAG system. During initialization, indices of steps       the text and JSON that are particular to our setting.
and tables are created using the retriever. When a           We use a siamese transformer encoder with mean
user submits a request, the retriever is called to sug-   pooling similar to Reimers and Gurevych (2019)
gest steps and tables. The suggestions are then ap-       to encode both the user query and the step or table
pended to the user query to form the LLM prompt.          JSON object into fixed-length vectors. We include
The LLM is then called to generate the workflow           a normalization layer in our model so that the re-
in the JSON format via greedy decoding.                   sulting embeddings have a norm of 1. We generate
   To build our system, we first train a retriever        three embeddings vq ∈ Rn , vs ∈ Rn , vt ∈ Rn :
encoder to align natural language with JSON ob-
jects. We then train an LLM in a RAG fashion by
including the retriever’s output in its prompt.              vq = R(q)        vs = R(s)        vt = R(t)      (1)

3.1 Retriever training                                       where q, s, t are the user query, step, and table
                                                          respectively. Retriever R can be decomposed as:
We expect the LLM to learn to construct JSON doc-
uments including the relationship between work-
flow steps, given sufficient examples. The risk of                R(q) = Norm(MeanPool(Enc(q)))               (2)
hallucination comes mainly from the step names
since there are tens of thousands of possible steps          The retriever model is trained on pairs of user
and every customer can add their own steps if the         queries and corresponding steps or tables. Since
default set does not meet their needs. In addition,       table names are used only in certain examples de-
as some trigger steps require database table names        pending on the type of trigger, a query can be
as a property, these names can also be hallucinated.      mapped to zero tables. For instance, the work-
We therefore require the retriever to map natural         flow in Figure 1 has four steps, forming four posi-
language to existing step and database table names.       tive training pairs, each pair consisting of the same
   We choose to fine-tune a retriever model for two       query and one of the steps in the flow. As the daily
reasons: to improve the mapping between text and          trigger step does not need a table name, the query
JSON objects, and to create a better representa-          is mapped to an empty list of tables.
tion of the domain of our application. While there           We also construct negative training pairs by sam-
exist a myriad of open-source sentence encoders           pling steps or tables that are not relevant to the user
(Reimers and Gurevych, 2019; Ni et al., 2022), they       query. We experiment with three different negative
have been trained in a setting where both queries         sampling strategies: random, BM25-based, and
and documents are in the same natural language            ANCE-based (Xiong et al., 2020).
semantic space. But in our case, the query or work-          The retriever is trained using a contrastive loss
flow requirement is unstructured while the JSON           (Hadsell et al., 2006) to minimize the distance be-
objects are structured data. Consistent with the          tween positive pairs (Y = 1) and negative pairs
results reported by Li et al. (2023b), who search         (Y = 0). Given the cosine similarity between
code snippets based on text, fine-tuning improves         the query and step (or table) vectors, and cosine
                                                      230


distance D = 1 − cossim(vq , vs ), we define con-          experiment with complicated or verbose prompts:
trastive loss L as:                                        we used a short and simple format, similar to Figure
                                                           3, to reduce the number of input tokens while mak-
                                                         ing it clear that this is a structured output task. As
        1                                  1
  L=            Y D2 + (1 − Y ) · max(0,     − D)2         shown in section 5.2, this approach yielded good
        2                                  2
                                                  (3)      performance.
   During initialization, we build an index of steps
                                                           4     Experiments
and tables using FAISS (Douze et al., 2024). When
a user submits a natural language query, we embed          As the task we are interested in is part of a commer-
the incoming query using our retriever and use             cial enterprise system, we had to devise our own
cosine similarity to retrieve the max K steps and          datasets as well as evaluation metrics.
tables associated with this requirement.
                                                           4.1    Datasets
3.2 LLM training                                           From internal deployments of our enterprise plat-
Contrary to end-to-end RAG systems such as Lewis           form, we extracted around 4,000 examples of de-
et al. (2020), we opted to train both the retriever and    ployed workflows and asked annotators to write
LLM separately, for simplicity. We use the trained         natural language requirements for them. In addi-
retriever to augment our dataset with suggested            tion, using deterministic rules, we created around
step and table names for each example. We then             1,000 samples having simple and few steps in or-
proceed with standard LLM supervised fine-tuning.          der to teach the model to handle input where the
                                                           user is incrementally building their workflow. To
                                                           have an unbiased estimate of the quality of results
                                                           once the system is deployed, we asked expert users
                                                           to simulate interacting with the system through a
                                                           simple user interface where they typed their require-
                                                           ment. We used these interactions and the expected
                                                           JSON documents to create an additional dataset
                                                           split, named "Human Eval." Our final metrics are
                                                           based on this split instead of the "Test" split, due
                                                           to its higher quality and more realistic input. Table
                                                           1 shows statistics for all of our in-domain splits.
                                                           Not all samples require triggers, and a small subset
Figure 3: Training example, where the last four lines      require the model to generate tables.
are the expected output (in red). The underlined text
comes from the retriever’s output.                                Split         Size   # Triggers    # Tables
                                                                  Train         2867      823          556
                                                                  Dev            318       77           44
   By inserting the retriever’s output in JSON for-               Test           798      247          163
mat into the LLM input, we effectively make this                  Human Eval     157       99           60
structured output task easier as the LLM can copy
                                                           Table 1: Data statistics for in-domain training and eval-
the relevant JSON objects during generation. Fig-
                                                           uation.
ure 3 shows an example of a training example. Ev-
ery line except the last four make up the LLM                 A drawback of our data labeling approach is
prompt. The suggested tables and steps come be-            that these internal datasets are mostly in the IT do-
fore the user query and are underlined in the figure.      main, whereas our RAG system can be deployed
We exclude the most frequent steps from these sug-         in diverse domains such as HR and finance. With-
gestions as we expect the LLM to memorize them.            out assessing the quality of the system in out-of-
Also, in every LLM training example, we assume             distribution settings, we cannot be confident that
the retriever has 100% recall: the steps and table         the system will behave as expected. We therefore
required to build the structured output are always in      asked annotators to label five other splits, which
the suggestions, except for the most frequent steps.       come from other deployments of our enterprise
   As we are showing the LLM thousands of exam-            platform. These are real workflows that have been
ples during training, we did not find it necessary to      created by real users.
                                                         231


   Table 2 includes statistics for these out-of-               We fine-tune models of different sizes to mea-
domain splits. A measure of how different they              sure the impact of model size on the final metrics.
are from our training data is the % of steps that           As StarCoderBase (Li et al., 2023a) has been pre-
are not in the set of steps in the "Train" split. This      trained on JSON in addition to many programming
discrepancy ranges from less than 10% to more               languages and comes in different sizes, we fine-
than 70%, highlighting the need to use a retriever          tune its 1B, 3B, 7B and 15.5B variants. Given our
and to customize the indices per deployment.                infrastructure constraints, we could deploy an LLM
                                                            of at most 7B parameters. Thus we also fine-tune
 Split    Size   # Triggers   # Tables   % Steps not
                                          in Train          other pretrained LLMs of this size: CodeLlama-7B
 OOD1      146       133          47        49%             (Roziere et al., 2023) and Mistral-7B-v0.1 (Jiang
 OOD2      162       111          21        76%             et al., 2023). All the LLMs were fine-tuned using
 OOD3      429       226         114        34%
 OOD4       42        25          11        33%             the same datasets and hyperparameters.
 OOD5      353       271          26         7%                We use all-mpnet-base-v21 as the base retriever
                                                            model. As it has only 110M parameters, it is suit-
 Table 2: Data statistics for out-of-domain evaluation.
                                                            able for deployment. We compare our fine-tuned
   To train the retriever encoder, we create pair ex-       model against different sizes of off-the-shelf GTR-
amples out of the 4,000 extracted and 1,000 deter-          T5 models (Ni et al., 2022) to see whether larger
ministically generated samples, resulting in around         encoders impact the performance.
15,000 pairs in the step names dataset and 1,500 in            Please see Appendix A for training details for
the table names dataset. The quality of this encoder        both the LLM and the retriever encoder.
is evaluated on the "Human Eval" split described
above.                                                      5        Results

4.2 Metrics                                                 5.1       Retriever encoder

We evaluate the entire RAG system using three               Table 3 shows the results of retrieval on the "Human
metrics, which can all range from 0 to 1:                   Eval" split for both steps and tables. Scaling the
                                                            size of the off-the-shelf encoders, as we did with
   • Trigger Exact Match (EM) verifies whether              GTR-T5, does not yield significant improvements
     the generated JSON trigger is exactly the same         on both retrieval metrics. A similar observation
     as the ground-truth, including the table name          was made by Neelakantan et al. (2022) for code
     if this trigger requires it.                           retrieval. What was crucial to significantly improve
   • Bag of Steps (BofS) measures the overlap               the performance was fine-tuning the encoder.
     between the generated JSON steps and the
     ground-truth steps in an order-agnostic fash-              Model (# Params)             Step          Table
                                                                                           Recall@15     Recall@10
     ion, akin to a bag-of-words approach.                      gtr-t5-base (110M)           0.505         0.489
   • Hallucinated Tables (HT) and Hallucinated                  gtr-t5-large (355M)          0.575         0.511
                                                                gtr-t5-xl (1.24B)            0.579         0.489
     Steps (HS) measure the % of generated ta-                  gtr-t5-xxl (4.8B)            0.561         0.489
     bles/steps that do not exist per workflow, in-             all-mpnet-base-v2 (110M)     0.425         0.170
     dicating that they were invented by the LLM.                  + Random                  0.640         0.752
                                                                   + BM25                    0.537         0.586
     This is the only metric where lower is better.                + ANCE                    0.556         0.699
   To evaluate the retriever, we use Recall@15 for                 + All                     0.743         0.766
steps and Recall@10 for tables. That is, given a            Table 3: Evaluation of different encoders on step and
natural language requirement, we retrieve the top           table retrieval. The last four rows represent encoders
K steps/tables from their respective indices and            fine-tuned using different negative sampling strategies.
verify whether they cover the set of steps and the
table, if required, included in the JSON document              Due to deployment considerations, we fine-tune
representing the workflow.                                  the smallest encoders (110M parameters), and
                                                            found that all-mpnet-base-v2 yielded the best per-
4.3 Models                                                  formance after fine-tuning with all negative sam-
As this is a production system, we have a trade-off         pling strategies.
between model size and performance for both the                  1
                                                                https://huggingface.co/sentence-transformers/all-mpnet-
LLM and the retriever encoder.                              base-v2

                                                          232


                                            Trigger     Bag of   Hallucinated   Hallucinated
                    Model                    EM         Steps       Steps         Tables
                    No Retriever
                    StarCoderBase-1B         0.580      0.645       0.157          0.192
                    StarCoderBase-3B         0.551      0.648       0.140          0.214
                    StarCoderBase-7B         0.547      0.669       0.137          0.206
                    StarCoderBase (15.5B)    0.632      0.662       0.160          0.194
                    With Retriever
                    StarCoderBase-1B         0.591      0.619       0.072          0.044
                    StarCoderBase-3B         0.615      0.641       0.017          0.030
                    StarCoderBase-7B         0.664      0.672       0.019          0.042
                    StarCoderBase (15.5B)    0.667      0.667       0.040          0.016
                    CodeLlama-7B             0.623      0.617       0.039          0.108
                    Mistral-7B-v0.1          0.596      0.617       0.049          0.045

Table 4: Performance of various model types and sizes on the "Human Eval" split. Lower is better for the
hallucination metrics. Results within 0.005 of the best score are highlighted in bold.

5.2 Retrieval-Augmented Generation                         5.3   OOD evaluation
Our main objective is to reduce hallucination while
                                                           We want our approach to perform well on OOD sce-
keeping the overall performance high given our in-
                                                           narios without further fine-tuning the retriever or
frastructure constraints. Table 4 shows that without
                                                           the LLM. Table 5 assesses the performance of our
a retriever (only LLM fine-tuning), the % of hal-
                                                           chosen RAG fine-tuned StarCoderBase-7B model
lucinated steps and tables can be as high as 21%
                                                           on the five OOD splits described by Table 2.
on the "Human Eval" split. Using a retriever, this
decreases to less than 7.5% for steps and less than
4.5% for tables with all StarCoderBase LLMs. All             Split          Trigger EM     BofS     HS      HT
models produce valid JSON documents following                OOD1              0.662       0.619   0.063   0.051
                                                             OOD2              0.645       0.612   0.020   0.151
the expected schema, thanks to fine-tuning.                  OOD3              0.562       0.743   0.014   0.033
   Without a retriever, scaling the size of the Star-        OOD4              0.400       0.671   0.011   0.154
                                                             OOD5              0.774       0.770   0.005   0.063
CoderBase models improves the Bag of Steps and               Avg.              0.647       0.714   0.018   0.066
Trigger Exact Match metrics, albeit unevenly. Scal-          No RAG Avg.       0.544       0.629   0.020   0.428
ing also helps with RAG, but we observe more                 Human Eval        0.664       0.672   0.019   0.042
consistent improvements. This suggests that larger
                                                           Table 5:      Performance of RAG            fine-tuned
LLMs can better copy and paste retrieved steps and
                                                           StarCoderBase-7B on OOD splits.
tables during generation.
   The smallest RAG fine-tuned model (1B) hallu-
cinates significantly more than its larger counter-           We observe that on average, thanks to the re-
parts. Among the other three variants, the 7B ver-         triever, all the OOD metrics are similar to the in-
sion gives us the best trade-off, as the performance       domain results represented by the "Human Eval"
difference between 7B and 15.5B is marginal. An-           split. We use a weighted average based on the
other observation is that the 3B version trained with      number of samples per split.
RAG is competitive even with the 15.5B version                To quantify the effect of suggesting step and
without RAG on the Trigger EM and Bag of Steps             table names, we evaluate the RAG fine-tuned
metrics, while keeping hallucination low. This is a        StarCoderBase-7B model without suggestions in
key lesson as we could deploy a 3B RAG fine-tuned          row "No RAG Avg.". All metrics worsen sig-
model if we had more limited infrastructure.               nificantly while the "Hallucinated Steps" remains
   Lastly, we compare the RAG fine-tuned                   roughly the same. Upon inspection, we see that the
StarCoderBase-7B to fine-tuning more recent                RAG fine-tuned model has learned to be conserva-
LLMs of the same size. Despite also fine-tuning            tive in generating steps when it does not receive
them with RAG, CodeLlama-7B and Mistral-7B-                suggestions, relying only on steps that it has seen
v0.1 produce worse results across all metrics, even        during training. On the other hand, the "Halluci-
compared to the smaller StarCoderBase-3B. We               nated Tables" metric is significantly worse as the
suspect that pre-training on large amounts of natu-        model is more creative when it comes to tables.
ral language data may be detrimental to our task.          Please see Appendix B for supplementary detail.
                                                      233


5.4 Error Analysis                                          We have several ideas to reduce the system re-
                                                         sponse time: changing the structured output format
When investigating error patterns found in the gen-
                                                         from JSON to YAML to reduce the number of to-
erated workflows, we observe issues arising from
                                                         kens, leveraging speculative decoding (Leviathan
failures both on the retriever and the LLM.
                                                         et al., 2023; Chen et al., 2023; Joao Gante, 2023),
   For complex flows where steps that are used less
                                                         and streaming one step at a time back to the user
frequently need to be retrieved, if a crucial compo-
                                                         instead of the entire generated workflow.
nent is not in the retriever’s suggestions, it becomes
difficult for the LLM to generate a valid workflow       6   Conclusion
in line with the user query. To improve the re-
triever’s recall, we can decompose the query into        We propose an approach to deploy a Retrieval-
shorter texts to make the retrieval step more precise    Augmented LLM to reduce hallucination and allow
for each step. This would mean performing several        generalization in a structured output task. Reduc-
retrieval calls, potentially one per step, instead of    ing hallucination is a sine qua non for users to
making one single retrieval call as we are doing         adopt real-world GenAI systems. We show that
now.                                                     RAG allows deploying a system in limited-resource
   In some cases, the LLM did not produce the de-        settings as a very small retriever can be coupled
sired structure. This is more often seen when using      with a small LLM. Future work includes improv-
steps that determine the logic of the workflow, such     ing the synergy between the retriever and the LLM,
as IF, TRY, or FOREACH. These are important errors       through joint training or a model architecture that
that can be addressed by synthetic data generation       allows them to work better together.
after analyzing which steps are being missed. For
examples of perfect output and when the retriever
                                                         Ethical Considerations
and LLM fail, please refer to Appendix C.                While our work proposes an approach to reduce
                                                         hallucination in structure output tasks, we do not
5.5 Impact on Engineering                                claim that the risk of harm due to hallucination is
The obtained results led us to make several deci-        eliminated. Our deployed system includes a layer
sions that impacted the scalability and modular-         of post-processing to clearly indicate to users the
ity of the system. Since the best overall perfor-        generated steps that do not exist and urge them to
mance was given by a 7B-parameter model, we              fix the output before continuing their work.
could have a larger batch size for incoming user
requests, thereby increasing the system throughput
                                                         Acknowledgements
given a single GPU. This implies a trade-off in la-      We thank our ServiceNow colleagues who worked
tency as larger queries (in number of tokens) result     hard in building the aforementioned system, from
in larger number of generated tokens, sometimes          project managers to quality engineers. We also
causing large queries to become a bottleneck if they     thank the several colleagues who reviewed an ear-
are included in a batch with many shorter queries.       lier version of this paper: Lindsay Brin, Hessam
Our stress tests and user research reveal that the       Amini, Erfan Hosseini, and Gabrielle Gauthier-
current system overall response time is acceptable.      Melançon, as well as the NAACL reviewers, for
   Obtaining good results after fine-tuning a very       their valuable feedback.
small encoder for the retriever (110M parameters),
allowed us to deploy it on the same GPU with neg-
ligible effect on the larger LLM. But we could even      References
deploy the retriever on CPU due to its small size.       Cambridge. 2023. Why hallucinate?   https://
A benefit of not performing joint training between         dictionary.cambridge.org/editorial/woty.
the retriever and the LLM is that the retriever can
                                                         Charlie Chen, Sebastian Borgeaud, Geoffrey Irving,
be reused for other use cases involving similar data       Jean-Baptiste Lespiau, Laurent Sifre, and John
sources. Moreover, decoupling them allows clearer          Jumper. 2023. Accelerating large language model
separation of concerns and independent optimiza-           decoding with speculative sampling.
tion by separate team members. Nevertheless, for         Mark Chen, Jerry Tworek, Heewoo Jun, Qiming
scientific purposes, it is still worthwhile to experi-    Yuan, Henrique Ponde de Oliveira Pinto, Jared Ka-
ment with joint training.                                 plan, Harri Edwards, Yuri Burda, Nicholas Joseph,
                                                     234


  Greg Brockman, et al. 2021. Evaluating large             Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick
  language models trained on code. arXiv preprint            Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and
  arXiv:2107.03374.                                          Wen-tau Yih. 2020. Dense passage retrieval for open-
                                                             domain question answering. In Proceedings of the
Dhairya Dalal and Byron V Galbraith. 2020. Evaluating        2020 Conference on Empirical Methods in Natu-
  sequence-to-sequence learning models for if-then pro-      ral Language Processing (EMNLP). Association for
  gram synthesis. arXiv preprint arXiv:2002.03485.           Computational Linguistics.

Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and            Denis Kocetkov, Raymond Li, LI Jia, Chenghao Mou,
   Christopher Ré. 2022. Flashattention: Fast and            Yacine Jernite, Margaret Mitchell, Carlos Muñoz Fer-
   memory-efficient exact attention with io-awareness.       randis, Sean Hughes, Thomas Wolf, Dzmitry Bah-
  Advances in Neural Information Processing Systems,         danau, et al. 2022. The stack: 3 tb of permissively li-
   35:16344–16359.                                           censed source code. Transactions on Machine Learn-
                                                             ing Research.
Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff
 Johnson, Gergely Szilvasy, Pierre-Emmanuel Mazaré,        Kenton Lee, Ming-Wei Chang, and Kristina Toutanova.
 Maria Lomeli, Lucas Hosseini, and Hervé Jégou.              2019. Latent retrieval for weakly supervised open do-
 2024. The faiss library.                                    main question answering. In Proceedings of the 57th
                                                             Annual Meeting of the Association for Computational
Tianyu Gao, Xingcheng Yao, and Danqi Chen. 2021.             Linguistics, pages 6086–6096.
  Simcse: Simple contrastive learning of sentence em-
                                                           Yaniv Leviathan, Matan Kalman, and Yossi Matias.
  beddings. In 2021 Conference on Empirical Meth-
                                                             2023. Fast inference from transformers via spec-
  ods in Natural Language Processing, EMNLP 2021,
                                                             ulative decoding.
  pages 6894–6910. Association for Computational
  Linguistics (ACL).                                       Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio
                                                             Petroni, Vladimir Karpukhin, Naman Goyal, Hein-
Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia,             rich Küttler, Mike Lewis, Wen-tau Yih, Tim Rock-
  Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, Qianyu Guo,       täschel, et al. 2020. Retrieval-augmented generation
  Meng Wang, and Haofen Wang. 2024. Retrieval-               for knowledge-intensive nlp tasks. In Proceedings of
  augmented generation for large language models: A          the 34th International Conference on Neural Infor-
  survey.                                                    mation Processing Systems, pages 9459–9474.
Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasu-          Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas
  pat, and Ming-Wei Chang. 2020. Realm: retrieval-           Muennighoff, Denis Kocetkov, Chenghao Mou, Marc
  augmented language model pre-training. In Proceed-         Marone, Christopher Akiki, Jia Li, Jenny Chim, et al.
  ings of the 37th International Conference on Machine       2023a. Starcoder: may the source be with you!
  Learning, pages 3929–3938.                                 arXiv preprint arXiv:2305.06161.

Raia Hadsell, Sumit Chopra, and Yann LeCun. 2006.          Xinze Li, Zhenghao Liu, Chenyan Xiong, Shi Yu,
  Dimensionality reduction by learning an invariant          Yu Gu, Zhiyuan Liu, and Ge Yu. 2023b. Structure-
  mapping. In 2006 IEEE Computer Society Confer-             aware language model pretraining improves dense
  ence on Computer Vision and Pattern Recognition,           retrieval on structured data. In Findings of the As-
  CVPR 2006, pages 1735–1742.                                sociation for Computational Linguistics: ACL 2023,
                                                             pages 11560–11574, Toronto, Canada. Association
Edward J Hu, Phillip Wallis, Zeyuan Allen-Zhu,               for Computational Linguistics.
  Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen,
  et al. 2021. Lora: Low-rank adaptation of large lan-     Chang Liu, Xinyun Chen, Eui Chul Shin, Mingcheng
  guage models. In International Conference on Learn-        Chen, and Dawn Song. 2016. Latent attention for
  ing Representations.                                       if-then program synthesis. Advances in Neural Infor-
                                                             mation Processing Systems, 29.
Gautier Izacard and Edouard Grave. 2021. Leveraging        Ilya Loshchilov and Frank Hutter. 2018. Decoupled
  passage retrieval with generative models for open           weight decay regularization. In International Confer-
  domain question answering. In EACL 2021-16th                ence on Learning Representations.
  Conference of the European Chapter of the Associa-
  tion for Computational Linguistics, pages 874–880.       Aman Madaan, Shuyan Zhou, Uri Alon, Yiming Yang,
  Association for Computational Linguistics.                and Graham Neubig. 2022. Language models of code
                                                            are few-shot commonsense learners. In Proceedings
Albert Q Jiang, Alexandre Sablayrolles, Arthur Men-         of the 2022 Conference on Empirical Methods in
  sch, Chris Bamford, Devendra Singh Chaplot, Diego         Natural Language Processing, pages 1384–1403.
  de las Casas, Florian Bressand, Gianna Lengyel, Guil-
  laume Lample, Lucile Saulnier, et al. 2023. Mistral      Arvind Neelakantan, Tao Xu, Raul Puri, Alec Rad-
  7b. arXiv preprint arXiv:2310.06825.                       ford, Jesse Michael Han, Jerry Tworek, Qiming Yuan,
                                                             Nikolas Tezak, Jong Wook Kim, Chris Hallacy, et al.
Joao Gante. 2023. Assisted generation: a new direction       2022. Text and code embeddings by contrastive pre-
  toward low-latency text generation.                        training. arXiv preprint arXiv:2201.10005.
                                                         235


Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Her-           In Proceedings of the 2018 Conference on Empiri-
   nandez Abrego, Ji Ma, Vincent Zhao, Yi Luan, Keith           cal Methods in Natural Language Processing, pages
   Hall, Ming-Wei Chang, et al. 2022. Large dual en-            3911–3921.
   coders are generalizable retrievers. In Proceedings
   of the 2022 Conference on Empirical Methods in           Victor Zhong, Caiming Xiong, and Richard Socher.
   Natural Language Processing, pages 9844–9855.              2017. Seq2sql: Generating structured queries from
                                                              natural language using reinforcement learning. arXiv
Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan         preprint arXiv:1709.00103.
  Wang, Yingbo Zhou, Silvio Savarese, and Caiming
  Xiong. 2022. Codegen: An open large language
   model for code with multi-turn program synthesis. In
  The Eleventh International Conference on Learning
   Representations.

Chris Quirk, Raymond Mooney, and Michel Galley.
  2015. Language to code: Learning semantic parsers
  for if-this-then-that recipes. In Proceedings of the
  53rd Annual Meeting of the Association for Compu-
  tational Linguistics and the 7th International Joint
  Conference on Natural Language Processing (Vol-
  ume 1: Long Papers), pages 878–888.

Nils Reimers and Iryna Gurevych. 2019. Sentence-bert:
  Sentence embeddings using siamese bert-networks.
  In Proceedings of the 2019 Conference on Empirical
  Methods in Natural Language Processing and the
  9th International Joint Conference on Natural Lan-
  guage Processing (EMNLP-IJCNLP). Association
  for Computational Linguistics.

Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten
  Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,
  Jingyu Liu, Tal Remez, Jérémy Rapin, et al. 2023.
  Code llama: Open foundation models for code. arXiv
  preprint arXiv:2308.12950.

Kurt Shuster, Spencer Poff, Moya Chen, Douwe Kiela,
  and Jason Weston. 2021. Retrieval augmentation
  reduces hallucination in conversation. In Findings
  of the Association for Computational Linguistics:
  EMNLP 2021, pages 3784–3803.

Bailin Wang, Richard Shin, Xiaodong Liu, Oleksandr
  Polozov, and Matthew Richardson. 2020. Rat-sql:
  Relation-aware schema encoding and linking for text-
  to-sql parsers. In Proceedings of the 58th Annual
  Meeting of the Association for Computational Lin-
  guistics, pages 7567–7578.

Brandon T Willard and Rémi Louf. 2023. Effi-
  cient guided generation for llms. arXiv preprint
  arXiv:2307.09702.

Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang,
  Jialin Liu, Paul N Bennett, Junaid Ahmed, and
  Arnold Overwijk. 2020. Approximate nearest neigh-
  bor negative contrastive learning for dense text re-
  trieval. In International Conference on Learning
  Representations.

Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga,
  Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingn-
  ing Yao, Shanelle Roman, et al. 2018. Spider: A
  large-scale human-labeled dataset for complex and
  cross-domain semantic parsing and text-to-sql task.
                                                          236


A   Training details for LLM and retriever               shown in Table 5, there are cases where the retriever
                                                         does not suggest what is expected or the LLM does
All LLMs were fine-tuned using the same set of hy-
                                                         not take into account the suggestions.
perparameters. We use the AdamW optimizer with
a learning rate of 5e − 4, β1 = 0.9, β2 = 0.999                        No suggestions    With suggestions
and weight decay of 0.01. Models were trained for             Split    # unique % H      # unique   %H
                                                                        tables            tables
5,000 steps with a cosine learning rate scheduler             OOD1        40     70%        22      14%
with 100 warmup steps. We use an effective batch              OOD2        31     71%        19      21%
size of 32 for all models, using gradient accumula-           OOD3        61     64%        44       9%
                                                              OOD4        11     54%         9      22%
tion when the batch size would not fit on a single            OOD5        38     68%        29      17%
GPU. We trained all models using LoRA (Hu et al.,
2021) with r = 16, α = 16 and a dropout rate of          Table 7: Statistics of generated table names in terms
0.05. All models were trained with flash-attention       of uniqueness and hallucination. H refers to unique
(Dao et al., 2022) on a single A100 80GB GPU.            hallucinated table names
   We fine-tuned the retriever model using the
SentenceTransformers framework (Reimers and                 When it comes to table names, there are similar
Gurevych, 2019). We use the AdamW optimizer              and different observations, as shown in Table 7. As
(Loshchilov and Hutter, 2018) and a learning rate        in the case of step names, without suggestions a
of 2e − 5. We use a batch size of 128 and train the      greater percentage of unique table names are in-
model for 10 epochs.                                     vented. However, when provided with suggestions,
                                                         the model is more conservative as it generates fewer
B   Differences in generation with and                   unique table names. This may be an artifact of the
    without suggestions                                  data, where there is less diversity of tables used
                                                         compared to step names.
To understand the impact of suggesting step and
table names during generation, for each OOD split,       C    Sample perfect output and errors
we inspect the % of unique steps and % of unique
                                                         Figure 4 shows three user queries along with their
table names that are hallucinated with and without
                                                         generated workflows. The first one is a compli-
suggestions.
                                                         cated workflow where the LLM is able to follow
   Table 6 shows that without suggestions, the RAG
                                                         exactly the structure described in the user query,
fine-tuned StarCoderBase-7B tends to generate sig-
                                                         and is able to use the steps that the user expected.
nificantly fewer unique step names. Receiving sug-
                                                         In this case, the retriever suggests only the step
gestions allows the model to copy the suggestions,
                                                         post_incident_details, as the rest are consid-
thereby increasing the diversity of what it gener-
                                                         ered common steps.
ates. In addition, without suggestions a greater
                                                            In the second example, the retriever fails to sug-
percentage of the unique step names it generates
                                                         gest the send_slack_message step. The result-
are invented.
                                                         ing workflow is not entirely wrong but it is of
              No suggestions   With suggestions          lesser quality as the LLM uses the common step
     Split    # unique % H     # unique   %H
                steps            steps
                                                         send_notification, which is not what the user
     OOD1        52     40%       100     13%            expected.
     OOD2        38     34%        96     13%               In the last example, the LLM shows that it does
     OOD3        122    37%       269      9%
     OOD4        20      5%       32       9%            not sufficiently understand the semantics of the task.
     OOD5        88     17%       151      3%            The word Try in the user query should have made
                                                         it use the TRY and CATCH flow logic, but the LLM
Table 6: Statistics of generated step names in terms     seems to ignore this word, resulting in a workflow
of uniqueness and hallucination. H refers to unique
                                                         that does not reflect what the user asked for.
hallucinated step names.

   We also see that even with suggestions, there is
still an important gap in the percentage of unique
step names that are hallucinated, as in some splits
more than 10% of unique steps are invented. While
the overall hallucination rate is less than 2%, as
                                                       237


        (a) Perfect output                    (b) Retrieval error                     (c) LLM error

Figure 4: Examples where both the retriever and the LLM worked perfectly and where each of them failed:
(a) All expected step names were suggested and used by the LLM. (b) The retriever did not suggest the step
send_slack_message and therefore the LLM used the common step send_notification instead. (c) The LLM
should have used the TRY step as the parent to all the steps, but it did not fully understand the user query.




                                                     238
